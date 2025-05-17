from typing import Annotated, List

from langchain_core.messages import BaseMessage


from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.state import CompiledStateGraph

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.icp.tools.icp_output import icp_output_tool
from app.info.appconfig import settings

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0,google_api_key=settings.GOOGLE_API_KEY)

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def build_chatbot_graph() -> CompiledStateGraph:
    graph_builder = StateGraph(State)

    tools = [icp_output_tool]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot_node(state: State):
        response_message = llm_with_tools.invoke(state["messages"])
        return {"messages": [response_message]}

    graph_builder.add_node("chatbot", chatbot_node)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )

    graph_builder.add_edge("tools", "chatbot")

    graph_builder.add_edge(START, "chatbot")

    graph = graph_builder.compile()
    return graph

icp_chatbot = build_chatbot_graph()