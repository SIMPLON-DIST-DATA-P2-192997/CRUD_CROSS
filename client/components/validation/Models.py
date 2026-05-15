from pydantic import BaseModel, Field
from schemas import operations
from enum import Enum
from typing import Optional, Union
import datetime

OperationtypeEnum = Enum('OperationtypeEnum', {v:v for v in operations.TYPES_OPERATION})

class FloatSchema(BaseModel):
  order_number: int
  flag: str
  float_state: str
  type: Optional[str] = None
  category: str
  immatriculation: Optional[str] = None
  
class OperationSchema(BaseModel):
  op_operation_type: str
  op_cause: Optional[str] = None
  op_means: Optional[str] = None
  op_author: Optional[str] = None
  op_cross: str
  op_author_category: str
  op_event: str
  op_event_category: str
  op_authority: str
  op_second_authority: Optional[str] = None
  op_responsability_zone: str
  op_is_metro: bool
  

class ParametersSchema(BaseModel):
  pa_start_date: datetime.datetime
  pa_end_date: datetime.datetime
  pa_lat: float = Field(ge=-90, le=90)
  pa_lng: float = Field(ge=-180, le=180)
  pa_wind_direction: Union[int|float] = Field(ge=0, le=360)
  pa_wind_strength: int = Field(ge=0, le=12)
  pa_deps: Union[str|int] = None
  pa_time_zone: str
  pa_sea_strength: int = Field(ge=0, le=9)
  
class HumanResultSchema(BaseModel):
  personn_category: str
  result: str
  number: int
  