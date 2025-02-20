import streamlit as st
from backend.user_manager import UserManager
from backend.training_manager import TrainingManager

def main():
    st.title("Quizz Page")

    # retrieve user name from URL or from session state
    user_name = None
    if "user_name" in st.query_params:
        user_name = st.query_params["user_name"]
    if user_name is None:
        user_name = st.session_state.get("user_name", None)
    if user_name is None:
        st.error("Username not found in URL or session")
        return
    
    user_manager = UserManager()
    user = user_manager.get_user_by_name(user_name)
    if not user:
        st.error(f"User '{user_name}' not found")
        return

    current_chapter = user.current_chapter
    if not current_chapter:
        st.success("You have completed all chapters in this training!")
        st.write("Your score is ", user_manager.get_score_for_user(user))
        finished_trainings  = user_manager.get_finised_trainings(user)
        st.write("Training Finished :" )
        for training in finished_trainings:
            st.write(training.name+" - "+training.description)
        return

    st.header(f"{current_chapter.name}")
    st.write(current_chapter.content)
    st.write(current_chapter.question)

    selected_response = st.radio("Select your response:", [response['text'] for response in current_chapter.answers])

    if st.button("Submit"):
        success = False
        for response in current_chapter.answers:
            if response['text'] == selected_response:
                if response['valid']:
                    st.success("Correct answer!")
                    success = True
                else:
                    st.error("Incorrect answer.")
                break
        user_manager.add_eval_to_current_training_chapter(user, success)
        if st.button("Essayer une autre question"):
            st.switch_page(f"pages/2_Quizz.py")

if __name__ == "__main__":
    main()
