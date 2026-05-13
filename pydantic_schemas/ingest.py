from pydantic import BaseModel, model_validator
from typing import Optional, List
from datetime import datetime


class FloatInput(BaseModel):
    order_number: Optional[str] = None
    flag: Optional[str] = None
    type: Optional[str] = None
    float_state: Optional[str] = None
    category: Optional[str] = None
    immatriculation: Optional[str] = None


class HumanResInput(BaseModel):
    personn_category: Optional[str] = None
    number: str
    result: Optional[str] = None


class OperationIngestInput(BaseModel):
    model_config = {"extra": "ignore"}

    op_operation_type: Optional[str] = None
    op_cause: Optional[str] = None
    op_means: Optional[str] = None
    op_author: Optional[str] = None
    op_author_category: Optional[str] = None
    op_cross: Optional[str] = None
    pa_depts: Optional[str] = None
    op_is_metro: Optional[bool] = None
    op_event: Optional[str] = None
    op_event_category: Optional[str] = None
    op_authority: Optional[str] = None
    op_second_authority: Optional[str] = None
    op_responsability_zone: Optional[str] = None
    pa_lat: Optional[str] = None
    pa_lng: Optional[str] = None
    pa_wind_direction: Optional[str] = None
    pa_wind_strength: Optional[float] = None
    pa_sea_strength: Optional[float] = None
    pa_start_date: Optional[str] = None
    pa_end_date: Optional[str] = None
    pa_time_zone: Optional[str] = None
    pa_system: Optional[str] = None
    floats: List[FloatInput] = []
    human_res: List[HumanResInput] = []

    @model_validator(mode="after")
    def check_dates(self) -> "OperationIngestInput":
        start = self.parse_date(self.pa_start_date)
        end = self.parse_date(self.pa_end_date)
        if start is not None and end is not None and start >= end:
            raise ValueError("pa_start_date must be strictly before pa_end_date")
        return self

    def parse_date(self, value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
