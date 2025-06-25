import streamlit as st
import streamlit.components.v1 as components

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Append user/bot messages
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# Handle input submission
def handle_submit():
    user_msg = st.session_state.user_input.strip()
    if user_msg:
        add_message("user", user_msg)
        # Dummy bot reply - replace with your LangGraph or LLM output
        add_message("bot", f"Echo: {user_msg}")

# Input text field
st.text_input("Type a message", key="user_input", label_visibility="collapsed", on_change=handle_submit)

# Generate chat messages HTML
html_messages = ""
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    html_messages += f'<div class="message {role_class}">{msg["content"]}</div>'

# HTML template with escaped curly braces
html_code = f"""
<div class="chat-wrapper">
  <div class="chat-box" id="chat-box">
    {html_messages}
  </div>
  <div class="input-box">
    <input type="text" id="chat-input" placeholder="Type a message..." onkeydown="handleKey(event)" />
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<style>
.chat-wrapper {{
    width: 100%;
    max-width: 600px;
    height: 600px;
    border: 1px solid #ccc;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin: auto;
    font-family: Arial, sans-serif;
}}
.chat-box {{
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    background: #e5ddd5;
}}
.message {{
    margin-bottom: 10px;
    padding: 10px 15px;
    border-radius: 10px;
    max-width: 75%;
    clear: both;
}}
.user {{
    background-color: #dcf8c6;
    float: right;
    text-align: right;
}}
.bot {{
    background-color: #fff;
    float: left;
    text-align: left;
}}
.input-box {{
    display: flex;
    padding: 10px;
    border-top: 1px solid #ccc;
    background: white;
}}
#chat-input {{
    flex: 1;
    padding: 10px;
    font-size: 16px;
    border-radius: 10px;
    border: 1px solid #ccc;
}}
button {{
    margin-left: 10px;
    padding: 10px 15px;
    font-size: 16px;
    border: none;
    background-color: #128C7E;
    color: white;
    border-radius: 10px;
    cursor: pointer;
}}
</style>

<script>
function handleKey(e) {{
  if (e.key === 'Enter') {{
    sendMessage();
  }}
}}
function sendMessage() {{
  const input = window.parent.document.querySelector('#chat-input');
  const value = input.value;
  if (value.trim()) {{
    const streamlitInput = window.parent.document.querySelector('input[data-baseweb="input"]');
    streamlitInput.value = value;
    const event = new Event('input', {{ bubbles: true }});
    streamlitInput.dispatchEvent(event);
    input.value = '';
    window.parent.document.querySelector('button[kind="secondary"]').click();
  }}
}}
setTimeout(() => {{
  const box = document.getElementById('chat-box');
  box.scrollTop = box.scrollHeight;
}}, 100);
</script>
"""

# Render final chat box
components.html(html_code, height=620, scrolling=False)
