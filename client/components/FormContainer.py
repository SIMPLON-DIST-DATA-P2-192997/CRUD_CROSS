import streamlit as st
import datetime
from .forms.OperationForm import OperationForm
from .forms.FloatForm import FloatForm
from .forms.HumanResForm import HumandResForm
from .forms.ParamsForm import ParamsForm
from .validation import Models
from pydantic import ValidationError


def on_next_handler():
  
  current_part = st.session_state['part']
  
  try:
    if current_part == 1:
      Models.OperationSchema(**st.session_state)
    elif current_part == 2:
      Models.ParametersSchema(**st.session_state)
      
    st.session_state['error_message'] = None
    st.session_state['part'] += 1
    
  except ValidationError as e:
    st.session_state['error_message'] = "Please fill the mandatories fields."
    
def on_previous_handler():
  if st.session_state['part'] > 1:
    st.session_state['part'] -= 1
    st.session_state['error_message'] = None

 
def on_create_handler():
  cles_a_ignorer = ['part'] 
  
  data = {
      key: value 
      for key, value in st.session_state.items() 
      if key not in cles_a_ignorer and not key.startswith("FormSubmitter:")
  }
  data['pa_start_date'] = st.session_state['pa_start_date'].strftime("%Y-%m-%d %H:%M:%S")
  data['pa_end_date'] = st.session_state['pa_end_date'].strftime("%Y-%m-%d %H:%M:%S")
  st.write(data)
  

MAX_PART = 4

keys = [
    'op_operation_type',
    'op_cause',
    'op_means',
    'op_author',
    'op_cross',
    'op_author_category',
    'op_event',
    'op_event_category',
    'op_authority',
    'op_second_authority',
    'op_responsability_zone',
    'op_is_metro',
    'pa_start_date',
    'pa_end_date',
    'pa_lat',
    'pa_lng',
    'pa_wind_direction',
    'pa_depts',
    'pa_sea_strength',
    'pa_wind_strength',
    'pa_time_zone',
    'pa_system',
    'error_message',
    'error_human',
    'error_float'
  ]


def FormContainer():
  if "part" not in st.session_state:
    st.session_state['part'] = 1
    
  if 'human_res' not in st.session_state:
    st.session_state['human_res'] = []
    
  for key in keys:
    if key not in st.session_state:
      st.session_state[key] = None if key != "op_is_metro" else False
      if 'strength' in key:
        st.session_state[key] = 0
    
  for key in list(st.session_state.keys()):
    if not key.startswith("FormSubmitter:"):
      st.session_state[key] = st.session_state[key]
  
  
  with st.container(width='stretch', border=True):
    st.header(f"{st.session_state['part']}/{MAX_PART}", text_alignment="right")
    match st.session_state['part']:
      case 1:
        OperationForm()
      case 2:
        ParamsForm()
      case 3:
        HumandResForm()
      case 4:
        FloatForm()
    left, right = st.columns(2, width='stretch')
    if st.session_state['part'] > 1:
      left.button('Previous', on_click=on_previous_handler, width='stretch')
    if st.session_state['part'] < MAX_PART:
      right.button('Next', on_click=on_next_handler, width='stretch')
    else:
      right.button('Create', on_click=on_create_handler, width='stretch')
    if st.session_state['error_message'] != None:
      st.error(st.session_state['error_message'], width='stretch')
