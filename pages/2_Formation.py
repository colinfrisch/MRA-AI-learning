import streamlit as st
import json, os
from backend.catalog_manager import CatalogManager

def main(data_path):
    st.title("Formation")
    catalog_manager = CatalogManager()

    selected_chapters = []
    if "selected_training" in st.session_state : 
        selected_chapters = json.loads(st.session_state["selected_training"])["selected_chapters"]
    else :
        st.warning("pas de selection de formation")
    print(selected_chapters)

    chapters = catalog_manager.get_chapters(selected_chapters)

    if not chapters:
        st.warning("Le JSON de formation ne contient pas de chapitres.")
        return

    # Initialisation de l'état pour les chapitres terminés et le chapitre en cours
    if "completed_chapters" not in st.session_state:
        st.session_state["completed_chapters"] = set()  # Utilisation d'un set pour garder les chapitres terminés

    if "current_chapter" not in st.session_state:
        st.session_state["current_chapter"] = 0

    # Barre latérale : liste des chapitres
    with st.sidebar:
        st.header("Chapitres")

        for i, chapter in enumerate(chapters):
            # Affichage du bouton avec le statut "✅" si le chapitre est terminé
            if i in st.session_state["completed_chapters"]:
                # Affichage du bouton avec le statut "✅" si le chapitre est terminé
                button_label = f"{'✅ ' if i in st.session_state['completed_chapters'] else ''}{chapter['name']}"
                if st.button(button_label, key=f"chap_{i}"):
                    st.session_state["current_chapter"] = i
                    st.rerun()
            else:
                # Affichage du bouton avec statut "✅" si le chapitre est terminé ou non
                button_label = f"{'✅ ' if i < st.session_state['current_chapter'] else ''}{chapter['name']}"
                
                if st.button(button_label, key=f"chap_{i}"):
                    # Mettre à jour le chapitre actuel seulement si ce chapitre n'est pas encore terminé
                    if i >= st.session_state["current_chapter"]:
                        st.session_state["current_chapter"] = i
                        st.session_state["completed_chapters"].add(i)  # Marquer ce chapitre comme terminé
                    st.rerun()  # Rafraîchir l'interface après avoir changé l'état

    # Chapitre en cours
    current_index = st.session_state["current_chapter"]
    current_chapter = chapters[current_index]

    st.subheader(current_chapter.get("name", "Chapitre"))
    st.write(current_chapter.get("description", ""))
    st.write(current_chapter.get("content", ""))

    # Test / QCM du chapitre
    test = current_chapter.get("test", [])
    if test:
        st.write("---")
        st.write("**Test du chapitre**")
        for idx_q, question_obj in enumerate(test):
            question = question_obj.get("question", "")
            responses = question_obj.get("responses", [])
            st.write(f"**Q{idx_q+1}. {question}**")
            
            for idx_r, response_obj in enumerate(responses):
                text = response_obj.get("text", "")
                valid = response_obj.get("valid", "false").lower() == "true"
                if st.button(text, key=f"q{idx_q}-r{idx_r}"):
                    if valid:
                        st.success("Bonne réponse !")
                    else:
                        st.error("Mauvaise réponse...")

    # Bouton "Chapitre suivant"
    if st.button("Passer au chapitre suivant"):
        if st.session_state["current_chapter"] < len(chapters) - 1:
            st.session_state["current_chapter"] += 1
            st.rerun()
        else:
            st.balloons()
            st.write("Félicitations ! Vous avez terminé tous les chapitres.")

if __name__ == "__main__":
    data_path = 'data'
    main(data_path)
