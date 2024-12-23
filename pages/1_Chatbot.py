import streamlit as st
import openai

def main():
    st.title("Chatbot")

    # Renseignez votre clé d'API OpenAI (vous pouvez la mettre dans Streamlit secrets)
    # openai.api_key = st.secrets["OPENAI_API_KEY"]
    # Pour la démonstration, on affiche juste un champ de texte permettant à l'utilisateur d'entrer sa clé
    user_api_key = st.text_input("Votre clé d'API OpenAI :", type="password")
    if user_api_key:
        openai.api_key = user_api_key

    st.write("Discutez avec ChatGPT via l'API OpenAI.")

    # Initialisation de l'historique de conversation
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Champ de saisie pour l'utilisateur
    user_input = st.text_input("Entrez votre message :")

    if st.button("Envoyer"):
        if not user_api_key:
            st.warning("Veuillez renseigner votre clé d'API OpenAI avant de continuer.")
            return

        # Ajout du message utilisateur dans l'historique
        st.session_state["messages"].append({"role": "user", "content": user_input})

        try:
            # Appel à l'API OpenAI ChatCompletion
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state["messages"]
            )
            assistant_message = completion.choices[0].message.content

            # Ajout du message assistant dans l'historique
            st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
            
            # Affichage ou actions selon la réponse de ChatGPT
            # 1. Si ChatGPT renvoie "ko"
            if assistant_message.strip().lower().startswith("ko"):
                st.error("Tant pis, plus tard...")
                # Bouton renvoyant vers Google
                if st.button("Aller sur Google"):
                    st.markdown("[Cliquez ici pour ouvrir Google](https://www.google.com)")

            # 2. Si ChatGPT renvoie "ok"
            elif assistant_message.strip().lower().startswith("ok"):
                st.success("Bravo !")
                st.write("Continuez vos échanges ! Quelle est votre prochaine question ?")

            # 3. Si ChatGPT renvoie un message qui commence par "{"
            elif assistant_message.strip().startswith("{"):
                st.info("Nous avons reçu un contenu JSON pour la formation.")
                # Stocker dans la session
                st.session_state["formation_data"] = assistant_message
                # Rediriger vers la page de formation
                st.experimental_rerun()

            # Sinon, on affiche le contenu tel quel
            else:
                st.write(assistant_message)

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

    # Historique de la conversation (optionnel) :
    with st.expander("Historique de la conversation"):
        for msg in st.session_state["messages"]:
            role = "Vous" if msg["role"] == "user" else "ChatGPT"
            st.write(f"**{role}:** {msg['content']}")

if __name__ == "__main__":
    main()
