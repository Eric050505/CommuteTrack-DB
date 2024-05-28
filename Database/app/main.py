from typing import Dict, Any, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models
from .database import SessionLocal, engine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/lines/{line_id}")
def read_line(line_id: int, db: Session = Depends(get_db)):
    db_line = crud.get_line(db, line_id=line_id)
    if db_line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return db_line


@app.get("/price/{start_station}/{end_station}")
def get_two_stations_price(start_station: str, end_station: str, db: Session = Depends(get_db)):
    price = crud.get_price(db, start_station=start_station, end_station=end_station)
    logging.info(f"Price: {price}")
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    price = {'start_station': start_station, 'end_station': end_station, 'price': price}
    return price


@app.get("/adjacent_stations/{line_id}/{station_id}/{n}", response_model=Dict[str, Any])
def get_adjacent_stations(line_id: int, station_id: int, n: int, db: Session = Depends(get_db)):
    stations = crud.get_adjacent_stations(db, line_id=line_id, station_id=station_id, n=n)
    logging.info(f"Stations: {stations}")
    if stations is None:
        raise HTTPException(status_code=404, detail="Adjacent stations not found")
    return stations


@app.get("/unfinished_passenger_rides", response_model=List[Dict[str, Any]])
def read_unfinished_passenger_rides(db: Session = Depends(get_db)):
    rides = crud.get_unfinished_passenger_rides(db)
    if rides is None:
        raise HTTPException(status_code=404, detail="No unfinished passenger rides found")
    return [{"passenger_id": ride.passenger_id, "start_station": ride.start_station, "start_time": ride.start_time} for
            ride in rides]


@app.get("/unfinished_card_rides", response_model=List[Dict[str, Any]])
def read_unfinished_card_rides(db: Session = Depends(get_db)):
    rides = crud.get_unfinished_card_rides(db)
    if rides is None:
        raise HTTPException(status_code=404, detail="No unfinished card rides found")
    return [{"card_code": ride.card_code, "start_station": ride.start_station, "start_time": ride.start_time} for ride
            in rides]


@app.post("/p_board/{passenger_id}/{start_station}", response_model=Dict[str, Any])
def p_board(passenger_id: str, start_station: str, db: Session = Depends(get_db)):
    result = crud.p_board(db, passenger_id, start_station)
    logging.info(f"Stations: {result}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/p_alight/{passenger_id}/{start_station}/{end_station}", response_model=Dict[str, Any])
def p_alight(passenger_id: str, start_station: str, end_station: str, db: Session = Depends(get_db)):
    result = crud.p_alight(db, passenger_id, start_station, end_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/c_board/{card_code}/{start_station}", response_model=Dict[str, Any])
def c_board(card_code: str, start_station: str, db: Session = Depends(get_db)):
    result = crud.c_board(db, card_code, start_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/c_alight/{card_code}/{start_station}/{end_station}", response_model=Dict[str, Any])
def c_alight(card_code: str, start_station: str, end_station: str, db: Session = Depends(get_db)):
    result = crud.c_alight(db, card_code, start_station, end_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
