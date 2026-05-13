import streamlit as st
from .forms.OperationForm import OperationForm
from .forms.FloatForm import FloatForm
from .forms.HumanResForm import HumandResForm
from .forms.ParamsForm import ParamsForm

def on_click_handler(i):
  st.session_state['part'] += i
  
def on_create_handler():
  st.write(st.session_state)

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
    'pa_system'
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
    
  for cle in list(st.session_state.keys()):
    if not cle.startswith("FormSubmitter:"):
      st.session_state[cle] = st.session_state[cle]
  
  
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
      left.button('Previous', on_click=on_click_handler, args=[-1], width='stretch')
    if st.session_state['part'] < MAX_PART:
      right.button('Next', on_click=on_click_handler, args=[1], width='stretch')
    else:
      right.button('Create', on_click=on_create_handler, width='stretch')
