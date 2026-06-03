import streamlit as st
import backend
import time
from typing import Optional

g_user_mail : Optional[str] = None


st.set_page_config(page_title="Smart AI Chatbot", page_icon=":robot_face:", layout="wide")

try:
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css not found")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.is_guest = False
    st.session_state.token = None
    st.session_state.messages = []


st.markdown("""
<div style="color: #333; padding: 15px; font-size: 24px; font-weight: bold; text-align: center;">
    <span class="word" style="animation-delay: 0.0s;">Hello!</span>
    <span class="word" style="animation-delay: 0.3s;">I</span>
    <span class="word" style="animation-delay: 0.9s;">am</span>
    <span class="word" style="animation-delay: 1.2s;">Chikku,</span>
    <span class="word" style="animation-delay: 1.5s;">your</span>
    <span class="word" style="animation-delay: 1.8s;">smart</span>
    <span class="word" style="animation-delay: 2.1s;">AI</span>
    <span class="word" style="animation-delay: 2.5s;">assistant</span>
    <span class="word" style="animation-delay: 2.8s;">🤖</span>
</div>
""", unsafe_allow_html=True)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Save prompt to session_state so it survives reruns
prompt = st.chat_input("Type your question here...")
if prompt:
    st.session_state.pending_prompt = prompt

# Use pending_prompt instead of prompt directly
if st.session_state.get("pending_prompt"):
    if not st.session_state.logged_in:
        st.title("Login / SignUp to continue...")
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Guest"])

        with tab1:
            st.subheader("Login")
            user_mail = st.text_input("Email", key="login_email")
            user_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", key="login_button"):
                if user_mail and user_password:
                    user_exists = backend.login_user(user_mail, user_password)
                    if user_exists == "True":
                        st.session_state.logged_in = True
                        st.session_state.is_guest = False
                        st.session_state.username = user_mail
                        st.session_state.token = backend.create_access_token({"sub": user_mail})
                        st.success("Logged in successfully!")
                        g_user_mail = user_mail
                        st.rerun()
                    elif user_exists == "Invalid Password":
                        st.error("Invalid password. Please try again.")
                    else:
                        st.error("User not found. Please register first.")
                else:
                    st.warning("Please fill in all fields.")

        with tab2:
            st.subheader("Register")
            new_mail = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

            if st.button("Signup", key="signup_button"):
                if not new_mail or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    if backend.register_user(new_mail, new_password):
                        st.success("Registration successful! Please login to continue.")
                    else:
                        st.error("User already exists. Please login to continue.")

        with tab3:
            st.subheader("Continue as Guest")
            st.write("You can continue as a guest without creating an account. However, your chat history will not be saved after you leave the session.")
            if st.button("Continue as Guest", key="guest_button"):
                guest_id = backend.create_guest_user()
                st.session_state.logged_in = True
                st.session_state.is_guest = True
                st.session_state.guest_user_id = guest_id
                st.session_state.username = "Guest"
                st.success("Continuing as guest.")
                st.rerun()

        st.stop()

    # User is logged in — process the saved prompt
    actual_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None  # Clear after use

    st.chat_message("user").markdown(actual_prompt)
    st.session_state.messages.append({"role": "user", "content": actual_prompt})

    with st.spinner("Chikku is thinking..."):
        if st.session_state.is_guest:
            response = backend.guest_chatbot(backend.userQuery(question=actual_prompt), st.session_state.guest_user_id)
        else:
            response = backend.Chatbot(backend.userQuery(question=actual_prompt), st.session_state.username)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = response['Ai Response']
        streamed_response = ""
        for char in full_response:
            streamed_response += char
            placeholder.markdown(streamed_response)
            time.sleep(0.01)

    st.session_state.messages.append({"role": "assistant", "content": full_response})