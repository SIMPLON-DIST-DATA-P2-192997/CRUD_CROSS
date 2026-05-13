import streamlit as st
from schemas import humain_results as hr

def HumandResForm():
  
  with st.container():
    st.header('Human results', text_alignment='center')


    with st.form('human_res_form', clear_on_submit=True, border=2):
      left, right = st.columns(2)
      with left:
        personn_category = st.selectbox("Catégorie de personne", options=hr.CATEGORIES_PERSONNE, index=None)
        number = st.text_input("Nombre", placeholder="Nombre de personnes impliquées dans ce bilan")
      with right:
        result = st.selectbox("Bilan humain", options=hr.RESULTATS_HUMAIN, index=None)
        # hurted_number = st.text_input("Nombre de bléssé")
      submit = st.form_submit_button("Ajouter un bilan", width="stretch")
    st.divider()
    st.text('Bilan actuel : ' )
    st.session_state['human_res'] = st.data_editor(st.session_state['human_res'], num_rows="dynamic", use_container_width=True)
    st.divider()
    if submit:
      new_res = {
        'personn_category': personn_category,
        'number': number,
        'result': result,
      }
      st.session_state['human_res'].append(new_res)
      
      st.rerun()