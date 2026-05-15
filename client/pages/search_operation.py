import streamlit as st
import requests
from client.components.forms.FloatForm import FloatForm

def fetch_operation(id: str):
  st.text(f'ID DANS LE FETCH : {id}')
  URL = f"http://localhost:8000/operations/full/{id}"
  try:
    response = requests.get(URL)
    st.text(response)
    if response.status_code == 200:
      operation = response.json()
      return operation
  except requests.exceptions.RequestException as e:
    st.text(f"Request failed : {e}")
    return None
  
def delete_operation(id: str):
  st.text(f"ID : {id}")
  DELETE_URL = f"http://localhost:8000/operations/{id}"
  
  try:
    res = requests.delete(DELETE_URL)
    if res.status_code == 204:
      # st.session_state.clear()
      st.rerun()
  except requests.exceptions.RequestException as e:
    st.write(f"Error : {e}")
    
    
    

with st.container():
  
  if 'operation' not in st.session_state:
    st.session_state['operation'] = None
    
  st.header("Look for operation by id")
  st.divider()
  
  with st.form(key="id_operation_form", ):
    left, right = st.columns(2)
    id_input = left.text_input("Operation ID")
    submit = right.form_submit_button("Search")
    
  if submit and id_input:
    operation = fetch_operation(id_input)
    if operation:
      st.session_state['operation'] = operation
      
  if st.session_state['operation']:
    operation_data = st.session_state['operation']
    rest = operation_data.copy()
    
    floats = rest.pop('flotteurs',[])
    human_results = rest.pop('human_results', [])
    stats = rest.pop('operations_stats', [])
    
    st.header("Operation details")
    left,right = st.columns(2)
    
    delete = left.button("Delete")
    if delete:
      delete_operation(id_input)
    update = right.button('Update')
    
    st.table(rest)
    
    st.header('Human results')
    st.table(human_results)
    
    st.header('Floats')
    float_click = st.dataframe(floats, on_select='rerun', selection_mode='single-row')
    if len(float_click.selection.rows) > 0:
      # Récupère l'index de la ligne cliquée
      selected_index = float_click.selection.rows[0]
      # Récupère le flotteur correspondant
      selected_float = floats[selected_index]
      
      # Affiche un popover avec les détails du flotteur sélectionné
      with st.popover(f"Update float", ):
          FloatForm()
          
    st.header('Stats')
    st.table(stats)