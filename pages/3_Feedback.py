import streamlit as st
from backend.feedback_manager import FeedbackManager

def main():
    st.title("Vos retours sont importants pour nous !")
    feedback_manager = FeedbackManager()

    if "feedback_sent" not in st.session_state:
        st.session_state["feedback_sent"] = False

    if not st.session_state["feedback_sent"]:
        # Text input for feedback
        feedback_input = st.text_area("Quels sont vos retours?")

        # Button to send feedback
        if st.button("Send Feedback"):
            result = feedback_manager.process_feedback(feedback_input)
            st.write(result)
            st.session_state["feedback_sent"] = True
    else:
        st.write("Merci pour votre retour !")

if __name__ == "__main__":
    main()




