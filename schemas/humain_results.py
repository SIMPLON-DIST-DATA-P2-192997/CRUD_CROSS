import pandera.pandas as pa
from pandera.typing import Series


CATEGORIES_PERSONNE = [
    "Autre", "Clandestin", "Commerce français", "Marin étranger", "Migrant",
    "Plaisancier français", "Pratiquant loisirs nautiques", "Pêcheur amateur",
    "Pêcheur français", "Toutes catégories",
]
RESULTATS_HUMAIN = [
    "Inconnu", "Personne assistée", "Personne blessée", "Personne disparue",
    "Personne décédée", "Personne décédée accidentellement", "Personne décédée naturellement",
    "Personne impliquée dans fausse alerte", "Personne indemne", "Personne malade",
    "Personne retrouvée", "Personne secourue", "Personne tirée d'affaire seule",
]


class HumainResultSchema(pa.DataFrameModel):
    operation_id: Series[int]
    categorie_personne: Series[str] = pa.Field(nullable=True, isin=CATEGORIES_PERSONNE)
    resultat_humain: Series[str] = pa.Field(nullable=True, isin=RESULTATS_HUMAIN)
    nombre: Series[int] = pa.Field(ge=0)
    dont_nombre_blesse: Series[int] = pa.Field(ge=0)

    class Config(pa.DataFrameModel.Config):
        coerce = True
        name = "HumainResultSchema"
