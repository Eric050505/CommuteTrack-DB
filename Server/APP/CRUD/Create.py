from datetime import datetime
from typing import List

from sqlalchemy import text

from .Read import *
from .. import ORMs
from ..schemas import *


def add_line(db: Session, line_create: LineCreate):
    try:
        db.execute(text("SELECT setval('lines_line_id_seq', (SELECT MAX(line_id) FROM lines));"))
        new_line = ORMs.Line(**line_create.dict())
        db.add(new_line)
        db.commit()
        db.refresh(new_line)
        logging.info(f"Line {new_line.chinese_name} added successfully.")
        return new_line
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding line: {e}")
        return None


def add_station(db: Session, station_create: StationCreate):
    try:
        db.execute(text("SELECT setval('stations_station_id_seq', (SELECT MAX(station_id) FROM stations))"))
        new_station = ORMs.Stations(**station_create.dict())
        db.add(new_station)
        db.commit()
        db.refresh(new_station)
        logging.info(f"Station {new_station.english_name} added successfully.")
        return new_station
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding station: {e}")
        return None


def place_new_stations(db: Session, line_id: int, stations: List[LinesDetailCreate]):
    try:
        for station in stations:
            station_id = station.station_id
            logging.info(f"{station_id}")
            status = db.query(ORMs.Stations.status).filter(ORMs.Stations.station_id == station_id).first()[0]
            logging.info(f"{status}")
            if status == 'running':
                logging.info(f"Station {station_id} is running.")
                position = station.nums
                db.query(ORMs.LinesDetail).filter(
                    ORMs.LinesDetail.line_id == line_id,
                    ORMs.LinesDetail.nums >= position
                ).update({ORMs.LinesDetail.nums: ORMs.LinesDetail.nums + 1})
                new_line_detail = ORMs.LinesDetail(line_id=line_id, station_id=station_id, nums=position)
                db.add(new_line_detail)

        db.commit()
        print("Stations placed in line successfully.")
        return {"message": "Stations placed in line successfully"}
    except Exception as e:
        db.rollback()
        logging.info(f"Error adding stations to line: {e}")
        return {"error": str(e)}


def p_board(db: Session, passenger_id: str, start_station: str):
    try:
        unfinished = get_unfinished_passenger_rides(db)
        for passenger in unfinished:
            if passenger.passenger_id == passenger_id:
                logging.error("This passenger has not finished the last ride!")
                return {"error": "This passenger has not finished the last ride!"}

        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_ride = ORMs.PassengerRide(
            passenger_id=passenger_id,
            start_station=start_station,
            start_time=start_time,
            end_time=None,
            price=0
        )
        db.execute(text("SELECT setval('passenger_ride_passenger_ride_id_seq', "
                        "(SELECT MAX(passenger_ride_id) FROM passenger_ride))"))
        db.add(new_ride)
        db.commit()
        logging.info("Passenger boarded successfully.")
        return {"success": "Passenger boarded successfully."}
    except Exception as e:
        db.rollback()
        logging.error(f"Error boarding passenger: {e}")
        return {"error": f"Error boarding passenger: {e}"}


def c_board(db: Session, card_code: int, start_station: str):
    try:
        unfinished = get_unfinished_card_rides(db)
        logging.info(f"Card boarded successfully. {unfinished}")

        for ride in unfinished:
            if ride.card_code == card_code:
                logging.error("This card has not finished the last ride!")
                return {"error": "This card has not finished the last ride!"}

        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_ride = ORMs.CardRide(
            card_code=card_code,
            start_station=start_station,
            start_time=start_time,
            end_time=None,
            price=0
        )
        db.execute(text("SELECT setval('card_ride_card_ride_id_seq', (SELECT MAX(card_ride_id) FROM card_ride))"))
        db.add(new_ride)
        db.commit()
        logging.info("Card boarded successfully.")
        return {"success": "Card boarded successfully."}
    except Exception as e:
        db.rollback()
        logging.error(f"Error boarding card: {e}")
        return {"error": f"Error boarding card: {e}"}


def add_passenger(db: Session, passenger_create: PassengerCreate):
    try:
        db.execute(text("SELECT setval('passenger_passenger_id_seq', (SELECT MAX(passenger_id) FROM passenger));"))
        new_passenger = ORMs.Passenger(**passenger_create.dict())
        logging.info(f"Passenger {new_passenger} added. !")
        db.add(new_passenger)
        db.commit()
        db.refresh(new_passenger)
        logging.info(f"Passenger {new_passenger.name} added successfully.")
        return new_passenger
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding passenger: {e}")
        return None


def add_card(db: Session, card_create: CardCreate):
    try:
        db.execute(text("SELECT setval('cards_card_id_seq', (SELECT MAX(card_id) FROM cards));"))
        new_card = ORMs.Cards(
            code=card_create.code,
            money=card_create.money,
            create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        )
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        logging.info(f"Code {new_card.code} added successfully.")
        return new_card
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding code: {e}")
        return None
