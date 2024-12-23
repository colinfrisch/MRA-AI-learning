import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets.general.OPENAI_API_KEY)

def main():
    st.title("Chatbot")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Load the initial prompt from a file
    with open("initial_prompt.json", "r") as file:
        initial_prompt = json.load(file)

    if not st.session_state["messages"]:
        st.session_state["messages"].append(initial_prompt)

    # Function to handle user input when pressing Enter
    def handle_user_input():
        user_input = st.session_state.user_input  # the text_input value is stored in session_state
        if not user_input.strip():
            st.warning("Veuillez entrer un message.")
            return

        # Add user message to the conversation
        st.session_state["messages"].append({"role": "user", "content": user_input})

        try:
            # Call OpenAI ChatCompletion
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state["messages"]
            )
            assistant_message = response.choices[0].message.content
            # Add assistant message
            st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
        # Clear the text_input after submission
        st.session_state.user_input = ""

    # Container for displaying the conversation
    top_container = st.container()
    with top_container:
        st.subheader("Historique de la conversation")
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                st.markdown(
                    f"<div style='text-align: right; color: blue;'>{message['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='text-align: left;'>{message['content']}</div>",
                    unsafe_allow_html=True
                )

    # Container for the user input at the bottom
    bottom_container = st.container()
    with bottom_container:
        # Text input that triggers `handle_user_input()` when Enter is pressed
        user_input = st.text_input(
            "Entrez votre message :", 
            key="user_input", 
            on_change=handle_user_input
        )
        # You could optionally add a button, but it's not strictly needed if we rely on Enter

if __name__ == "__main__":
    main()
