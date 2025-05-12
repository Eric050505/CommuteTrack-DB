from typing import Dict, Any, List, Tuple

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import ORMs, schemas
from .database import SessionLocal, engine
from .CRUD import Update, Delete, Read, Create
import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ORMs.Base.metadata.create_all(bind=engine)

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    now = datetime.datetime.now()
    return {f"message": f"Welcome to SUSTech CS307! {now}"}


@app.get("/lines/{chinese_name}")
async def read_line(chinese_name: str, db: Session = Depends(get_db)):
    db_line = Read.get_line(db, chinese_name=chinese_name)
    if db_line is None:
        raise HTTPException(status_code=404, detail="Line not found")
    return db_line


@app.get("/stations/{english_name}")
async def read_station(english_name: str, db: Session = Depends(get_db)):
    db_station = Read.get_station(db, english_name=english_name)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return db_station


@app.post("/add_line", response_model=Dict[str, Any])
async def add_line(line_create: schemas.LineCreate, db: Session = Depends(get_db)):
    line = Create.add_line(db, line_create)
    if not line:
        raise HTTPException(status_code=400, detail="Error adding line")
    return {"message": f"Line {line.chinese_name} added successfully"}


@app.delete("/delete_line/{line_id}", response_model=Dict[str, Any])
async def delete_line(line_id: int, db: Session = Depends(get_db)):
    chinese_name = Delete.delete_line(db, line_id)
    if not chinese_name:
        raise HTTPException(status_code=400, detail="Error deleting line")
    return {"message": f"Line {chinese_name} deleted successfully"}


@app.put("/modify_line/{line_id}", response_model=Dict[str, Any])
async def modify_line(line_id: int, line_update: schemas.LineUpdate, db: Session = Depends(get_db)):
    line = Update.modify_line(db, line_id, line_update)
    if not line:
        raise HTTPException(status_code=400, detail="Error modifying line")
    return {"message": f"Line {line.line_id} modified successfully"}


@app.post("/add_station", response_model=Dict[str, Any])
async def add_station(station_create: schemas.StationCreate, db: Session = Depends(get_db)):
    station = Create.add_station(db, station_create)
    if not station:
        raise HTTPException(status_code=400, detail="Error adding station")
    return {"message": f"Station {station.english_name} added successfully"}


@app.delete("/delete_station/{station_id}", response_model=Dict[str, Any])
async def delete_station(station_id: int, db: Session = Depends(get_db)):
    english_name = Delete.delete_station(db, station_id)
    if not english_name:
        raise HTTPException(status_code=400, detail="Error deleting station")
    return {"message": f"Station {english_name} deleted successfully"}


@app.put("/modify_station/{station_id}", response_model=Dict[str, Any])
async def modify_station(station_id: int, station_update: schemas.StationUpdate, db: Session = Depends(get_db)):
    station = Update.modify_station(db, station_id, station_update)
    if not station:
        raise HTTPException(status_code=400, detail="Error modifying station")
    return {"message": f"Station {station.station_id} modified successfully"}


@app.post("/place_new_stations/{line_id}", response_model=Dict[str, Any])
async def place_new_stations(line_id: int, stations: List[schemas.LinesDetailCreate], db: Session = Depends(get_db)):
    result = Create.place_new_stations(db, line_id, stations)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/remove_station_in_line/{line_id}/{station_id}", response_model=Dict[str, Any])
