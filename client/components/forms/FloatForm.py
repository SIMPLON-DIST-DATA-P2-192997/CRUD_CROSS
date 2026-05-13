import streamlit as st
from schemas import flotteur as f

def FloatForm():
  
  if "floats" not in st.session_state:
    st.session_state['floats'] = []
    
  with st.container():
    st.header('Float')
    with st.form("float_part_form", clear_on_submit=True):
      left, right = st.columns(2)
      
      with left:
        order_number = st.text_input(label="Numéro d'ordre")
        flag = st.selectbox('Pavillon', f.PAVILLONS, index=None)
        float_state = st.selectbox('Etat du flotteur', f.RESULTATS_FLOTTEUR, index=None)

      with right:
        type = st.text_input('Type de flotteur')
        category = st.selectbox("Catégorie", f.CATEGORIES_FLOTTEUR, index=None)
        immmatriculation = st.text_input('Immatriculation', placeholder="Numéro d'immatriculation du navire")
      
      submit = st.form_submit_button("Create floats", width='stretch')
    
    if submit:
      new_float = {
        'order_number': order_number,
        'flag': flag,
        'type': type,
        'float_state': float_state,
        'category': category,
        'immatriculation': immmatriculation
      }
      st.session_state['floats'].append(new_float)
      
    st.divider()
    st.write('#### Current float :')
    if len(st.session_state['floats']) <= 0:
      st.text("No float", text_alignment='center', width='stretch' )
    else:
      st.session_state['floats'] = st.data_editor(
        st.session_state['floats'],
        width='stretch',
        num_rows='dynamic'
      )
    st.divider()