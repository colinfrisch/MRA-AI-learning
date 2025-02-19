import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Application Formation + Chatbot",
                   layout="wide")

st.title("Bienvenue sur l'application Formation")
st.write("""
Utilisez la barre de navigation à gauche pour passer d'une page à l'autre.
""")
