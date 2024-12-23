import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Application Formation + Chatbot",
                   layout="wide")

st.title("Bienvenue sur l'application Formation & Chatbot")
st.write("""
Cette application contient deux pages :
1. Un chatbot qui communique avec l'API OpenAI (ChatGPT).
2. Une page de formation, qui s'alimente d'un contenu JSON envoyé par ChatGPT.
  
Utilisez la barre de navigation à gauche pour passer d'une page à l'autre.
""")
