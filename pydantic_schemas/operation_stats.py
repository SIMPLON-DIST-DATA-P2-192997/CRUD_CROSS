from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
import re

MoisTexte = Literal[
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
]
JourSemaine = Literal["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
PhaseJournee = Literal["matinée", "déjeuner", "après-midi", "nuit"]
NomSTM = Literal["stm-corsen", "stm-gris-nez", "stm-jobourg"]
NomDST = Literal["dst-casquets", "dst-corse", "dst-dover", "dst-ouessant"]
PrefectureMaritme = Literal["atlantique", "manche", "mediterranee"]
CategorieMaree = Literal["20-45", "46-70", "71-95", "96-120"]


class OperationStatsBase(BaseModel):
    operation_id: int = Field(..., gt=0)
    date: Optional[str] = None
    annee: int = Field(..., ge=1984, le=2100)
    mois: int = Field(..., ge=1, le=12)
    jour: int = Field(..., ge=1, le=31)
    mois_texte: Optional[MoisTexte] = None
    semaine: Optional[int] = Field(None, ge=1, le=53)
    annee_semaine: Optional[str] = None
    jour_semaine: Optional[JourSemaine] = None
    est_weekend: bool
    est_jour_ferie: bool
    est_vacances_scolaires: Optional[str] = None
    phase_journee: Optional[PhaseJournee] = None
    concerne_plongee: bool
    implique_wingfoil: bool
    avec_clandestins: bool
    distance_cote_metres: Optional[float] = Field(None, ge=0.0)
    distance_cote_milles_nautiques: Optional[float] = Field(None, ge=0.0)
    est_dans_stm: bool
    nom_stm: Optional[NomSTM] = None
    est_dans_dst: bool
    nom_dst: Optional[NomDST] = None
    prefecture_maritime: Optional[PrefectureMaritme] = None
    maree_port: Optional[str] = None
    maree_coefficient: Optional[float] = Field(None, ge=22.0, le=118.0, description="French tidal coefficient 22-118")
    maree_categorie: Optional[CategorieMaree] = None

    @field_validator("date", mode="before")
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
            raise ValueError(f"date must match YYYY-MM-DD, got '{v}'")
        return v

    @field_validator("annee_semaine", mode="before")
    @classmethod
    def validate_annee_semaine_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.fullmatch(r"\d{4}-\d{1,2}", v):
            raise ValueError(f"annee_semaine must match YYYY-W, got '{v}'")
        return v
    nombre_personnes_blessees: int = Field(..., ge=0)
    nombre_personnes_assistees: int = Field(..., ge=0)
    nombre_personnes_decedees: int = Field(..., ge=0)
    nombre_personnes_decedees_accidentellement: int = Field(..., ge=0)
    nombre_personnes_decedees_naturellement: int = Field(..., ge=0)
    nombre_personnes_disparues: int = Field(..., ge=0)
    nombre_personnes_impliquees_dans_fausse_alerte: int = Field(..., ge=0)
    nombre_personnes_retrouvees: int = Field(..., ge=0)
    nombre_personnes_secourues: int = Field(..., ge=0)
    nombre_personnes_tirees_daffaire_seule: int = Field(..., ge=0)
    nombre_personnes_tous_deces: int = Field(..., ge=0)
    nombre_personnes_tous_deces_ou_disparues: int = Field(..., ge=0)
    nombre_personnes_impliquees: int = Field(..., ge=0)
    nombre_personnes_blessees_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_assistees_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_decedees_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_decedees_accidentellement_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_decedees_naturellement_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_disparues_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_impliquees_dans_fausse_alerte_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_retrouvees_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_secourues_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_tirees_daffaire_seule_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_tous_deces_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_tous_deces_ou_disparues_sans_clandestins: int = Field(..., ge=0)
    nombre_personnes_impliquees_sans_clandestins: int = Field(..., ge=0)
    nombre_flotteurs_commerce_impliques: int = Field(..., ge=0)
    nombre_flotteurs_peche_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_impliques: int = Field(..., ge=0)
    nombre_flotteurs_loisirs_nautiques_impliques: int = Field(..., ge=0)
    nombre_aeronefs_impliques: int = Field(..., ge=0)
    nombre_flotteurs_autre_impliques: int = Field(..., ge=0)
    nombre_flotteurs_annexe_impliques: int = Field(..., ge=0)
    nombre_flotteurs_autre_loisir_nautique_impliques: int = Field(..., ge=0)
    nombre_flotteurs_canoe_kayak_aviron_impliques: int = Field(..., ge=0)
    nombre_flotteurs_engin_de_plage_impliques: int = Field(..., ge=0)
    nombre_flotteurs_kitesurf_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_voile_legere_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_a_moteur_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_a_moteur_moins_8m_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_a_moteur_plus_8m_impliques: int = Field(..., ge=0)
    nombre_flotteurs_plaisance_a_voile_impliques: int = Field(..., ge=0)
    nombre_flotteurs_planche_a_voile_impliques: int = Field(..., ge=0)
    nombre_flotteurs_ski_nautique_impliques: int = Field(..., ge=0)
    nombre_flotteurs_surf_impliques: int = Field(..., ge=0)
    nombre_flotteurs_vehicule_nautique_a_moteur_impliques: int = Field(..., ge=0)
    sans_flotteur_implique: bool


class OperationStatsCreate(OperationStatsBase):
    pass


class OperationStatsUpdate(BaseModel):
    date: Optional[str] = None
    annee: Optional[int] = None
    mois: Optional[int] = None
    jour: Optional[int] = None
    mois_texte: Optional[str] = None
    semaine: Optional[int] = None
    annee_semaine: Optional[str] = None
    jour_semaine: Optional[str] = None
    est_weekend: Optional[bool] = None
    est_jour_ferie: Optional[bool] = None
    est_vacances_scolaires: Optional[str] = None
    phase_journee: Optional[str] = None
    concerne_plongee: Optional[bool] = None
    implique_wingfoil: Optional[bool] = None
    avec_clandestins: Optional[bool] = None
    distance_cote_metres: Optional[float] = None
    distance_cote_milles_nautiques: Optional[float] = None
    est_dans_stm: Optional[bool] = None
    nom_stm: Optional[str] = None
    est_dans_dst: Optional[bool] = None
    nom_dst: Optional[str] = None
    prefecture_maritime: Optional[str] = None
    maree_port: Optional[str] = None
    maree_coefficient: Optional[float] = None
    maree_categorie: Optional[str] = None


class OperationStatsRead(OperationStatsBase):
    id: int

    model_config = {"from_attributes": True}
