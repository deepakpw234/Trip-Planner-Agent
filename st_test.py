import streamlit as st
from streamlit.components.v1 import html

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input handling
def add_message():
    user_input = st.session_state.user_input.strip()
    if user_input:
        st.session_state.messages.append(("user", user_input))
        bot_reply = f"You said: {user_input}"
        st.session_state.messages.append(("bot", bot_reply))
        st.session_state.user_input = ""  # Clear input



with open("src\layout\logic_agent.js",'r') as f:
    js = f"<script>{f.read()}</script>"


with open("src\layout\css_agent.css",'r') as f:
    css = f"<style>{f.read()}</style>"

with open("src\layout\html_agent.html",'r') as f:
    html_template = f.read()


# Generate messages HTML
messages_html = ""
for role, msg in reversed(st.session_state.messages):
    messages_html += f'<div class="message {role}">{msg}</div>'




# Inject the HTML + JS
final_html = html_template.format(messages_html=messages_html)
html(css + final_html + js,height=530)


with st.form('input_form',clear_on_submit=True):
    col1, col2 = st.columns([8,1])
    with col1:
        st.text_input("User Input",label_visibility='collapsed',placeholder="Type a message...",key="user_input")
    with col2:
        st.form_submit_button("Send",on_click=add_message)
