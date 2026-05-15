import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
import streamlit as st
import pandas as pd
from database import engine
import matplotlib.pyplot as plt

with st.container():
  st.header('KPI')
  st.divider()
  
  st.header("Répartition des types d'opérations")
  repartition_res = pd.read_sql_query("SELECT type_operation, COUNT(*) as count FROM operation WHERE type_operation IS NOT NULL GROUP BY type_operation;", con=engine)
  fig, ax = plt.subplots()
  ax.bar(repartition_res['type_operation'], repartition_res['count'])
  plt.xticks(rotation=45, ha='right')
  st.pyplot(fig)
  
  st.header("Gravité des opérations")
  gravite_res = pd.read_sql_query("SELECT SUM(nombre_personnes_decedees) AS morts, SUM(nombre_personnes_blessees) AS blesses FROM operation_stat;", con=engine)
  categories = ['Morts', 'Blesses']
  valeurs = [gravite_res['morts'][0], gravite_res['blesses'][0]]
  fig, ax = plt.subplots()
  ax.bar(categories, valeurs, color=['#d62728', '#ff7f0e']) 
  ax.set_ylabel('Nombre de personnes')
  st.pyplot(fig)
  
  st.header("Météo et incidents")
  meteo_res = pd.read_sql_query("SELECT vent_force, COUNT(*) as count FROM operation WHERE vent_force IS NOT NULL GROUP BY vent_force ORDER BY vent_force;", con=engine)
  fig, ax = plt.subplots()
  ax.bar(meteo_res['vent_force'], meteo_res['count'])
  ax.set_xlabel('Force du vent')
  ax.set_ylabel("Nombre d'incidents")
  st.pyplot(fig)
  
  st.header('Type de flotteur et danger')
  danger_res = pd.read_sql_query("SELECT categorie_flotteur, COUNT(*) AS incidents FROM flotteur WHERE categorie_flotteur IS NOT NULL GROUP BY categorie_flotteur ORDER BY incidents DESC;", con=engine)
  fig, ax = plt.subplots(figsize=(10, 6))
  ax.bar(danger_res['categorie_flotteur'], danger_res['incidents'])
  plt.xticks(rotation=45, ha='right')
  ax.set_xlabel('Catégorie de flotteur')
  ax.set_ylabel("Nombre d'incidents")
  plt.tight_layout()
  st.pyplot(fig)

  st.header("Evolution annuelle des opérations")
  evolution_res = pd.read_sql_query("""SELECT
          annee,
          COUNT(DISTINCT operation_id) AS total_operations
      FROM operation_stat
      GROUP BY annee
      ORDER BY annee""", con=engine)
  fig, ax = plt.subplots(figsize=(10, 5))

  ax.plot(
      evolution_res["annee"],
      evolution_res["total_operations"],
      marker="o",
      linewidth=2
  )

  ax.set_title("Nombre d'opérations par année")
  ax.set_xlabel("Année")
  ax.set_ylabel("Nombre d'opérations")
  ax.grid(True, alpha=0.3)

  st.pyplot(fig)