from pydantic import BaseModel, Field
from typing import Literal, Optional

Pavillon = Literal["Français", "Étranger"]
ResultatFlotteur = Literal[
    "A la dérive", "Assisté", "Au mouillage", "Côte rejointe par ses propres moyens",
    "Difficulté surmontée, reprise de route", "Déséchoué", "Immobilisé dans engin",
    "Inconnu", "Non assisté, cas de fausse alerte", "Non renseigné", "Perdu / Coulé",
    "Remorqué", "Renfloué", "Retrouvé après recherche", "Volé", "Échoué",
]
CategorieFlotteur = Literal["Autre", "Aéronef", "Commerce", "Loisir nautique", "Plaisance", "Pêche"]


class FlotteurBase(BaseModel):
    operation_id: int = Field(..., gt=0)
    numero_ordre: Optional[float] = Field(None, ge=1.0, le=25.0)
    pavillon: Optional[Pavillon] = None
    resultat_flotteur: Optional[ResultatFlotteur] = None
    type_flotteur: Optional[str] = None
    categorie_flotteur: Optional[CategorieFlotteur] = None


class FlotteurCreate(FlotteurBase):
    pass


class FlotteurUpdate(BaseModel):
    numero_ordre: Optional[float] = Field(None, ge=1.0, le=25.0)
    pavillon: Optional[Pavillon] = None
    resultat_flotteur: Optional[ResultatFlotteur] = None
    type_flotteur: Optional[str] = None
    categorie_flotteur: Optional[CategorieFlotteur] = None


class FlotteurRead(BaseModel):
    id: int
    operation_id: int
    numero_ordre: Optional[float] = None
    pavillon: Optional[str] = None
    resultat_flotteur: Optional[str] = None
    type_flotteur: Optional[str] = None
    categorie_flotteur: Optional[str] = None

    model_config = {"from_attributes": True}
