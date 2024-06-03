from datetime import datetime

from .Read import *

from sqlalchemy.orm import Session
from .. import ORMs
from ..schemas import LineUpdate, StationUpdate, UserUpdate
import logging


def modify_line(db: Session, line_id: int, line_update: LineUpdate):
    try:
        line = db.query(ORMs.Line).filter(ORMs.Line.line_id == line_id).first()
        if not line:
            return None

        if line_update.chinese_name is not None:
            line.chinese_name = line_update.chinese_name
        if line_update.start_time is not None:
            line.start_time = line_update.start_time
        if line_update.end_time is not None:
            line.end_time = line_update.end_time
        if line_update.mileage is not None:
            line.mileage = line_update.mileage
        if line_update.color is not None:
            line.color = line_update.color
        if line_update.first_opening is not None:
            line.first_opening = line_update.first_opening
        if line_update.intro is not None:
            line.intro = line_update.intro
        if line_update.url is not None:
            line.url = line_update.url

        db.commit()
        db.refresh(line)
        logging.info(f"Line {line_id} modified successfully.")
        return line
    except Exception as e:
        db.rollback()
        logging.error(f"Error modifying line: {e}")
        return None


def modify_station(db: Session, station_id: int, station_update: StationUpdate):
    try:
        station = db.query(ORMs.Stations).filter(ORMs.Stations.station_id == station_id).first()
        if not station:
            return None

        if station_update.chinese_name is not None:
            station.chinese_name = station_update.chinese_name
        if station_update.english_name is not None:
            station.english_name = station_update.english_name
        if station_update.district is not None:
            station.district = station_update.district
        if station_update.intro is not None:
            station.intro = station_update.intro
        if station_update.status is not None:
            station.status = station_update.status

        db.commit()
        db.refresh(station)
        logging.info(f"Station {station_id} modified successfully.")
        return station
    except Exception as e:
        db.rollback()
        logging.error(f"Error modifying station: {e}")
        return None


def c_alight(db: Session, card_code: int, start_station: str, end_station: str):
    try:
        unfinished = get_unfinished_card_rides(db)
        for ride in unfinished:
            if ride.card_code == card_code:
                price = get_price(db, start_station, end_station)
                if not price:
                    logging.error("Error: Price not found for the given stations")
                    return {"error": "Price not found for the given stations"}

                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                db.query(ORMs.CardRide).filter(
                    ORMs.CardRide.card_code == card_code,
                    ORMs.CardRide.end_time == None
                ).update({
                    ORMs.CardRide.end_station: end_station,
                    ORMs.CardRide.end_time: end_time,
                    ORMs.CardRide.price: price
                })

                db.query(ORMs.Cards).filter(
                    ORMs.Cards.code == card_code
                ).update({
                    ORMs.Cards.money: ORMs.Cards.money - price
                })

                money = db.query(ORMs.Cards.money).filter(
                    ORMs.Cards.code == card_code
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

                db.query(ORMs.PassengerRide).filter(
                    ORMs.PassengerRide.passenger_id == passenger_id,
                    ORMs.PassengerRide.end_time == None
                ).update({
                    ORMs.PassengerRide.end_station: end_station,
                    ORMs.PassengerRide.end_time: end_time,
                    ORMs.PassengerRide.price: price
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


def modify_user(db: Session, user_name: str, user_update: UserUpdate):
    try:
        user = db.query(ORMs.UserIdentity).filter(ORMs.UserIdentity.user_name == user_name).first()
        if not user:
            return None

        if user_update.password is not None:
            user.password = user_update.password
        if user_update.permission is not None:
            user.permission = user_update.permission

        db.commit()
        db.refresh(user)
        logging.info(f"User {user_name} modified successfully.")
        return user
    except Exception as e:
        db.rollback()
        logging.error(f"Error modifying user: {e}")
        return None

