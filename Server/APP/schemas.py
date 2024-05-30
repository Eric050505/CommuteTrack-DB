from typing import Optional

from pydantic import BaseModel


class LineBase(BaseModel):
    line_id: int
    Chinese_name: str
    start_time: str
    end_time: str
    mileage: float
    color: str
    first_opening: str
    intro: str
    url: str
    running_speed: float = float('inf')


class LineCreate(BaseModel):
    chinese_name: str
    start_time: str
    end_time: str
    mileage: float
    color: str
    first_opening: str
    intro: str
    url: str
    running_speed: float


class Line(LineBase):
    line_id: int

    class Config:
        from_attributes = True


class LineUpdate(BaseModel):
    chinese_name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    mileage: Optional[float] = None
    color: Optional[str] = None
    first_opening: Optional[str] = None
    intro: Optional[str] = None
    url: Optional[str] = None
    running_speed: Optional[float] = None


class StationBase(BaseModel):
    chinese_name: str
    english_name: str
    district: str
    intro: str
    status: str


class StationCreate(StationBase):
    chinese_name: str
    english_name: str
    district: str
    intro: str
    status: str


class Station(StationBase):
    station_id: int

    class Config:
        from_attributes = True


class StationUpdate(BaseModel):
    chinese_name: Optional[str] = None
    english_name: Optional[str] = None
    district: Optional[str] = None
    intro: Optional[str] = None
    status: Optional[str] = None


class LinesDetailBase(BaseModel):
    station_id: int
    nums: int


class LinesDetailCreate(LinesDetailBase):
    station_id: int
    nums: int


class LinesDetailUpdate(BaseModel):
    nums: int


class LinesDetail(LinesDetailCreate):
    line_id: int
    station_id: int

    class Config:
        from_attributes = True