async def remove_station_in_line(line_id: int, station_id: int, db: Session = Depends(get_db)):
    result = Delete.remove_station_in_line(db, line_id, station_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/price/{start_station}/{end_station}")
async def read_two_stations_price(start_station: str, end_station: str, db: Session = Depends(get_db)):
    price = Read.get_price(db, start_station=start_station, end_station=end_station)
    logging.info(f"Price: {price}")
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    price = {'start_station': start_station, 'end_station': end_station, 'price': price}
    return price


@app.get("/adjacent_stations/{line_id}/{station_id}/{n}", response_model=Dict[str, Any])
async def read_adj_n_stations(line_id: int, station_id: int, n: int, db: Session = Depends(get_db)):
    stations = Read.get_adjacent_stations(db, line_id=line_id, station_id=station_id, n=n)
    logging.info(f"Stations: {stations}")
    if stations is None:
        raise HTTPException(status_code=404, detail="Adjacent stations not found")
    return stations


@app.get("/unfinished_passenger_rides", response_model=List[Dict[str, Any]])
async def read_unf_p_rides(db: Session = Depends(get_db)):
    rides = Read.get_unfinished_passenger_rides(db)
    if rides is None:
        raise HTTPException(status_code=404, detail="No unfinished passenger rides found")
    return [{"passenger_id": ride.passenger_id, "start_station": ride.start_station, "start_time": ride.start_time} for
            ride in rides]


@app.get("/unfinished_card_rides", response_model=List[Dict[str, Any]])
async def read_unf_c_rides(db: Session = Depends(get_db)):
    rides = Read.get_unfinished_card_rides(db)
    if rides is None:
        raise HTTPException(status_code=404, detail="No unfinished card rides found")
    return [{"card_code": ride.card_code, "start_station": ride.start_station, "start_time": ride.start_time} for ride
            in rides]


@app.post("/p_board/{passenger_id}/{start_station}", response_model=Dict[str, Any])
async def p_board(passenger_id: str, start_station: str, db: Session = Depends(get_db)):
    result = Create.p_board(db, passenger_id, start_station)
    logging.info(f"Stations: {result}")

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/p_alight/{passenger_id}/{start_station}/{end_station}", response_model=Dict[str, Any])
async def p_alight(passenger_id: str, start_station: str, end_station: str, db: Session = Depends(get_db)):
    result = Update.p_alight(db, passenger_id, start_station, end_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/c_board/{card_code}/{start_station}", response_model=Dict[str, Any])
async def c_board(card_code: int, start_station: str, db: Session = Depends(get_db)):
    result = Create.c_board(db, card_code, start_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/c_alight/{card_code}/{start_station}/{end_station}", response_model=Dict[str, Any])
async def c_alight(card_code: int, start_station: str, end_station: str, db: Session = Depends(get_db)):
    result = Update.c_alight(db, card_code, start_station, end_station)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/graph", response_model=Dict[int, List[Tuple[int, int, float]]])
async def read_graph(db: Session = Depends(get_db)):
    graph = Read.get_graph(db)
    return graph


@app.get("/data", response_model=List[Tuple[int, int]])
async def read_lines_d(db: Session = Depends(get_db)):
    data = Read.get_lines_d(db)
    return data


@app.get("/path_least_stations/{start_station}/{end_station}", response_model=Tuple[float, List[int]])
async def read_path_least_stations(start_station: str, end_station: str, db: Session = Depends(get_db)):
    min_dist, shortest_path = Read.get_path_least_stations(db, start_station, end_station)
    if min_dist == float('inf'):
        raise HTTPException(status_code=404, detail="Path not found")
    return min_dist, shortest_path


@app.get("/path_shortest_time/{start_station}/{end_station}", response_model=Tuple[float, List[int]])
async def read_path_shortest_time(start_station: str, end_station: str, db: Session = Depends(get_db)):
    min_dist, shortest_path = Read.get_path_shortest_time(db, start_station, end_station)
    if min_dist == float('inf'):
        raise HTTPException(status_code=404, detail="Path not found")
    return min_dist, shortest_path


@app.post("/add_passenger", response_model=Dict[str, Any])
async def add_passenger(passenger_create: schemas.PassengerCreate, db: Session = Depends(get_db)):
    passenger = Create.add_passenger(db, passenger_create)
    logging.info(f"Passenger: {passenger}")
    if not passenger:
        raise HTTPException(status_code=400, detail="Error adding passenger")
    return {"message": f"Passenger {passenger.name} added successfully"}


@app.post("/add_card", response_model=Dict[str, Any])
async def add_card(card_create: schemas.CardCreate, db: Session = Depends(get_db)):
    card = Create.add_card(db, card_create)
    if not card:
        raise HTTPException(status_code=400, detail="Error adding card")
    return {"message": f"Card {card.code} added successfully"}


@app.get("/user/{user_name}")
async def read_user(user_name: str, db: Session = Depends(get_db)):
    db_user = Read.get_user(db, user_name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/add_user", response_model=Dict[str, Any])
async def add_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    user = Create.add_user(db, user_create)
    if not user:
        raise HTTPException(status_code=400, detail="Error adding user")
    return {"message": f"User {user.user_name} added successfully"}


@app.post("/modify_user/{user_name}", response_model=Dict[str, Any])
async def modify_user(user_name: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = Update.modify_user(db, user_name, user_update)
    if not user:
        raise HTTPException(status_code=400, detail="Error modify user")
    return {"message": f"User {user.user_name} modified successfully"}


@app.delete("/delete_user/{user_name}", response_model=Dict[str, Any])
async def delete_user(user_name: str, user_delete: schemas.UserDelete, db: Session = Depends(get_db)):
    user_name = Delete.delete_user(db, user_name, user_delete)
    if not user_name:
        raise HTTPException(status_code=400, detail="Error deleting user")
    return {"message": f"User {user_name} deleted successfully"}


@app.get("/passenger_ride/{passenger_id}")
async def read_passenger(passenger_id: str, p_search: schemas.PassengerSearch, db: Session = Depends(get_db)):
    db_passenger_ride = Read.get_passenger_ride(db, passenger_id, p_search)
    if db_passenger_ride is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_passenger_ride


@app.get("/card_ride/{card_code}")
async def read_card(card_code: int, c_search: schemas.CardSearch, db: Session = Depends(get_db)):
    db_card_ride = Read.get_card_ride(db, card_code, c_search)
    if db_card_ride is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return db_card_ride


@app.get("/cards/{card_code}")
def read_card(card_code: int, db: Session = Depends(get_db)):
    db_card = Read.get_card(db, card_code=card_code)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Cards not found")
    return db_card


@app.get("/passengers/{id_number}")
def read_passenger(id_number: str, db: Session = Depends(get_db)):
    db_passenger = Read.get_passenger(db, id_number=id_number)
    if db_passenger is None:
        raise HTTPException(status_code=404, detail="Passengers not found")
    return db_passenger
