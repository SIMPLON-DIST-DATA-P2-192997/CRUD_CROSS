import pandera.pandas as pa
from pandera.typing import Series


PAVILLONS = ["Français", "Étranger"]
RESULTATS_FLOTTEUR = [
    "A la dérive", "Assisté", "Au mouillage", "Côte rejointe par ses propres moyens",
    "Difficulté surmontée, reprise de route", "Déséchoué", "Immobilisé dans engin",
    "Inconnu", "Non assisté, cas de fausse alerte", "Non renseigné", "Perdu / Coulé",
    "Remorqué", "Renfloué", "Retrouvé après recherche", "Volé", "Échoué",
]
CATEGORIES_FLOTTEUR = ["Autre", "Aéronef", "Commerce", "Loisir nautique", "Plaisance", "Pêche"]


class FlotteurSchema(pa.DataFrameModel):
    operation_id: Series[int]
    numero_ordre: Series[float] = pa.Field(nullable=True, ge=1, le=25)
    pavillon: Series[str] = pa.Field(nullable=True, isin=PAVILLONS)
    resultat_flotteur: Series[str] = pa.Field(nullable=True, isin=RESULTATS_FLOTTEUR)
    type_flotteur: Series[str] = pa.Field(nullable=True)
    categorie_flotteur: Series[str] = pa.Field(nullable=True, isin=CATEGORIES_FLOTTEUR)

    class Config(pa.DataFrameModel.Config):
        coerce = True
        name = "FlotteurSchema"
