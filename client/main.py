import sys
import os
import streamlit as st

# Ajoute le dossier parent (la racine du projet) aux chemins de recherche de Python
chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if chemin_racine not in sys.path:
    sys.path.append(chemin_racine)
# import pandas as pd
# from pathlib import Path
# import requests
from components.FormContainer import FormContainer
# from schemas.flotteur import FlotteurSchema, PAVILLONS, CATEGORIES_FLOTTEUR, RESULTATS_FLOTTEUR

with st.container():
    st.header("Brief CROSS", width='stretch', text_alignment='center')
    st.text("Florian, Yannick, William", width='stretch', text_alignment='center')
