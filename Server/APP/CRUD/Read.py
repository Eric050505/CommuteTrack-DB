import heapq
from collections import defaultdict
import logging

from sqlalchemy.orm import Session
from .. import ORMs
from .. import schemas


def get_line(db: Session, chinese_name: str):
    return db.query(ORMs.Line).filter(ORMs.Line.chinese_name == chinese_name).first()


def get_card(db: Session, card_code: int):
    return db.query(ORMs.Cards).filter(ORMs.Cards.code == card_code).first()


def get_passenger(db: Session, id_number: str):
    return db.query(ORMs.Passenger).filter(ORMs.Passenger.id_number == id_number).first()


def get_station(db: Session, english_name: str):
    return db.query(ORMs.Stations).filter(ORMs.Stations.english_name == english_name).first()


def get_user(db: Session, user_name: str):
    return db.query(ORMs.UserIdentity).filter(ORMs.UserIdentity.user_name == user_name).first()


def get_price(db: Session, start_station: str, end_station: str):
    try:
        start_station_id = db.query(ORMs.Stations.station_id).filter(
            ORMs.Stations.english_name == start_station).scalar()
        logging.info(f"Start station ID: {start_station_id}")
        end_station_id = db.query(ORMs.Stations.station_id).filter(
            ORMs.Stations.english_name == end_station).scalar()
        logging.info(f"End station ID: {end_station_id}")

        if start_station_id is None or end_station_id is None:
            logging.warning("One of the stations was not found.")
            return None

        result = (
            db.query(ORMs.Price.price)
            .filter(ORMs.Price.start_station_id == start_station_id)
            .filter(ORMs.Price.end_station_id == end_station_id)
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
        station = db.query(ORMs.Stations).filter(ORMs.Stations.station_id == station_id).first()
        logging.info(f"Start station ID: {station.english_name}")

        if not station:
            logging.warning(f"Station with id {station_id} not found.")
            return None
        english_name = station.english_name
        line_detail = db.query(ORMs.LinesDetail).filter(ORMs.LinesDetail.line_id == line_id,
                                                        ORMs.LinesDetail.station_id == station_id).first()
        if not line_detail:
            logging.warning(f"Line detail for line_id {line_id} and station_id {station_id} not found.")
            return None
        nums = line_detail.nums

        results = db.query(ORMs.Stations.chinese_name, ORMs.Stations.english_name).distinct() \
            .join(ORMs.LinesDetail, ORMs.LinesDetail.station_id == ORMs.Stations.station_id) \
            .filter(ORMs.LinesDetail.line_id == line_id) \
            .filter((ORMs.LinesDetail.nums == nums - n) | (ORMs.LinesDetail.nums == nums + n)).all()

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
            ORMs.PassengerRide.passenger_id,
            ORMs.PassengerRide.start_station,
            ORMs.PassengerRide.start_time
        ).filter(ORMs.PassengerRide.end_time == None).all()  # SQLAlchemy uses 'None' for NULL

        return unfinished_rides
    except Exception as e:
        logging.error(f"Error querying unfinished passenger rides: {e}")
        return None


def get_unfinished_card_rides(db: Session):
    try:
        unfinished_rides = db.query(
            ORMs.CardRide.card_code,
            ORMs.CardRide.start_station,
            ORMs.CardRide.start_time
        ).filter(ORMs.CardRide.end_time == None).all()  # SQLAlchemy uses 'None' for NULL

        return unfinished_rides
    except Exception as e:
        logging.error(f"Error querying unfinished card rides: {e}")
        return None


def get_graph(db: Session):
    speed = {}
    graph = defaultdict(list)

    result = db.query(ORMs.Line.line_id, ORMs.Line.running_speed).all()
    for line_id, running_speed in result:
        speed[line_id] = float(running_speed)

    data = tuple(get_lines_d(db))
    for i in range(len(data) - 1):
        this_line = data[i][0]
        next_line = data[i + 1][0]
        if this_line == next_line:
            if not (this_line, data[i + 1][1], speed[this_line]) in graph[data[i][1]]:
                graph[data[i][1]].append((this_line, data[i + 1][1], speed[this_line]))
            if not (this_line, data[i][1], speed[this_line]) in graph[data[i + 1][1]]:
                graph[data[i + 1][1]].append((this_line, data[i][1], speed[this_line]))

    return graph


def get_lines_d(db: Session):
    return db.query(ORMs.LinesDetail.line_id, ORMs.LinesDetail.station_id).join(ORMs.Stations,
                                                                                ORMs.LinesDetail.station_id == ORMs.Stations.station_id).filter(
        ORMs.Stations.status == 'running')


