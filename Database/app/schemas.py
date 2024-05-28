from pydantic import BaseModel


class LineBase(BaseModel):
    Chinese_name: str
    start_time: str
    end_time: str
    mileage: float
    color: str
    first_opening: str
    intro: str
    url: str
    running_speed: float = None


class LineCreate(LineBase):
    pass


class Line(LineBase):
    line_id: int

    class Config:
        from_attributes = True


class StationBase(BaseModel):
    Chinese_name: str
    English_name: str
    district: str
    intro: str
    status: str


class StationCreate(StationBase):
    pass


class Station(StationBase):
    station_id: int

    class Config:
        from_attributes = True


class PriceBase(BaseModel):
    start_station_id: int
    end_station_id: int
    price: int


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    class Config:
        from_attributes = True
