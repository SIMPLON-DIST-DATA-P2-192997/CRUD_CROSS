from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, List, Optional
from datetime import datetime

DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


Pavillon = Literal["Français", "Étranger"]
ResultatFlotteur = Literal[
    "A la dérive", "Assisté", "Au mouillage", "Côte rejointe par ses propres moyens",
    "Difficulté surmontée, reprise de route", "Déséchoué", "Immobilisé dans engin",
    "Inconnu", "Non assisté, cas de fausse alerte", "Non renseigné", "Perdu / Coulé",
    "Remorqué", "Renfloué", "Retrouvé après recherche", "Volé", "Échoué",
]
CategorieFlotteur = Literal["Autre", "Aéronef", "Commerce", "Loisir nautique", "Plaisance", "Pêche"]
CategoriePersonne = Literal[
    "Autre", "Clandestin", "Commerce français", "Marin étranger", "Migrant",
    "Plaisancier français", "Pratiquant loisirs nautiques", "Pêcheur amateur",
    "Pêcheur français", "Toutes catégories",
]
ResultatHumain = Literal[
    "Inconnu", "Personne assistée", "Personne blessée", "Personne disparue",
    "Personne décédée", "Personne décédée accidentellement", "Personne décédée naturellement",
    "Personne impliquée dans fausse alerte", "Personne indemne", "Personne malade",
    "Personne retrouvée", "Personne secourue", "Personne tirée d'affaire seule",
]


class FloatInput(BaseModel):
    order_number: Optional[str] = None
    flag: Optional[Pavillon] = None
    type: Optional[str] = None
    float_state: Optional[ResultatFlotteur] = None
    category: Optional[CategorieFlotteur] = None


class HumanResInput(BaseModel):
    personn_category: Optional[CategoriePersonne] = None
    number: str
    result: Optional[ResultatHumain] = None

    @field_validator("number", mode="before")
    @classmethod
    def number_must_be_parseable_int(cls, v: str) -> str:
        try:
            if int(str(v).strip()) < 0:
                raise ValueError("number must be >= 0")
        except (ValueError, TypeError):
            raise ValueError(f"'number' must be a non-negative integer string, got '{v}'")
        return v


class OperationIngestInput(BaseModel):
    model_config = {"extra": "ignore"}

    op_operation_type: Optional[str] = Field(None, max_length=10)
    op_cause: Optional[str] = None
    op_means: Optional[str] = None
    op_author: Optional[str] = None
    op_author_category: Optional[str] = None
    op_cross: Optional[str] = None
    pa_depts: Optional[str] = Field(None, max_length=3)
    op_is_metro: Optional[bool] = None
    op_event: Optional[str] = None
    op_event_category: Optional[str] = None
    op_authority: Optional[str] = None
    op_responsability_zone: Optional[str] = None
    pa_lat: Optional[str] = None
    pa_lng: Optional[str] = None
    pa_wind_direction: Optional[str] = None
    pa_wind_strength: Optional[float] = Field(None, ge=0.0, le=12.0, description="Beaufort scale 0-12")
    pa_sea_strength: Optional[float] = Field(None, ge=0.0, le=9.0, description="Douglas sea scale 0-9")
    pa_start_date: Optional[str] = None
    pa_end_date: Optional[str] = None
    pa_time_zone: Optional[str] = None
    pa_system: Optional[str] = None
    floats: List[FloatInput] = []
    human_res: List[HumanResInput] = []

    @field_validator("pa_lat", mode="before")
    @classmethod
    def validate_lat(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            val = float(v)
        except (ValueError, TypeError):
            raise ValueError(f"pa_lat must be a numeric string, got '{v}'")
        if not -90.0 <= val <= 90.0:
            raise ValueError(f"pa_lat must be between -90 and 90, got {val}")
        return v

    @field_validator("pa_lng", mode="before")
    @classmethod
    def validate_lng(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            val = float(v)
        except (ValueError, TypeError):
            raise ValueError(f"pa_lng must be a numeric string, got '{v}'")
        if not -180.0 <= val <= 180.0:
            raise ValueError(f"pa_lng must be between -180 and 180, got {val}")
        return v

    @field_validator("pa_start_date", "pa_end_date", mode="before")
    @classmethod
    def validate_datetime_format(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            datetime.strptime(v, DATETIME_FMT)
        except ValueError:
            raise ValueError(f"Expected datetime format 'YYYY-MM-DD HH:MM:SS', got '{v}'")
        return v

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
            return datetime.strptime(value, DATETIME_FMT)
        except ValueError:
            return None