def get_path_least_stations(db: Session, start_station: str, end_station: str):
    start_station_id = \
        db.query(ORMs.Stations.station_id).filter(ORMs.Stations.english_name == start_station).first()[0]
    end_station_id = db.query(ORMs.Stations.station_id).filter(ORMs.Stations.english_name == end_station).first()[0]

    graph = get_graph(db)
    min_dist, shortest_path = dijkstra_single(graph, start_station_id, end_station_id)
    return min_dist, shortest_path


def get_path_shortest_time(db: Session, start_station: str, end_station: str):
    start_station_id = \
        db.query(ORMs.Stations.station_id).filter(ORMs.Stations.english_name == start_station).first()[0]
    end_station_id = db.query(ORMs.Stations.station_id).filter(ORMs.Stations.english_name == end_station).first()[0]

    graph = get_graph(db)
    data = get_lines_d(db)
    min_dist, shortest_path = dijkstra_time(graph, data, start_station_id, end_station_id)
    return min_dist, shortest_path


def dijkstra_time(graph, data, start_station_id, end_station_id):
    shortest_path = []
    queue = [(0, start_station_id, shortest_path)]
    visited = set()
    min_dist = {start_station_id: 0}

    while queue:
        cost, curr_station_id, path = heapq.heappop(queue)
        if curr_station_id in visited:
            continue
        path = path + [curr_station_id]
        visited.add(curr_station_id)
        if curr_station_id == end_station_id:
            return cost, path
        for adjacent in graph[curr_station_id]:
            weight = adjacent[2]
            adjacent_id = adjacent[1]
            if adjacent_id in visited:
                continue
            prev_cost = min_dist.get(adjacent_id, float('inf'))
            next_cost = cost + weight
            if data[curr_station_id][0] != data[adjacent_id][0]:
                next_cost += 3
            if next_cost < prev_cost:
                min_dist[adjacent_id] = next_cost
                heapq.heappush(queue, (next_cost, adjacent_id, path))

    if not shortest_path:
        return float('inf'), []
    else:
        return min_dist[start_station_id], shortest_path


def dijkstra_single(graph, start_station_id, end_station_id):
    shortest_path = []
    queue = [(0, start_station_id, shortest_path)]
    visited = set()
    min_dist = {start_station_id: 0}

    while queue:
        cost, curr_station_id, path = heapq.heappop(queue)
        if curr_station_id in visited:
            continue
        path = path + [curr_station_id]
        visited.add(curr_station_id)
        if curr_station_id == end_station_id:
            return cost, path
        for adjacent in graph[curr_station_id]:
            adjacent = adjacent[1]
            if adjacent in visited:
                continue
            prev_cost = min_dist.get(adjacent, float('inf'))
            next_cost = cost + 1
            if next_cost < prev_cost:
                min_dist[adjacent] = next_cost
                heapq.heappush(queue, (next_cost, adjacent, path))

    if not shortest_path:
        return float('inf'), []
    else:
        return min_dist[start_station_id], shortest_path


def get_passenger_ride(db: Session, passenger_id: str, p_search: schemas.PassengerSearch):
    query = db.query(ORMs.PassengerRide).filter(ORMs.PassengerRide.passenger_id == passenger_id)

    if p_search.start_station is not None:
        query = query.filter(ORMs.PassengerRide.start_station == p_search.start_station)
    if p_search.end_station is not None:
        query = query.filter(ORMs.PassengerRide.end_station == p_search.end_station)
    if p_search.price is not None:
        query = query.filter(ORMs.PassengerRide.price == p_search.price)
    if p_search.start_time is not None:
        query = query.filter(ORMs.PassengerRide.start_time >= p_search.start_time)
    if p_search.end_time is not None:
        query = query.filter(ORMs.PassengerRide.end_time <= p_search.end_time)

    records = query.all()
    logging.info(f"{len(records)} passengers records found")

    if not records:
        logging.warning(f"Ride not found.")
        return None
    else:
        return records


def get_card_ride(db: Session, card_cord: int, c_search: schemas.CardSearch):
    query = db.query(ORMs.CardRide).filter(ORMs.CardRide.card_code == card_cord)

    if c_search.start_station is not None:
        query = query.filter(ORMs.CardRide.start_station == c_search.start_station)
    if c_search.end_station is not None:
        query = query.filter(ORMs.CardRide.end_station == c_search.end_station)
    if c_search.price is not None:
        query = query.filter(ORMs.CardRide.price == c_search.price)
    if c_search.start_time is not None:
        query = query.filter(ORMs.CardRide.start_time >= c_search.start_time)
    if c_search.end_time is not None:
        query = query.filter(ORMs.CardRide.end_time <= c_search.end_time)

    records = query.all()
    logging.info(f"{len(records)} card records found")

    if not records:
        logging.warning(f"Ride not found.")
        return None
    else:
        return records
