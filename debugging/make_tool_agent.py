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
from src.agent_tools.hotel_tools import HotelTools

import streamlit as st
from streamlit.components.v1 import html
import requests
import os

from dotenv import load_dotenv 
load_dotenv()

# Creating State
class State(TypedDict):
    messages: Annotated[list, add_messages]

def make_tool_graph():

    llm = ChatOpenAI()

    tools = [AllTools.get_flight_details,AllTools.get_cheapest_flight_details,AllTools.get_airport_code,AllTools.curreny_converter,
            AllTools.collect_user_information,AllTools.book_flight_comfirmation, HotelTools.get_hotel_list_by_city,HotelTools.get_hotel_details_by_hotelID,
            HotelTools.final_confirmation_node,HotelTools.book_hotel_comfirmation]

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

    return graph

tool_agent = make_tool_graph()

