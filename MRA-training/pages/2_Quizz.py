import streamlit as st
from backend.user_manager import UserManager
from backend.catalog_manager import TrainingManager

def get_user_from_url():
    query_params = st.experimental_get_query_params()
    return query_params.get("username", [None])[0]

def main():
    st.title("Quizz Page")

    username = get_user_from_url()
    if not username:
        st.error("Username not found in URL")
        return

    user_manager = UserManager()
    user = user_manager.get_user_by_name(username)
    if not user:
        st.error(f"User '{username}' not found")
        return

    current_training = user.get_current_training()
    if not current_training:
        st.error("No current training found for the user")
        return

    training_manager = TrainingManager()
    training = training_manager.get_training_by_id(current_training.get_training_id())
    chapters_done = current_training.get_chapters_done()
    next_chapter = None

    for chapter in training.get_chapters():
        if chapter.id not in chapters_done:
            next_chapter = chapter
            break

    if not next_chapter:
        st.success("You have completed all chapters in this training!")
        return

    st.header(f"Chapter: {next_chapter.id}")
    st.write(next_chapter.content)
    st.write(next_chapter.question)

    selected_response = st.radio("Select your response:", [response.text for response in next_chapter.get_responses()])

    if st.button("Submit"):
        for response in next_chapter.get_responses():
            if response.text == selected_response:
                if response.valid:
                    st.success("Correct answer!")
                else:
                    st.error("Incorrect answer.")
                break

if __name__ == "__main__":
    main()
