from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models import Operation, Flotteur, HumainResult, OperationStats
from pydantic_schemas.ingest import OperationIngestInput
from pydantic_schemas.operation import OperationRead

router = APIRouter(prefix="/ingest", tags=["Ingest"])

RESULT_TO_STAT = {
    "Personne blessée": "nombre_personnes_blessees",
    "Personne assistée": "nombre_personnes_assistees",
    "Personne décédée": "nombre_personnes_decedees",
    "Personne décédée accidentellement": "nombre_personnes_decedees_accidentellement",
    "Personne décédée naturellement": "nombre_personnes_decedees_naturellement",
    "Personne disparue": "nombre_personnes_disparues",
    "Personne impliquée dans fausse alerte": "nombre_personnes_impliquees_dans_fausse_alerte",
    "Personne retrouvée": "nombre_personnes_retrouvees",
    "Personne secourue": "nombre_personnes_secourues",
    "Personne tirée d'affaire seule": "nombre_personnes_tirees_daffaire_seule",
}

INTEGER_STAT_FIELDS = [
    "nombre_personnes_blessees", "nombre_personnes_assistees", "nombre_personnes_decedees",
    "nombre_personnes_decedees_accidentellement", "nombre_personnes_decedees_naturellement",
    "nombre_personnes_disparues", "nombre_personnes_impliquees_dans_fausse_alerte",
    "nombre_personnes_retrouvees", "nombre_personnes_secourues",
    "nombre_personnes_tirees_daffaire_seule", "nombre_personnes_tous_deces",
    "nombre_personnes_tous_deces_ou_disparues", "nombre_personnes_impliquees",
    "nombre_personnes_blessees_sans_clandestins", "nombre_personnes_assistees_sans_clandestins",
    "nombre_personnes_decedees_sans_clandestins",
    "nombre_personnes_decedees_accidentellement_sans_clandestins",
    "nombre_personnes_decedees_naturellement_sans_clandestins",
    "nombre_personnes_disparues_sans_clandestins",
    "nombre_personnes_impliquees_dans_fausse_alerte_sans_clandestins",
    "nombre_personnes_retrouvees_sans_clandestins", "nombre_personnes_secourues_sans_clandestins",
    "nombre_personnes_tirees_daffaire_seule_sans_clandestins",
    "nombre_personnes_tous_deces_sans_clandestins",
    "nombre_personnes_tous_deces_ou_disparues_sans_clandestins",
    "nombre_personnes_impliquees_sans_clandestins",
    "nombre_flotteurs_commerce_impliques", "nombre_flotteurs_peche_impliques",
    "nombre_flotteurs_plaisance_impliques", "nombre_flotteurs_loisirs_nautiques_impliques",
    "nombre_aeronefs_impliques", "nombre_flotteurs_autre_impliques",
    "nombre_flotteurs_annexe_impliques", "nombre_flotteurs_autre_loisir_nautique_impliques",
    "nombre_flotteurs_canoe_kayak_aviron_impliques", "nombre_flotteurs_engin_de_plage_impliques",
    "nombre_flotteurs_kitesurf_impliques", "nombre_flotteurs_plaisance_voile_legere_impliques",
    "nombre_flotteurs_plaisance_a_moteur_impliques",
    "nombre_flotteurs_plaisance_a_moteur_moins_8m_impliques",
    "nombre_flotteurs_plaisance_a_moteur_plus_8m_impliques",
    "nombre_flotteurs_plaisance_a_voile_impliques", "nombre_flotteurs_planche_a_voile_impliques",
    "nombre_flotteurs_ski_nautique_impliques", "nombre_flotteurs_surf_impliques",
    "nombre_flotteurs_vehicule_nautique_a_moteur_impliques",
]

CATEGORY_TO_FLOAT_STAT = {
    "Commerce": "nombre_flotteurs_commerce_impliques",
    "Pêche": "nombre_flotteurs_peche_impliques",
    "Plaisance": "nombre_flotteurs_plaisance_impliques",
    "Loisir nautique": "nombre_flotteurs_loisirs_nautiques_impliques",
    "Aéronef": "nombre_aeronefs_impliques",
    "Autre": "nombre_flotteurs_autre_impliques",
}

