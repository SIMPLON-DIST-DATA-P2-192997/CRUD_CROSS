import sys
import os
import streamlit as st

# Ajoute le dossier parent (la racine du projet) aux chemins de recherche de Python
chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)
# import pandas as pd
# from pathlib import Path
# import requests
from components.FormContainer import FormContainer
# from schemas.flotteur import FlotteurSchema, PAVILLONS, CATEGORIES_FLOTTEUR, RESULTATS_FLOTTEUR

FormContainer()

# @st.cache_data
# def get_data_and_display(csv_name: str, number_of_items: int = 200):
#   dataset_path = f"{Path(__file__).parent.parent}/data/{csv_name}.csv"
#   df = pd.read_csv(dataset_path,nrows=number_of_items)
  
#   return st.dataframe(df, hide_index=True)

# @st.cache_data
# def get_filling_values_for_forms(form_name: str):
#   return None

# st.title('_Crud CROSS FYW_', width="stretch", text_alignment="center")
# left, right = st.columns(2)
# csv_name = None
# create = left.button("Create", width="stretch")
# read = right.button("Read", width="stretch")

# if read:
#   op, stats, human, floats = st.tabs(['Operations', 'Stats', 'Human result', 'Floats'])
#   with op:
#     st.header('Operations :')
#     get_data_and_display('operations')
#   with stats:
#     st.header('Operations :')
#     get_data_and_display('operation_stats')
#   with human: 
#     get_data_and_display('human_result')
#   with floats:
#     get_data_and_display('flotteurs')
    
    
# if create:
#   op, stats, human, floats = st.tabs(['Operations', 'Stats', 'Human result', 'Floats'])
#   with floats:
#     df = pd.read_csv('data/flotteurs.csv')
    
#     type_options = df['type_flotteur'].dropna().unique()
#     current_operation_id = "17320251153"
#     with st.form('create_floats'):
#       order_number = st.text_input(label="Numéro d'ordre")
#       flag = st.selectbox('Pavillon', PAVILLONS, index=None)
#       float_state = st.selectbox('Etat du flotteur', RESULTATS_FLOTTEUR, index=None)
#       type = st.text_input('Type de flotteur')
#       category = st.selectbox("Catégorie", CATEGORIES_FLOTTEUR, index=None)
#       immmatriculation = st.text_input('Immatriculation', placeholder="Numéro d'immatriculation du navire")
      
#       submit = st.form_submit_button("Create floats", width='stretch')
      
      
#   if submit:
#     payload = {
#       "operation_id": [current_operation_id],
#       "numero_ordre": [order_number],
#       "pavillon": [flag],
#       "resultat_flotteur": [float_state],
#       "type_flotteur": [type],
#       "categorie_flotteur": [category],
#       "numero_immatriculation": [immmatriculation if immmatriculation else None]
#     }
    
#     FlotteurSchema.validate(payload)
    