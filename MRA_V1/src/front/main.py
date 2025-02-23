import streamlit as st
from dotenv import load_dotenv

from backend.user_manager import UserManager
from backend.training_creator import TrainingCreator

load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Application Formation + Chatbot", layout="wide")

st.title("Bienvenue sur l'application Formation")
st.write(
    """
Utilisez la barre de navigation à gauche pour passer d'une page à l'autre.
"""
)


if st.button("Premier apprentissage (fake)"):
    username = "john doe"
    user_manager = UserManager()
    user = user_manager.get_user_by_name(username)
    if not user:
        print("Creating User")
        user = user_manager.create_user(username, "911")
    training_creator = TrainingCreator()
    training_creator.check_trainings()
    training = training_creator.db.training.find_first()
    if training:
        user_manager.start_training(user, training)
        st.session_state["user_name"] = "john doe"
        st.switch_page(f"pages/2_Quizz.py")
    else:
        st.error("No training found")
