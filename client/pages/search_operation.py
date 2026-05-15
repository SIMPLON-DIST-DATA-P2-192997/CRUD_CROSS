import streamlit as st
import requests
from client.components.forms.FloatForm import FloatForm
from client.components.forms.updateFloatForm import UpdateFloatForm

def fetch_operation(id: str):
  URL = f"http://localhost:8000/operations/full/{id}"
  try:
    response = requests.get(URL)
    if response.status_code == 200:
      st.session_state.clear()
      operation = response.json()
      st.session_state['deleted'] = False
      return operation
  except requests.exceptions.RequestException as e:
    st.text(f"Request failed : {e}")
    return None
  
def delete_operation(id: str):
  DELETE_URL = f"http://localhost:8000/operations/{id}"
  
  try:
    res = requests.delete(DELETE_URL)
    if res.status_code == 204:
      st.session_state.clear()
      st.success("Operation successfully deleted.")
      st.session_state['deleted'] = True
  except requests.exceptions.RequestException as e:
    st.write(f"Error : {e}")
    

with st.container():
  
  if 'operation' not in st.session_state:
    st.session_state['operation'] = None
    
  if 'deleted' not in st.session_state:
    st.session_state['deleted'] = False
    
  st.header("Look for operation by id")
  st.divider()
  
  
  with st.form(key="id_operation_form", ):
    left, right = st.columns(2, vertical_alignment="bottom")
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
    
    st.table(rest)
    
    st.header('Human results')
    st.table(human_results)
    
    st.header('Floats')
    left, right = st.columns([0.9,0.1], vertical_alignment='center')
    float_click = left.dataframe(floats, on_select='rerun', selection_mode='single-row', width='stretch')
    add_float = right.button('Add', width="content")
    if len(float_click.selection.rows) > 0:
      selected_index = float_click.selection.rows[0]
      selected_float = floats[selected_index]

      UpdateFloatForm(float=selected_float,is_update=True)
          
    st.header('Stats')
    st.table(stats)