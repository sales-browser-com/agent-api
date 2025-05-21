# agent-api-main/app/agents/search/search_agent.py
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.state import CompiledStateGraph # Correct import based on existing icp.py

from app.info.appconfig import settings
from app.agents.search.tools.profile_search_tool import profile_search_tool
from app.agents.search.tools.report_found_profiles_tool import report_found_profiles_tool
# from app.models.icp import ICPData # Not directly in state, but used for prompt

# LLM configuration
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=settings.GOOGLE_API_KEY)

class SearchAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # icp_data: Optional[ICPData] = None # ICP data is primarily passed via system prompt

def build_search_agent_graph() -> CompiledStateGraph: # Adjusted return type
    graph_builder = StateGraph(SearchAgentState)

    tools = [profile_search_tool, report_found_profiles_tool]
    # Bind tools to LLM
    # Note: The exact method to bind tools can vary slightly with Langchain versions.
    # For gemini-1.5-flash, it should support the .bind_tools method.
    llm_with_tools = llm.bind_tools(tools)


    # Define the agent node that will use the LLM and tools
    def agent_node(state: SearchAgentState):
        response_message = llm_with_tools.invoke(state["messages"])
        return {"messages": [response_message]}

    graph_builder.add_node("agent", agent_node)

    # Define the tool node
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Define conditional edges
    # The 'tools_condition' function checks if the last message contains tool calls
    graph_builder.add_conditional_edges(
        "agent",      # Source node
        tools_condition, # Function to decide the next state
        {
            "tools": "tools",  # If tool calls are present, go to "tools" node
            END: END           # Otherwise, end the graph
        }
    )

    # Add an edge from the "tools" node back to the "agent" node
    # This allows the agent to process tool outputs and continue
    graph_builder.add_edge("tools", "agent")

    # Set the entry point of the graph
    graph_builder.add_edge(START, "agent")

    # Compile the graph
    search_graph = graph_builder.compile()
    return search_graph

search_agent_graph = build_search_agent_graph()