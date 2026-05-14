import streamlit as st
from schemas import humain_results as hr
from ..validation import Models
from pydantic import ValidationError


def HumandResForm():
  
  with st.container():
    st.header('Human results', text_alignment='center')
    st.badge('*Mandatory field', color='orange')

    with st.form('human_res_form', clear_on_submit=True, border=2):
      left, right = st.columns(2)
      with left:
        personn_category = st.selectbox("Catégorie de personne", options=hr.CATEGORIES_PERSONNE, index=None)
        number = st.text_input("Nombre", placeholder="Nombre de personnes impliquées dans ce bilan")
      with right:
        result = st.selectbox("Bilan humain", options=hr.RESULTATS_HUMAIN, index=None)
      submit = st.form_submit_button("Ajouter un bilan", width="stretch")
      error_placeholder = st.empty()
      
    st.write('#### Current human result :' )
    if len(st.session_state['human_res']) == 0:
      st.text('No human results.', width='stretch', text_alignment='center')
    else:
      st.session_state['human_res'] = st.data_editor(st.session_state['human_res'], num_rows="dynamic", use_container_width=True)
    st.divider()
    
    if submit:
      new_res = {
        'personn_category': personn_category,
        'number': number,
        'result': result,
      }
      try:
        Models.HumanResultSchema(**new_res)
        st.session_state['human_res'].append(new_res)
        st.session_state['error_human'] = None
        st.rerun()
      except ValidationError as e:
        st.session_state['error_human'] = "Please fill all fields."
        error_placeholder.error("Please fill all fields.")
      