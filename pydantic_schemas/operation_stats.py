from pydantic import BaseModel
from typing import Optional


class OperationStatsBase(BaseModel):
    operation_id: int
    date: Optional[str] = None
    annee: int
    mois: int
    jour: int
    mois_texte: Optional[str] = None
    semaine: Optional[int] = None
    annee_semaine: Optional[str] = None
    jour_semaine: Optional[str] = None
    est_weekend: bool
    est_jour_ferie: bool
    est_vacances_scolaires: Optional[str] = None
    phase_journee: Optional[str] = None
    concerne_plongee: bool
    implique_wingfoil: bool
    avec_clandestins: bool
    distance_cote_metres: Optional[float] = None
    distance_cote_milles_nautiques: Optional[float] = None
    est_dans_stm: bool
    nom_stm: Optional[str] = None
    est_dans_dst: bool
    nom_dst: Optional[str] = None
    prefecture_maritime: Optional[str] = None
    maree_port: Optional[str] = None
    maree_coefficient: Optional[float] = None
    maree_categorie: Optional[str] = None
    nombre_personnes_blessees: int
    nombre_personnes_assistees: int
    nombre_personnes_decedees: int
    nombre_personnes_decedees_accidentellement: int
    nombre_personnes_decedees_naturellement: int
    nombre_personnes_disparues: int
    nombre_personnes_impliquees_dans_fausse_alerte: int
    nombre_personnes_retrouvees: int
    nombre_personnes_secourues: int
    nombre_personnes_tirees_daffaire_seule: int
    nombre_personnes_tous_deces: int
    nombre_personnes_tous_deces_ou_disparues: int
    nombre_personnes_impliquees: int
    nombre_personnes_blessees_sans_clandestins: int
    nombre_personnes_assistees_sans_clandestins: int
    nombre_personnes_decedees_sans_clandestins: int
    nombre_personnes_decedees_accidentellement_sans_clandestins: int
    nombre_personnes_decedees_naturellement_sans_clandestins: int
    nombre_personnes_disparues_sans_clandestins: int
    nombre_personnes_impliquees_dans_fausse_alerte_sans_clandestins: int
    nombre_personnes_retrouvees_sans_clandestins: int
    nombre_personnes_secourues_sans_clandestins: int
    nombre_personnes_tirees_daffaire_seule_sans_clandestins: int
    nombre_personnes_tous_deces_sans_clandestins: int
    nombre_personnes_tous_deces_ou_disparues_sans_clandestins: int
    nombre_personnes_impliquees_sans_clandestins: int
    nombre_flotteurs_commerce_impliques: int
    nombre_flotteurs_peche_impliques: int
    nombre_flotteurs_plaisance_impliques: int
    nombre_flotteurs_loisirs_nautiques_impliques: int
    nombre_aeronefs_impliques: int
    nombre_flotteurs_autre_impliques: int
    nombre_flotteurs_annexe_impliques: int
    nombre_flotteurs_autre_loisir_nautique_impliques: int
    nombre_flotteurs_canoe_kayak_aviron_impliques: int
    nombre_flotteurs_engin_de_plage_impliques: int
    nombre_flotteurs_kitesurf_impliques: int
    nombre_flotteurs_plaisance_voile_legere_impliques: int
    nombre_flotteurs_plaisance_a_moteur_impliques: int
    nombre_flotteurs_plaisance_a_moteur_moins_8m_impliques: int
    nombre_flotteurs_plaisance_a_moteur_plus_8m_impliques: int
    nombre_flotteurs_plaisance_a_voile_impliques: int
    nombre_flotteurs_planche_a_voile_impliques: int
    nombre_flotteurs_ski_nautique_impliques: int
    nombre_flotteurs_surf_impliques: int
    nombre_flotteurs_vehicule_nautique_a_moteur_impliques: int
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
