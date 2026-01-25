from datetime import datetime

from pydantic import BaseModel

from src.constants import City


class Meta(BaseModel):
    actual_at: datetime
    total_items: int


class SalaryIndexByCity(BaseModel):
    city: City
    net_salary: int
    price_per_sqm: int
    cool_index: float
    cool_group: str
    months_per_sqm: float


class SalaryIndexResponse(BaseModel):
    meta: Meta
    main: SalaryIndexByCity
    other: list[SalaryIndexByCity]
