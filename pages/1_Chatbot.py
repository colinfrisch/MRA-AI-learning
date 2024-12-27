import streamlit as st
from openai import OpenAI
from backend.catalog_manager import CatalogManager
import json

client = OpenAI(api_key=st.secrets.general.OPENAI_API_KEY)
keywords_to_skip = ["--OK","--KO","--PERSONNALISATION","JSON","{"]

def main():
    st.title("Bienvenu chez MRA")
    catalog_manager = CatalogManager()
               
    def get_next_message():
        response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state["messages"]
            )
        assistant_message = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
        return assistant_message


    def call_openai_chat():
        try:
            # Call OpenAI ChatCompletion
            msg = get_next_message()
            if msg=="--OK":
              st.session_state["messages"].append({"role": "user", "content": "--PERSONNALISATION"})
              msg = get_next_message()
            # if message starts with "GO!"
            if msg.startswith("GO!"):
                st.session_state["finish"]=True
                st.session_state["messages"].append({"role": "user", "content": "--JSON"})
                msg = get_next_message()
              
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")


    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Load the initial prompt from a file as a string
    with open("data/initial_prompt.txt", "r") as file:
        prompt= file.read()
        # replace the placeholder "CATALOG" with the list of chapters
        chapters = catalog_manager.get_chapter_list()
        prompt = prompt.replace("CATALOG", "\n".join(chapters))


        initial_prompt = {"role": "system", "content":prompt}

    if not st.session_state["messages"]:
        st.session_state["messages"].append(initial_prompt)
        call_openai_chat()


    # Function to handle user input when pressing Enter
    def handle_user_input():
        user_input = st.session_state.user_input  # the text_input value is stored in session_state
        if not user_input.strip():
            st.warning("Veuillez entrer un message.")
            return

        # Add user message to the conversation
        st.session_state["messages"].append({"role": "user", "content": user_input})
        call_openai_chat()
        # Clear the text_input after submission
        st.session_state.user_input = ""
        st.rerun()

    # Container for displaying the conversation
    for message in st.session_state.messages[1:]:
        if any(message["content"].startswith(keyword) for keyword in keywords_to_skip):
          print (message["content"])
          continue 

        with st.chat_message(message["role"]):
          st.markdown(message["content"])

            
    # Container for the user input at the bottom
    if "finish" in st.session_state:
        # create a button to go to the page Formation
        st.write("Merci pour votre temps, vous pouvez maintenant accéder à la formation!")
        # write the last message
        selected_training=st.session_state["messages"][-1]["content"]
        st.session_state["selected_training"]=selected_training
        if st.button("Acceder à la formation"):
            st.switch_page("pages/2_Formation.py")
            
    else:
        # Text input that triggers `handle_user_input()` when Enter is pressed
        prompt = st.chat_input("Say something")
        if prompt:
            #st.write(f"User has sent the following prompt: {prompt}")
            st.session_state.user_input = prompt
            handle_user_input()

if __name__ == "__main__":
    main()
