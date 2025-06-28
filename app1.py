from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from typing_extensions import TypedDict
from typing import Annotated

from src.agent_tools.flight_tools import AllTools

import streamlit as st
import requests
import os

from dotenv import load_dotenv 
load_dotenv()

st.set_page_config(page_title="Trip Planner", page_icon="🤖")
st.title("Trip Planner Agent")

class State(TypedDict):
    messages: Annotated[list, add_messages]





if 'state' not in st.session_state:
    st.session_state.state = State(messages=[])


if "graph" not in st.session_state:


    llm = ChatOpenAI()

    tools = [AllTools.get_flight_details,AllTools.get_airport_code,AllTools.curreny_converter,
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


    st.session_state.graph = graph_builder.compile(checkpointer=memory)

    with open("graph_output.png", "wb") as f:
        f.write(st.session_state.graph.get_graph().draw_mermaid_png())



session_id = st.sidebar.selectbox("Please select the session state",options=['current','new'])


st.markdown('<div class="chat-container">', unsafe_allow_html=True)

with st.form(key='chatform',clear_on_submit=True):
    col1, col2 = st.columns([8,1])
    with col1:
        user_input = st.text_input("",label_visibility='collapsed',placeholder="Type a message...",)
    with col2:
        submitted = st.form_submit_button("📤")


if submitted and user_input.strip():

    st.session_state.state['messages'].append(HumanMessage(content=user_input))

    config = {'configurable':{'thread_id':session_id}}

    response = st.session_state.graph.invoke(st.session_state.state , config=config)

    st.session_state.state = response

    for m in response['messages']:
        m.pretty_print()



st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
for msg in st.session_state.state['messages']:
    role_class = "user" if isinstance(msg, HumanMessage) else "bot"
    st.markdown(f'<div class="message {role_class}">{msg.content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
