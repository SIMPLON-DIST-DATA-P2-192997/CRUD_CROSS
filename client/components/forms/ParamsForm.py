import streamlit as st
from schemas import operations

def ParamsForm():
  with st.container():
    
    if "params" not in st.session_state:
      st.session_state['params'] = {}
      
    st.header("Params")
    st.badge('*Mandatory field', color='orange')
    left, right = st.columns(2)
    
    with left:
      start_date = st.datetime_input("*Début de l'opération", key="pa_start_date")
      lat = st.text_input('*Latitude', key="pa_lat")
      wind_direction = st.text_input("*Direction du vent", key='pa_wind_direction', placeholder="En degré, exemple : 42")
      depts = st.text_input("Département", key='pa_depts', placeholder="Département où se déroule l'opération")
      sea_strength = st.slider("*Etat de la mer",0,9,0, key='pa_sea_strength')
      
    with right:
      end_date = st.datetime_input("*Fin de l'opération", key="pa_end_date")
      lng = st.text_input('*Longitude', key='pa_lng')
      wind_strength = st.slider("*Force du vent",0,12,0, key='pa_wind_strength')
      time_zone = st.selectbox('*Fuseau horaire', key='pa_time_zone', options=operations.FUSEAUX_HORAIRES, index=None)
      system = st.selectbox("*Système source", key="pa_system", options=operations.SYSTEMES_SOURCE, index=None)
    