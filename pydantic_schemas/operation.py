from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional
from datetime import datetime

from pydantic_schemas.flotteur import FlotteurRead
from pydantic_schemas.humain_result import HumainResultRead
from pydantic_schemas.operation_stats import OperationStatsRead


DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

TypeOperation = Literal["DIV", "MAS", "SAR", "SUR"]
PourquoiAlerte = Literal[
    "Autre", "Autre signal réglementaire", "Balise 121,5 - 243", "Balise 406",
    "IMMARSAT", "IMMARSAT A", "IMMARSAT C", "Inquiétude",
    "Signal pyrotechnique", "Signal radio-électrique", "Événement reconnu",
]
CategorieQuiAlerte = Literal[
    "Autorité civile française à terre", "Autorité maritime française à terre",
    "Autorité militaire française à terre", "Autorité étrangère",
    "Aéronef", "Navire à la mer", "Organisme ou personne privée",
]
CrossName = Literal[
    "Adge", "Antilles-Guyane", "Corse", "Corsen", "Gris-Nez", "Guadeloupe",
    "Guyane", "Jobourg", "La Garde", "La Réunion", "Martinique", "Mayotte",
    "Nouvelle-Calédonie", "Polynésie", "Soulac", "Sud océan Indien", "Étel",
]
CategorieEvenement = Literal[
    "Accidents de navire", "Accidents individuels à personnes",
    "Accidents individuels à personnes embarquées",
    "Accidents individuels à personnes non embarquées",
    "Autres affaires nécessitant opération",
    "Avaries non suivies d'accident navire", "Fausses alertes",
]
Autorite = Literal[
    "Affaires maritimes", "Autorité portuaire", "Autorité étrangère", "Autre",
    "CROSS ou sous-CROSS", "MRCC étranger", "Maire", "Préfet maritime",
    "RCC - RSC français", "RCC - RSC étrangers", "Représentant du gouvernement", "SG-Mer",
]
ZoneResponsabilite = Literal[
    "Eaux territoriales", "Hors responsabilité", "Plage et 300 mètres",
    "Plan eau salée", "Port et accès", "Responsabilité française",
    "Responsabilité étrangère", "Terrestre",
]
VentDirectionCategorie = Literal["est", "nord", "nord-est", "nord-ouest", "ouest", "sud", "sud-est", "sud-ouest"]
FuseauHoraire = Literal[
    "America/Cayenne", "America/Guadeloupe", "America/Guyana", "America/Martinique",
    "Europe/Paris", "Indian/Mayotte", "Indian/Reunion", "Pacific/Noumea", "Pacific/Tahiti",
]
SystemeSource = Literal["seamis_json", "secmarweb"]


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.strptime(value, DATETIME_FMT)
    except ValueError:
        raise ValueError(f"Expected datetime format 'YYYY-MM-DD HH:MM:SS', got '{value}'")


class OperationBase(BaseModel):
    type_operation: Optional[TypeOperation] = None
    pourquoi_alerte: Optional[PourquoiAlerte] = None
    moyen_alerte: Optional[str] = None
    qui_alerte: Optional[str] = None
    categorie_qui_alerte: Optional[CategorieQuiAlerte] = None
    cross: Optional[CrossName] = None
    departement: Optional[str] = None
    est_metropolitain: Optional[bool] = None
    evenement: Optional[str] = None
    categorie_evenement: Optional[CategorieEvenement] = None
    autorite: Optional[Autorite] = None
    zone_responsabilite: Optional[ZoneResponsabilite] = None
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    vent_direction: Optional[float] = Field(None, ge=0.0, le=360.0, description="Wind direction in degrees")
    vent_direction_categorie: Optional[VentDirectionCategorie] = None
    vent_force: Optional[float] = Field(None, ge=0.0, le=12.0, description="Beaufort scale 0-12")
    mer_force: Optional[float] = Field(None, ge=0.0, le=9.0, description="Douglas sea scale 0-9")
    date_heure_reception_alerte: Optional[str] = None
    date_heure_fin_operation: Optional[str] = None
    numero_sitrep: Optional[int] = Field(None, ge=0)
    fuseau_horaire: Optional[FuseauHoraire] = None
    systeme_source: Optional[SystemeSource] = None

    @field_validator("date_heure_reception_alerte", "date_heure_fin_operation", mode="before")
    @classmethod
    def validate_datetime_format(cls, v: Optional[str]) -> Optional[str]:
        _parse_dt(v)  # raises if invalid
        return v

    @model_validator(mode="after")
    def validate_dates_order(self) -> "OperationBase":
        start = _parse_dt(self.date_heure_reception_alerte)
        end = _parse_dt(self.date_heure_fin_operation)
        if start and end and start >= end:
            raise ValueError(
                "date_heure_reception_alerte must be strictly before date_heure_fin_operation"
            )
        return self


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass


class OperationRead(BaseModel):
    operation_id: int
    type_operation: Optional[str] = None
    pourquoi_alerte: Optional[str] = None
    moyen_alerte: Optional[str] = None
    qui_alerte: Optional[str] = None
    categorie_qui_alerte: Optional[str] = None
    cross: Optional[str] = None
    departement: Optional[str] = None
    est_metropolitain: Optional[bool] = None
    evenement: Optional[str] = None
    categorie_evenement: Optional[str] = None
    autorite: Optional[str] = None
    zone_responsabilite: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    vent_direction: Optional[float] = None
    vent_direction_categorie: Optional[str] = None
    vent_force: Optional[float] = None
    mer_force: Optional[float] = None
    date_heure_reception_alerte: Optional[str] = None
    date_heure_fin_operation: Optional[str] = None
    numero_sitrep: Optional[int] = None
    fuseau_horaire: Optional[str] = None
    systeme_source: Optional[str] = None


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass


class OperationRead(OperationBase):
    operation_id: int

    model_config = {"from_attributes": True, "ser_json_inf_nan": 'null'}
    

class OperationReadFull(OperationRead):
    operations_stats: List[OperationStatsRead] = []
    human_results: List[HumainResultRead] = []
    flotteurs: List[FlotteurRead] = []
    model_config = {"from_attributes": True}