MOIS_TEXTE = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def _compute_stats(payload: OperationIngestInput, operation_id: int) -> OperationStats:
    start_dt = payload.parse_date(payload.pa_start_date)
    is_clandestin = any(
        h.personn_category == "Clandestin" for h in payload.human_res
    )

    # Count persons per result type
    counts: dict[str, int] = {f: 0 for f in INTEGER_STAT_FIELDS}
    total_impliques = 0
    for h in payload.human_res:
        n = int(h.number)
        total_impliques += n
        stat_field = RESULT_TO_STAT.get(h.result or "")
        if stat_field:
            counts[stat_field] += n
        if h.personn_category != "Clandestin":
            sans_field = stat_field + "_sans_clandestins" if stat_field else None
            if sans_field and sans_field in counts:
                counts[sans_field] += n

    counts["nombre_personnes_tous_deces"] = (
        counts["nombre_personnes_decedees_accidentellement"]
        + counts["nombre_personnes_decedees_naturellement"]
    )
    counts["nombre_personnes_tous_deces_ou_disparues"] = (
        counts["nombre_personnes_tous_deces"] + counts["nombre_personnes_disparues"]
    )
    counts["nombre_personnes_impliquees"] = total_impliques

    non_clandestin_impliques = sum(
        int(h.number) for h in payload.human_res if h.personn_category != "Clandestin"
    )
    counts["nombre_personnes_impliquees_sans_clandestins"] = non_clandestin_impliques
    counts["nombre_personnes_tous_deces_sans_clandestins"] = (
        counts["nombre_personnes_decedees_accidentellement_sans_clandestins"]
        + counts["nombre_personnes_decedees_naturellement_sans_clandestins"]
    )
    counts["nombre_personnes_tous_deces_ou_disparues_sans_clandestins"] = (
        counts["nombre_personnes_tous_deces_sans_clandestins"]
        + counts["nombre_personnes_disparues_sans_clandestins"]
    )

    # Count flotteurs by category
    for f in payload.floats:
        stat_field = CATEGORY_TO_FLOAT_STAT.get(f.category or "")
        if stat_field:
            counts[stat_field] += 1

    has_flotteur = len(payload.floats) > 0

    return OperationStats(
        operation_id=operation_id,
        date=start_dt.strftime("%Y-%m-%d") if start_dt else None,
        annee=start_dt.year if start_dt else 0,
        mois=start_dt.month if start_dt else 0,
        jour=start_dt.day if start_dt else 0,
        mois_texte=MOIS_TEXTE[start_dt.month - 1] if start_dt else None,
        semaine=int(start_dt.strftime("%V")) if start_dt else None,
        annee_semaine=f"{start_dt.year}-{int(start_dt.strftime('%V'))}" if start_dt else None,
        jour_semaine=JOURS_SEMAINE[start_dt.weekday()] if start_dt else None,
        est_weekend=start_dt.weekday() >= 5 if start_dt else False,
        est_jour_ferie=False,
        est_vacances_scolaires=None,
        phase_journee=None,
        concerne_plongee=False,
        implique_wingfoil=False,
        avec_clandestins=is_clandestin,
        distance_cote_metres=None,
        distance_cote_milles_nautiques=None,
        est_dans_stm=False,
        nom_stm=None,
        est_dans_dst=False,
        nom_dst=None,
        prefecture_maritime=None,
        maree_port=None,
        maree_coefficient=None,
        maree_categorie=None,
        sans_flotteur_implique=not has_flotteur,
        **counts,
    )


@router.post("/", response_model=OperationRead, status_code=status.HTTP_201_CREATED)
def ingest_operation(payload: OperationIngestInput, db: Session = Depends(get_db)):
    # 1. Create Operation
    operation = Operation(
        type_operation=payload.op_operation_type,
        pourquoi_alerte=payload.op_cause,
        moyen_alerte=payload.op_means,
        qui_alerte=payload.op_author,
        categorie_qui_alerte=payload.op_author_category,
        cross=payload.op_cross,
        departement=payload.pa_depts,
        est_metropolitain=payload.op_is_metro,
        evenement=payload.op_event,
        categorie_evenement=payload.op_event_category,
        autorite=payload.op_authority,
        zone_responsabilite=payload.op_responsability_zone,
        latitude=float(payload.pa_lat) if payload.pa_lat else None,
        longitude=float(payload.pa_lng) if payload.pa_lng else None,
        vent_direction=float(payload.pa_wind_direction) if payload.pa_wind_direction else None,
        vent_force=payload.pa_wind_strength,
        mer_force=payload.pa_sea_strength,
        date_heure_reception_alerte=payload.pa_start_date,
        date_heure_fin_operation=payload.pa_end_date,
        fuseau_horaire=payload.pa_time_zone,
        systeme_source=payload.pa_system,
    )
    db.add(operation)
    db.flush()  # get operation_id without committing

    # 2. Create Flotteurs
    for f in payload.floats:
        flotteur = Flotteur(
            operation_id=operation.operation_id,
            numero_ordre=float(f.order_number) if f.order_number else None,
            pavillon=f.flag,
            resultat_flotteur=f.float_state,
            type_flotteur=f.type,
            categorie_flotteur=f.category,
        )
        db.add(flotteur)

    # 3. Create HumainResults
    for h in payload.human_res:
        result = HumainResult(
            operation_id=operation.operation_id,
            categorie_personne=h.personn_category,
            resultat_humain=h.result,
            nombre=int(h.number),
            dont_nombre_blesse=0,
        )
        db.add(result)
    
    # 4. Compute and create OperationStats
    stats = _compute_stats(payload, int(operation.operation_id))  # type: ignore[arg-type]
    db.add(stats)

    db.commit()
    db.refresh(operation)
    return operation

