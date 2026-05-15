# CRUD_CROSS

FastAPI + SQLAlchemy CRUD application for maritime rescue operations data (CROSS).

## Stack

- **FastAPI** — REST API
- **SQLAlchemy 2.0** + **psycopg2** — ORM + PostgreSQL driver
- **Alembic** — database migrations
- **Pydantic v2** — request/response schemas
- **pytest + pytest-cov** — testing & coverage
- **Docker** — PostgreSQL 16

## Database Schema

```mermaid
erDiagram
    operation {
        BigInteger operation_id PK
        String type_operation
        String pourquoi_alerte
        String moyen_alerte
        String qui_alerte
        String categorie_qui_alerte
        String cross
        String departement
        Boolean est_metropolitain
        String evenement
        String categorie_evenement
        String autorite
        String seconde_autorite
        String zone_responsabilite
        Float latitude
        Float longitude
        Float vent_direction
        String vent_direction_categorie
        Float vent_force
        Float mer_force
        String date_heure_reception_alerte
        String date_heure_fin_operation
        Integer numero_sitrep
        String cross_sitrep
        String fuseau_horaire
        String systeme_source
    }

    flotteur {
        Integer id PK
        BigInteger operation_id FK
        Float numero_ordre
        String pavillon
        String resultat_flotteur
        String type_flotteur
        String categorie_flotteur
        String numero_immatriculation
    }

    human_result {
        Integer id PK
        BigInteger operation_id FK
        String categorie_personne
        String resultat_humain
        Integer nombre
        Integer dont_nombre_blesse
    }

    operation_stat {
        Integer id PK
        BigInteger operation_id FK
        String date
        Integer annee
        Integer mois
        Integer jour
        String mois_texte
        Integer semaine
        String annee_semaine
        String jour_semaine
        Boolean est_weekend
        Boolean est_jour_ferie
        String est_vacances_scolaires
        String phase_journee
        Boolean concerne_plongee
        Boolean implique_wingfoil
        Boolean avec_clandestins
        Float distance_cote_metres
        Float distance_cote_milles_nautiques
        Boolean est_dans_stm
        String nom_stm
        Boolean est_dans_dst
        String nom_dst
        String prefecture_maritime
        String maree_port
        Float maree_coefficient
        String maree_categorie
        Integer nombre_personnes_blessees
        Integer nombre_personnes_assistees
        Integer nombre_personnes_decedees
        Integer nombre_personnes_disparues
        Integer nombre_personnes_secourues
        Integer nombre_personnes_impliquees
        Integer nombre_flotteurs_commerce_impliques
        Integer nombre_flotteurs_peche_impliques
        Integer nombre_flotteurs_plaisance_impliques
        Integer nombre_flotteurs_loisirs_nautiques_impliques
        Integer nombre_aeronefs_impliques
    }

    audit_log {
        Integer id PK
        String table_name
        String operation
        String record_id
        String changed_data
        DateTime created_at
    }

    operation ||--o{ flotteur : "has"
    operation ||--o{ human_result : "has"
    operation ||--|| operation_stat : "has"
```

## Getting Started

### 1. Start the database

```bash
docker compose up -d
```

### 2. Run the API

```bash
fastapi dev main_fastapi.py
```

### 3. Run migrations

```bash
alembic upgrade head
```

### 4. Run tests with coverage

```bash
python -m pytest tests/ -v
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/operations/` | List all operations |
| POST | `/operations/` | Create an operation |
| GET | `/operations/{id}` | Get an operation |
| PUT | `/operations/{id}` | Update an operation |
| DELETE | `/operations/{id}` | Delete an operation |
| GET | `/flotteurs/` | List all flotteurs |
| POST | `/flotteurs/` | Create a flotteur |
| GET | `/flotteurs/{id}` | Get a flotteur |
| PUT | `/flotteurs/{id}` | Update a flotteur |
| DELETE | `/flotteurs/{id}` | Delete a flotteur |
| GET | `/humain-results/` | List all human results |
| POST | `/humain-results/` | Create a human result |
| GET | `/humain-results/{id}` | Get a human result |
| PUT | `/humain-results/{id}` | Update a human result |
| DELETE | `/humain-results/{id}` | Delete a human result |
| GET | `/operation-stats/` | List all operation stats |
| GET | `/operation-stats/{id}` | Get operation stats |
| POST | `/ingest/` | Ingest a full operation payload |
| GET | `/audit/` | List audit log entries |
| GET | `/audit/{id}` | Get an audit log entry |