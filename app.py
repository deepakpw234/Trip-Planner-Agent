from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from typing_extensions import TypedDict
from typing import Annotated

from src.agent_tools.tools import AllTools

import streamlit as st
from streamlit.components.v1 import html
import requests
import os

from dotenv import load_dotenv 
load_dotenv()

st.set_page_config(page_title="Trip Planner", page_icon="🤖")
st.title("🤖 Trip Planner Agent")

# Creating State
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initializing State in session
if 'state' not in st.session_state:
    st.session_state.state = State(messages=[])


# Loading Layout for Agent
with open("src\layout\logic_agent.js",'r') as f:
    js = f"<script>{f.read()}</script>"


with open("src\layout\css_agent.css",'r') as f:
    css = f"<style>{f.read()}</style>"

with open("src\layout\html_agent.html",'r') as f:
    html_template = f.read()

session_id = st.sidebar.selectbox("Please select the session state",options=['current','new'])

config = {'configurable':{'thread_id':session_id}}

# Input handling
def add_message():
    user_input = st.session_state.user_input.strip()
    if user_input:

        st.session_state.state['messages'].append(HumanMessage(content=user_input))

        print(config["configurable"]['thread_id'])

        response = graph.invoke(st.session_state.state , config=config)

        

        st.session_state.state = response

        # for m in response['messages']:
        #     m.pretty_print()

        print(response['messages'])

        
 
messages_html = ""
for msg in reversed(st.session_state.state['messages']):
    if isinstance(msg, HumanMessage):
        role_class = 'user'
        messages_html += f'<div class="message {role_class}">{msg.content}</div>'

    elif isinstance(msg, AIMessage) and msg.content != "":
        role_class = 'bot'
        messages_html += f'<div class="message {role_class}">{msg.content}</div>'



final_html = html_template.format(messages_html=messages_html)
html(css + final_html + js,height=460)



llm = ChatOpenAI()

tools = [AllTools.get_flight_details,AllTools.get_cheapest_flight_details,AllTools.get_airport_code,AllTools.curreny_converter,
        AllTools.collect_user_information,AllTools.book_flight_comfirmation]

llm_with_tools = llm.bind_tools(tools=tools)


def planner_chatbot(data):
    messages = data['messages']
    ai_message = llm_with_tools.invoke(messages)
    messages.append(ai_message)
    return {"messages": messages }


graph_builder = StateGraph(State)

graph_builder.add_node('planner_chatbot',planner_chatbot)
graph_builder.add_node('tools',ToolNode(tools=tools))

graph_builder.add_edge(START,"planner_chatbot")
graph_builder.add_conditional_edges("planner_chatbot",tools_condition)
graph_builder.add_edge("tools","planner_chatbot")

memory = MemorySaver()


graph = graph_builder.compile(checkpointer=memory)

with open("graph_output.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

with st.form('input_form',clear_on_submit=True):
    col1, col2 = st.columns([8,1])
    with col1:
        user_input = st.text_input("User Input",label_visibility='collapsed',placeholder="Type a message...",key="user_input")
    with col2:
        submitted = st.form_submit_button("Send",on_click=add_message)



    






