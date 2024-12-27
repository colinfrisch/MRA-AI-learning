from openai import OpenAI
import streamlit as st
from chat.chat_manager import ChatManager

def main():
  st.title("Traiing")

  if "chatmgr" not in st.session_state:
        st.session_state["chatmgr"] = ChatManager()

  client = st.session_state.chatmgr
  messages = client.get_messages()[1:]
  
  for message in messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  if prompt := st.chat_input("What is up?"):
      client.add_message("user", prompt)


if __name__ == "__main__":
    main()


  