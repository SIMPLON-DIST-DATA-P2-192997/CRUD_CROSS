from pydantic import BaseModel
from typing import Optional


class FlotteurBase(BaseModel):
    operation_id: int
    numero_ordre: Optional[float] = None
    pavillon: Optional[str] = None
    resultat_flotteur: Optional[str] = None
    type_flotteur: Optional[str] = None
    categorie_flotteur: Optional[str] = None
    numero_immatriculation: Optional[str] = None


class FlotteurCreate(FlotteurBase):
    pass


class FlotteurUpdate(BaseModel):
    numero_ordre: Optional[float] = None
    pavillon: Optional[str] = None
    resultat_flotteur: Optional[str] = None
    type_flotteur: Optional[str] = None
    categorie_flotteur: Optional[str] = None
    numero_immatriculation: Optional[str] = None


class FlotteurRead(FlotteurBase):
    id: int

    model_config = {"from_attributes": True}
