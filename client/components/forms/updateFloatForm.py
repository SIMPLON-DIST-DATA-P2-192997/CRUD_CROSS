from pydantic_schemas.flotteur import FlotteurRead
import streamlit as st
from schemas import flotteur as f
import requests

def on_submit_handler(is_update: bool, float_id: int, data: FlotteurRead):
  if is_update:
    UPDATE_URL = f"http://localhost:8000/flotteurs/{float_id}"
    try:
      st.text(f"UPDATE CALLED : {data}")
      response = requests.put(UPDATE_URL, json=data)
      st.toast("Float successfully updated")
    except requests.exceptions.RequestException as e:
      st.error(f"Error update float : {e}")
  return

def UpdateFloatForm(float: FlotteurRead, is_update: bool = False):
  st.text(f"FLOAT : {float}")
  order_number_val = float.get('numero_ordre')
  previous_data = {
    "up_f_order_number" : str(order_number_val) if order_number_val is not None else None,
    "up_f_flag": float.get('pavillon'),
    "up_f_float_state": float.get('resultat_flotteur'),
    "up_f_type": float.get('type_flotteur'),
    "up_f_category": float.get('categorie_flotteur'),
    "up_f_immatriculation": float.get('numero_immatriculation') 
  }
  
  for key, value in previous_data.items():
    if key not in st.session_state:
      st.session_state[key] = value
    
  with st.form(key="float_form"):
    # st.text(st.session_state)
    order_number = st.text_input("numero d'ordre", key="up_f_order_number")
    flag = st.selectbox("Pavillon", key="up_f_flag", options=f.PAVILLONS)
    float_state = st.selectbox("Etat du flotteur", key="up_f_float_state", options=f.RESULTATS_FLOTTEUR)
    type = st.text_input('Type de flotteur', key="up_f_type")
    category = st.selectbox('Catégorie', key="up_f_category", options=f.CATEGORIES_FLOTTEUR)
    immatriculation = st.text_input('Immatriculation', key="up_f_immatriculation")
    if is_update:
      submit = st.form_submit_button("Update", width="stretch")
    else:
      submit = st.form_submit_button('Add float', width='stretch')
      
    if submit:
      updated_float = {
      'numero_ordre': order_number,
      'pavillon': flag,
      'type_flotteur': type,
      'resultat_flotteur': float_state,
      'categorie_flotteur': category,
      }
      on_submit_handler(is_update, float['id'], updated_float)