import streamlit as st
import pandas as pd
from pathlib import Path
import requests

@st.cache_data
def get_data_and_display(csv_name: str, number_of_items: int = 200):
  dataset_path = f"{Path(__file__).parent.parent}/data/{csv_name}.csv"
  df = pd.read_csv(dataset_path,nrows=number_of_items)
  
  return st.dataframe(df, hide_index=True)

@st.cache_data
def get_filling_values_for_forms(form_name: str):
  return None

st.title('_Crud CROSS FYW_', width="stretch", text_alignment="center")
left, right = st.columns(2)
csv_name = None
create = left.button("Create", width="stretch")
read = right.button("Read", width="stretch")

if read:
  op, stats, human, floats = st.tabs(['Operations', 'Stats', 'Human result', 'Floats'])
  with op:
    st.header('Operations :')
    get_data_and_display('operations')
  with stats:
    st.header('Operations :')
    get_data_and_display('operation_stats')
  with human: 
    get_data_and_display('human_result')
  with floats:
    get_data_and_display('flotteurs')
if create:
  op, stats, human, floats = st.tabs(['Operations', 'Stats', 'Human result', 'Floats'])
  with floats:
    df = pd.read_csv('data/flotteurs.csv')
    
    flag_options = df['pavillon'].dropna().unique()
    float_stat_options = df['resultat_flotteur'].dropna().unique()
    type_options = df['type_flotteur'].dropna().unique()
    category_options = df['categorie_flotteur'].dropna().unique()
    
    with st.form('create_floats'):
      order_number = st.text_input(label="Numéro d'ordre")
      flag = st.selectbox('Pavillon', flag_options, index=None)
      float_state = st.selectbox('Etat du flotteur', float_stat_options, index=None)
      type = st.selectbox("Type du flotteur", type_options, index=None)
      category = st.selectbox("Catégorie", category_options, index=None)
      immmatriculation = st.text_input('Immatriculation', placeholder="Numéro d'immatriculation du navire")
      
      submit = st.form_submit_button("Create floats", width='stretch')

if submit:
  payload = {order_number,flag,float_state,type,category, immmatriculation}
  
  