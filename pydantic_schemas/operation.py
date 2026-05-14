from pydantic import BaseModel
from typing import Optional
from .operation_stats import OperationStatsRead
from .humain_result import HumainResultRead
from .flotteur import FlotteurRead
from typing import List


class OperationBase(BaseModel):
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
    seconde_autorite: Optional[str] = None
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
    cross_sitrep: Optional[str] = None
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
