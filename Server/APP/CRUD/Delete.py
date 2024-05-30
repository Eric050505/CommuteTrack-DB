from .Read import *
from sqlalchemy.orm import Session
from .. import ORMs


def delete_line(db: Session, line_id: int):
    try:
        line = db.query(ORMs.Line).filter(ORMs.Line.line_id == line_id).first()
        if not line:
            return None
        db.delete(line)
        db.commit()
        logging.info(f"Line {line.chinese_name} deleted successfully.")
        return line.chinese_name
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting line: {e}")
        return None


def delete_station(db: Session, station_id: int):
    try:
        station = db.query(ORMs.Stations).filter(ORMs.Stations.station_id == station_id).first()
        if not station:
            return None

        english_name = station.english_name
        db.delete(station)
        db.commit()
        logging.info(f"Station {english_name} deleted successfully.")
        return english_name
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting station: {e}")
        return None


def remove_station_in_line(db: Session, line_id: int, station_id: int):
    try:
        line_detail = db.query(ORMs.LinesDetail).filter(
            ORMs.LinesDetail.line_id == line_id,
            ORMs.LinesDetail.station_id == station_id
        ).first()

        if line_detail:
            position = line_detail.nums
            db.delete(line_detail)
            db.query(ORMs.LinesDetail).filter(
                ORMs.LinesDetail.line_id == line_id,
                ORMs.LinesDetail.nums > position
            ).update({ORMs.LinesDetail.nums: ORMs.LinesDetail.nums - 1})

            db.commit()
            print("Station removed from line successfully.")
            return {"message": "Station removed from line successfully"}
        else:
            print("Station or line not found OR station not contained in line.")
            return {"error": "Station or line not found OR station not contained in line."}
    except Exception as e:
        db.rollback()
        print(f"Error removing station from line: {e}")
        return {"error": str(e)}
