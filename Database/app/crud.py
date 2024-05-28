import datetime
import logging

from sqlalchemy.orm import Session
from . import models


def get_line(db: Session, line_id: int):
    logging.info(f"Start station ID: {line_id}")
    return db.query(models.Line).filter(models.Line.line_id == line_id).first()


def get_price(db: Session, start_station: str, end_station: str):
    try:
        start_station_id = db.query(models.Stations.station_id).filter(
            models.Stations.english_name == start_station).scalar()
        logging.info(f"Start station ID: {start_station_id}")
        end_station_id = db.query(models.Stations.station_id).filter(
            models.Stations.english_name == end_station).scalar()
        logging.info(f"End station ID: {end_station_id}")

        if start_station_id is None or end_station_id is None:
            logging.warning("One of the stations was not found.")
            return None

        result = (
            db.query(models.Price.price)
            .filter(models.Price.start_station_id == start_station_id)
            .filter(models.Price.end_station_id == end_station_id)
            .first()
        )
        logging.info(f"Query result: {result}")

        return result[0]
    except Exception as e:
        db.rollback()
        logging.error(f"Error querying price: {e}")
        return None


def get_adjacent_stations(db: Session, line_id: int, station_id: int, n: int):
    try:
        station = db.query(models.Stations).filter(models.Stations.station_id == station_id).first()
        logging.info(f"Start station ID: {station.english_name}")

        if not station:
            logging.warning(f"Station with id {station_id} not found.")
            return None
        english_name = station.english_name
        line_detail = db.query(models.LinesDetail).filter(models.LinesDetail.line_id == line_id,
                                                          models.LinesDetail.station_id == station_id).first()
        if not line_detail:
            logging.warning(f"Line detail for line_id {line_id} and station_id {station_id} not found.")
            return None
        nums = line_detail.nums

        results = db.query(models.Stations.chinese_name, models.Stations.english_name).distinct() \
            .join(models.LinesDetail, models.LinesDetail.station_id == models.Stations.station_id) \
            .filter(models.LinesDetail.line_id == line_id) \
            .filter((models.LinesDetail.nums == nums - n) | (models.LinesDetail.nums == nums + n)).all()

        if len(results) < 2:
            logging.warning(
                f"Index out of bounds when adding or subtracting {n} for station_id {station_id} on line_id {line_id}.")
            return None

        ahead_station = results[0]
        behind_station = results[1]

        logging.info(
            f"The stations that is the {n}-th {english_name} ahead:"
            f" {ahead_station.english_name} ({ahead_station.chinese_name})")
        logging.info(
            f"The stations that is the {n}-th {english_name} behind:"
            f" {behind_station.english_name} ({behind_station.chinese_name})")

        return {
            "bias": {n},
            "ahead": {
                "chinese_name": ahead_station.chinese_name,
                "english_name": ahead_station.english_name
            },
            "behind": {
                "chinese_name": behind_station.chinese_name,
                "english_name": behind_station.english_name
            }
        }

    except Exception as e:
        db.rollback()
        logging.error(f"Error querying adjacent stations: {e}")
        return None


def get_unfinished_passenger_rides(db: Session):
    try:
        unfinished_rides = db.query(
            models.PassengerRide.passenger_id,
            models.PassengerRide.start_station,
            models.PassengerRide.start_time
        ).filter(models.PassengerRide.end_time == None).all()  # SQLAlchemy uses 'None' for NULL

        return unfinished_rides
    except Exception as e:
        logging.error(f"Error querying unfinished passenger rides: {e}")
        return None


def get_unfinished_card_rides(db: Session):
    try:
        unfinished_rides = db.query(
            models.CardRide.card_code,
            models.CardRide.start_station,
            models.CardRide.start_time
        ).filter(models.CardRide.end_time == None).all()  # SQLAlchemy uses 'None' for NULL

        return unfinished_rides
    except Exception as e:
        logging.error(f"Error querying unfinished card rides: {e}")
        return None


