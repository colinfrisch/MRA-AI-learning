import streamlit as st
from backend.feedback_manager import FeedbackManager

def main():
    st.title("Vos retours sont importants pour nous !")
    feedback_manager = FeedbackManager()

    feedback_input = st.text_area("Quels sont vos retours?")

    # Button to send feedback
    if st.button("Send Feedback"):
        result = feedback_manager.process_feedback(feedback_input)
        st.warning(result)

if __name__ == "__main__":
    main()
