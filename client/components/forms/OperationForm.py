import streamlit as st
from schemas import operations

def OperationForm():
  with st.container():
    st.header('Operation', text_alignment='center')
    st.badge('*Mandatory field', color='orange')
    left, right = st.columns(2)
    with left:
      operation_type = st.selectbox("*Type d'opération", index=None, options=operations.TYPES_OPERATION, key='op_operation_type')
      cause = st.text_input("Cause", placeholder="Pourquoi l'alerte a été donnée", key='op_cause')
      means = st.text_input("Moyen", placeholder="Comment l'alerte a été donnée", key="op_means")
      author = st.text_input("Auteur", placeholder="Qui a donnée l'alerte", key='op_author')
      cross = st.selectbox("*CROSS", options=operations.CROSS_LIST, index=None, key="op_cross")
    with right:
      author_category = st.selectbox("*Categorie de l'auteur",index=None, options=operations.CATEGORIES_QUI_ALERTE, key="op_author_category")
      event = st.text_input("*Evènement", placeholder="Évenement qui a donné lieu à l'opération", key='op_event')
      event_category = st.selectbox("*Catégorie de l'évènement", options=operations.CATEGORIES_EVENEMENT, index=None, key="op_event_category")
      authority = st.selectbox("*Autorité", options=operations.AUTORITES, index=None, key="op_authority")
      if authority != None:
        second_authority = st.selectbox("2nd autorité", operations.AUTORITES, index=None, key='op_second_authority')
      responsability_zone = st.selectbox("*Zone de responsabilité", options=operations.ZONES_RESPONSABILITE, index=None, key='op_responsability_zone')
      is_metro = st.checkbox("En métropole",key="op_is_metro")
    