def p_board(db: Session, passenger_id: str, start_station: str):
    try:
        unfinished = get_unfinished_passenger_rides(db)
        for passenger in unfinished:
            if passenger.passenger_id == passenger_id:
                logging.error("This passenger has not finished the last ride!")
                return {"error": "This passenger has not finished the last ride!"}

        start_time = datetime.now()
        new_ride = models.PassengerRide(
            passenger_id=passenger_id,
            start_station=start_station,
            start_time=start_time,
            end_time=None,
            price=0
        )

        db.add(new_ride)
        db.commit()
        logging.info("Passenger boarded successfully.")
        return {"success": "Passenger boarded successfully."}
    except Exception as e:
        db.rollback()
        logging.error(f"Error boarding passenger: {e}")
        return {"error": f"Error boarding passenger: {e}"}


def p_alight(db: Session, passenger_id: str, start_station: str, end_station: str):
    try:
        unfinished = get_unfinished_passenger_rides(db)
        for passenger in unfinished:
            if passenger.passenger_id == passenger_id:
                end_time = datetime.now()
                price = get_price(db, start_station, end_station)
                if not price:
                    logging.error("Error: Price not found for the given stations")
                    return {"error": "Price not found for the given stations"}

                db.query(models.PassengerRide).filter(
                    models.PassengerRide.passenger_id == passenger_id,
                    models.PassengerRide.end_time == None
                ).update({
                    models.PassengerRide.end_station: end_station,
                    models.PassengerRide.end_time: end_time,
                    models.PassengerRide.price: price
                })
                db.commit()
                logging.info("Passenger alighted successfully.")
                return {"success": "Passenger alighted successfully."}
        logging.error("Error: Passenger has not been boarded!")
        return {"error": "Passenger has not been boarded!"}
    except Exception as e:
        db.rollback()
        logging.error(f"Error alighting passenger: {e}")
        return {"error": f"Error alighting passenger: {e}"}


def c_board(db: Session, card_code: str, start_station: str):
    try:
        unfinished = get_unfinished_card_rides(db)
        for ride in unfinished:
            if ride.card_code == card_code:
                logging.error("This card has not finished the last ride!")
                return {"error": "This card has not finished the last ride!"}

        start_time = datetime.now()
        new_ride = models.CardRide(
            card_code=card_code,
            start_station=start_station,
            start_time=start_time,
            end_time=None,
            price=0
        )
        db.add(new_ride)
        db.commit()
        logging.info("Card boarded successfully.")
        return {"success": "Card boarded successfully."}
    except Exception as e:
        db.rollback()
        logging.error(f"Error boarding card: {e}")
        return {"error": f"Error boarding card: {e}"}


def c_alight(db: Session, card_code: str, start_station: str, end_station: str):
    try:
        unfinished = get_unfinished_card_rides(db)
        for ride in unfinished:
            if ride.card_code == card_code:
                price = get_price(db, start_station, end_station)
                if not price:
                    logging.error("Error: Price not found for the given stations")
                    return {"error": "Price not found for the given stations"}

                end_time = datetime.now()
                db.query(models.CardRide).filter(
                    models.CardRide.card_code == card_code,
                    models.CardRide.end_time == None
                ).update({
                    models.CardRide.end_station: end_station,
                    models.CardRide.end_time: end_time,
                    models.CardRide.price: price
                })

                db.query(models.Cards).filter(
                    models.Cards.code == card_code
                ).update({
                    models.Cards.money: models.Cards.money - price
                })

                money = db.query(models.Cards.money).filter(
                    models.Cards.code == card_code
                ).scalar()

                if money < 0:
                    logging.error(
                        "Error: This card does not have enough money! "
                        "Please go to the Customer Service Center for help!")
                    return {
                        "error": "This card does not have enough money! "
                                 "Please go to the Customer Service Center for help!"}

                db.commit()
                logging.info(f"Card alighted successfully. Account Balance: {money}")
                if money < 10:
                    logging.warning("Warning: This card has less than 10 RMB!")
                return {
                    "success": "Card alighted successfully.",
                    "balance": money,
                    "warning": "This card has less than 10 RMB!" if money < 10 else None
                }
        logging.error("Error: Card has not been boarded!")
        return {"error": "Card has not been boarded!"}
    except Exception as e:
        db.rollback()
        logging.error(f"Error alighting card: {e}")
        return {"error": f"Error alighting card: {e}"}
