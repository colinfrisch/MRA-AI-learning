import streamlit as st
import json

def main():
    st.title("Formation")

    # Vérifier si on a reçu des données de formation
    if "formation_data" not in st.session_state:
        st.warning("Aucun contenu de formation n'est disponible pour le moment.")
        st.info("Veuillez d'abord aller sur la page Chatbot pour charger une formation.")
        return

    # Récupérer le contenu JSON depuis la session
    formation_json = st.session_state["formation_data"]

    try:
        formation_data = json.loads(formation_json)
    except json.JSONDecodeError:
        st.error("Impossible de décoder le JSON de la formation.")
        return

    chapters = formation_data.get("chapters", [])
    if not chapters:
        st.warning("Le JSON de formation ne contient pas de chapitres.")
        return

    # État : index du chapitre en cours
    if "current_chapter" not in st.session_state:
        st.session_state["current_chapter"] = 0

    # Barre latérale : liste des chapitres
    with st.sidebar:
        st.header("Chapitres")
        for i, chapter in enumerate(chapters):
            # Indique si un chapitre est "fait" ou pas.
            # Ici, on considère qu'un chapitre est fait si l'index est strictement inférieur 
            # au chapitre en cours (vous pouvez personnaliser la logique).
            status = "✅ " if i < st.session_state["current_chapter"] else ""
            if st.button(f"{status}{chapter['name']}", key=f"chap_{i}"):
                st.session_state["current_chapter"] = i

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
            
            # Affichage des réponses sous forme de boutons
            for idx_r, response_obj in enumerate(responses):
                text = response_obj.get("text", "")
                valid = response_obj.get("valid", "false").lower() == "true"
                # On utilise un bouton par réponse
                if st.button(text, key=f"q{idx_q}-r{idx_r}"):
                    if valid:
                        st.success("Bonne réponse !")
                    else:
                        st.error("Mauvaise réponse...")

    # Bouton "Chapitre suivant"
    if st.button("Passer au chapitre suivant"):
        if st.session_state["current_chapter"] < len(chapters) - 1:
            st.session_state["current_chapter"] += 1
            st.experimental_rerun()
        else:
            st.balloons()
            st.write("Félicitations ! Vous avez terminé tous les chapitres.")

if __name__ == "__main__":
    main()
