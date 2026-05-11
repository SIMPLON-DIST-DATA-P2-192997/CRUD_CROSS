import pandera.pandas as pa
from pandera.typing import Series


TYPES_OPERATION = ["DIV", "MAS", "SAR", "SUR"]
POURQUOI_ALERTE = [
    "Autre", "Autre signal réglementaire", "Balise 121,5 - 243", "Balise 406",
    "IMMARSAT", "IMMARSAT A", "IMMARSAT C", "Inquiétude",
    "Signal pyrotechnique", "Signal radio-électrique", "Événement reconnu",
]
CATEGORIES_QUI_ALERTE = [
    "Autorité civile française à terre", "Autorité maritime française à terre",
    "Autorité militaire française à terre", "Autorité étrangère",
    "Aéronef", "Navire à la mer", "Organisme ou personne privée",
]
CROSS_LIST = [
    "Adge", "Antilles-Guyane", "Corse", "Corsen", "Gris-Nez", "Guadeloupe",
    "Guyane", "Jobourg", "La Garde", "La Réunion", "Martinique", "Mayotte",
    "Nouvelle-Calédonie", "Polynésie", "Soulac", "Sud océan Indien", "Étel",
]
CATEGORIES_EVENEMENT = [
    "Accidents de navire", "Accidents individuels à personnes",
    "Accidents individuels à personnes embarquées",
    "Accidents individuels à personnes non embarquées",
    "Autres affaires nécessitant opération",
    "Avaries non suivies d'accident navire", "Fausses alertes",
]
AUTORITES = [
    "Affaires maritimes", "Autorité portuaire", "Autorité étrangère", "Autre",
    "CROSS ou sous-CROSS", "MRCC étranger", "Maire", "Préfet maritime",
    "RCC - RSC français", "RCC - RSC étrangers", "Représentant du gouvernement", "SG-Mer",
]
SECONDES_AUTORITES = [
    "Autorité portuaire", "Autre", "CROSS ou sous-CROSS", "MRCC étranger",
    "Maire", "Préfet maritime", "RCC - RSC français", "RCC - RSC étrangers",
]
ZONES_RESPONSABILITE = [
    "Eaux territoriales", "Hors responsabilité", "Plage et 300 mètres",
    "Plan eau salée", "Port et accès", "Responsabilité française",
    "Responsabilité étrangère", "Terrestre",
]
DIRECTIONS_VENT = ["est", "nord", "nord-est", "nord-ouest", "ouest", "sud", "sud-est", "sud-ouest"]
FUSEAUX_HORAIRES = [
    "America/Cayenne", "America/Guadeloupe", "America/Guyana", "America/Martinique",
    "Europe/Paris", "Indian/Mayotte", "Indian/Reunion", "Pacific/Noumea", "Pacific/Tahiti",
]
SYSTEMES_SOURCE = ["seamis_json", "secmarweb"]


class OperationSchema(pa.DataFrameModel):
    operation_id: Series[int]
    type_operation: Series[str] = pa.Field(nullable=True, isin=TYPES_OPERATION)
    pourquoi_alerte: Series[str] = pa.Field(nullable=True, isin=POURQUOI_ALERTE)
    moyen_alerte: Series[str] = pa.Field(nullable=True)
    qui_alerte: Series[str] = pa.Field(nullable=True)
    categorie_qui_alerte: Series[str] = pa.Field(nullable=True, isin=CATEGORIES_QUI_ALERTE)
    cross: Series[str] = pa.Field(nullable=True, isin=CROSS_LIST)
    departement: Series[str] = pa.Field(nullable=True)
    est_metropolitain: Series[bool] = pa.Field(nullable=True)
    evenement: Series[str] = pa.Field(nullable=True)
    categorie_evenement: Series[str] = pa.Field(nullable=True, isin=CATEGORIES_EVENEMENT)
    autorite: Series[str] = pa.Field(nullable=True, isin=AUTORITES)
    seconde_autorite: Series[str] = pa.Field(nullable=True, isin=SECONDES_AUTORITES)
    zone_responsabilite: Series[str] = pa.Field(nullable=True, isin=ZONES_RESPONSABILITE)
    latitude: Series[float] = pa.Field(nullable=True, ge=-90, le=90)
    longitude: Series[float] = pa.Field(nullable=True, ge=-180, le=180)
    vent_direction: Series[float] = pa.Field(nullable=True, ge=0, le=360)
    vent_direction_categorie: Series[str] = pa.Field(nullable=True, isin=DIRECTIONS_VENT)
    vent_force: Series[float] = pa.Field(nullable=True, ge=0, le=12)
    mer_force: Series[float] = pa.Field(nullable=True, ge=0, le=9)
    date_heure_reception_alerte: Series[str] = pa.Field(nullable=True)
    date_heure_fin_operation: Series[str] = pa.Field(nullable=True)
    numero_sitrep: Series[int] = pa.Field(nullable=True, ge=0)
    cross_sitrep: Series[str] = pa.Field(nullable=True)
    fuseau_horaire: Series[str] = pa.Field(nullable=True, isin=FUSEAUX_HORAIRES)
    systeme_source: Series[str] = pa.Field(nullable=True, isin=SYSTEMES_SOURCE)

    class Config(pa.DataFrameModel.Config):
        coerce = True
        name = "OperationSchema"
