from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

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


class HumainResultBase(BaseModel):
    operation_id: int = Field(..., gt=0)
    categorie_personne: Optional[CategoriePersonne] = None
    resultat_humain: Optional[ResultatHumain] = None
    nombre: int = Field(..., ge=0)
    dont_nombre_blesse: int = Field(..., ge=0)

    @model_validator(mode="after")
    def blesse_lte_nombre(self) -> "HumainResultBase":
        if self.dont_nombre_blesse > self.nombre:
            raise ValueError(
                f"dont_nombre_blesse ({self.dont_nombre_blesse}) cannot exceed nombre ({self.nombre})"
            )
        return self


class HumainResultCreate(HumainResultBase):
    pass


class HumainResultUpdate(BaseModel):
    categorie_personne: Optional[CategoriePersonne] = None
    resultat_humain: Optional[ResultatHumain] = None
    nombre: Optional[int] = Field(None, ge=0)
    dont_nombre_blesse: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def blesse_lte_nombre(self) -> "HumainResultUpdate":
        if self.nombre is not None and self.dont_nombre_blesse is not None:
            if self.dont_nombre_blesse > self.nombre:
                raise ValueError(
                    f"dont_nombre_blesse ({self.dont_nombre_blesse}) cannot exceed nombre ({self.nombre})"
                )
        return self


class HumainResultRead(BaseModel):
    id: int
    operation_id: int
    categorie_personne: Optional[str] = None
    resultat_humain: Optional[str] = None
    nombre: int
    dont_nombre_blesse: int

    model_config = {"from_attributes": True}
