from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

from src.agent_tools.tools import AllTools

from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass

from typing_extensions import TypedDict
from typing import Annotated


@dataclass
class GraphWorkflowConfig:
    pass


class GraphWorkflow:
    def __init__(self):
        self.graph_workflow_config = GraphWorkflowConfig()


    def graph_builder(self):

        class State(TypedDict):
            messages: Annotated[list, add_messages]

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


        graph = graph_builder.compile(checkpointer=memory)

        return graph
