from sqlalchemy import Table, MetaData

from .database import Base, engine

metadata = MetaData()

bus_info_table = Table('bus_info', metadata, autoload_with=engine)
card_ride_table = Table('card_ride', metadata, autoload_with=engine)
cards_table = Table('cards', metadata, autoload_with=engine)
lines_table = Table('lines', metadata, autoload_with=engine)
lines_detail_table = Table('lines_detail', metadata, autoload_with=engine)
out_info_table = Table('out_info', metadata, autoload_with=engine)
passenger_table = Table('passenger', metadata, autoload_with=engine)
passenger_ride_table = Table('passenger_ride', metadata, autoload_with=engine)
price_table = Table('price', metadata, autoload_with=engine)
stations_table = Table('stations', metadata, autoload_with=engine)
user_identity_table = Table('user_identity', metadata, autoload_with=engine)


class BusInfo(Base):
    __table__ = bus_info_table


class OutInfo(Base):
    __table__ = out_info_table


class CardRide(Base):
    __table__ = card_ride_table


class Cards(Base):
    __table__ = cards_table


class Line(Base):
    __table__ = lines_table


class LinesDetail(Base):
    __table__ = lines_detail_table


class Passenger(Base):
    __table__ = passenger_table


class PassengerRide(Base):
    __table__ = passenger_ride_table


class Price(Base):
    __table__ = price_table


class Stations(Base):
    __table__ = stations_table


class UserIdentity(Base):
    __table__ = user_identity_table
