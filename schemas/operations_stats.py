import pandera.pandas as pa
from pandera.typing import Series


MOIS_TEXTE = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
PHASES_JOURNEE = ["matinée", "déjeuner", "après-midi", "nuit"]
NOMS_STM = ["stm-corsen", "stm-gris-nez", "stm-jobourg"]
NOMS_DST = ["dst-casquets", "dst-corse", "dst-dover", "dst-ouessant"]
PREFECTURES_MARITIMES = ["atlantique", "manche", "mediterranee"]
CATEGORIES_MAREE = ["20-45", "46-70", "71-95", "96-120"]


class OperationStatsSchema(pa.DataFrameModel):
    operation_id: Series[int]
    date: Series[str] = pa.Field(nullable=True, str_matches=r"^\d{4}-\d{2}-\d{2}$")
    annee: Series[int] = pa.Field(ge=1984)
    mois: Series[int] = pa.Field(ge=1, le=12)
    jour: Series[int] = pa.Field(ge=1, le=31)
    mois_texte: Series[str] = pa.Field(nullable=True, isin=MOIS_TEXTE)
    semaine: Series[int] = pa.Field(ge=1, le=53)
    annee_semaine: Series[str] = pa.Field(nullable=True, str_matches=r"^\d{4}-\d{1,2}$")
    jour_semaine: Series[str] = pa.Field(nullable=True, isin=JOURS_SEMAINE)
    est_weekend: Series[bool]
    est_jour_ferie: Series[bool]
    est_vacances_scolaires: Series[object] = pa.Field(nullable=True)
    phase_journee: Series[str] = pa.Field(nullable=True, isin=PHASES_JOURNEE)
    concerne_plongee: Series[bool]
    implique_wingfoil: Series[bool]
    avec_clandestins: Series[bool]
    distance_cote_metres: Series[float] = pa.Field(nullable=True, ge=0)
    distance_cote_milles_nautiques: Series[float] = pa.Field(nullable=True, ge=0)
    est_dans_stm: Series[bool]
    nom_stm: Series[str] = pa.Field(nullable=True, isin=NOMS_STM)
    est_dans_dst: Series[bool]
    nom_dst: Series[str] = pa.Field(nullable=True, isin=NOMS_DST)
    prefecture_maritime: Series[str] = pa.Field(nullable=True, isin=PREFECTURES_MARITIMES)
    maree_port: Series[str] = pa.Field(nullable=True)
    maree_coefficient: Series[float] = pa.Field(nullable=True, ge=22, le=118)
    maree_categorie: Series[str] = pa.Field(nullable=True, isin=CATEGORIES_MAREE)
    nombre_personnes_blessees: Series[int] = pa.Field(ge=0)
    nombre_personnes_assistees: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees_accidentellement: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees_naturellement: Series[int] = pa.Field(ge=0)
    nombre_personnes_disparues: Series[int] = pa.Field(ge=0)
    nombre_personnes_impliquees_dans_fausse_alerte: Series[int] = pa.Field(ge=0)
    nombre_personnes_retrouvees: Series[int] = pa.Field(ge=0)
    nombre_personnes_secourues: Series[int] = pa.Field(ge=0)
    nombre_personnes_tirees_daffaire_seule: Series[int] = pa.Field(ge=0)
    nombre_personnes_tous_deces: Series[int] = pa.Field(ge=0)
    nombre_personnes_tous_deces_ou_disparues: Series[int] = pa.Field(ge=0)
    nombre_personnes_impliquees: Series[int] = pa.Field(ge=0)
    nombre_personnes_blessees_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_assistees_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees_accidentellement_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_decedees_naturellement_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_disparues_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_impliquees_dans_fausse_alerte_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_retrouvees_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_secourues_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_tirees_daffaire_seule_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_tous_deces_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_tous_deces_ou_disparues_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_personnes_impliquees_sans_clandestins: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_commerce_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_peche_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_loisirs_nautiques_impliques: Series[int] = pa.Field(ge=0)
    nombre_aeronefs_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_autre_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_annexe_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_autre_loisir_nautique_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_canoe_kayak_aviron_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_engin_de_plage_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_kitesurf_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_voile_legere_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_a_moteur_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_a_moteur_moins_8m_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_a_moteur_plus_8m_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_plaisance_a_voile_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_planche_a_voile_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_ski_nautique_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_surf_impliques: Series[int] = pa.Field(ge=0)
    nombre_flotteurs_vehicule_nautique_a_moteur_impliques: Series[int] = pa.Field(ge=0)
    sans_flotteur_implique: Series[bool]

    class Config(pa.DataFrameModel.Config):
        coerce = True
        name = "OperationStatsSchema"
