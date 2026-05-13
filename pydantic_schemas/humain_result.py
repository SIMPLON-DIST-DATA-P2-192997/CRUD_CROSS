from pydantic import BaseModel
from typing import Optional


class HumainResultBase(BaseModel):
    operation_id: int
    categorie_personne: Optional[str] = None
    resultat_humain: Optional[str] = None
    nombre: int
    dont_nombre_blesse: int


class HumainResultCreate(HumainResultBase):
    pass


class HumainResultUpdate(BaseModel):
    categorie_personne: Optional[str] = None
    resultat_humain: Optional[str] = None
    nombre: Optional[int] = None
    dont_nombre_blesse: Optional[int] = None


class HumainResultRead(HumainResultBase):
    id: int

    model_config = {"from_attributes": True}
