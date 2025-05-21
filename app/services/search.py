# agent-api-main/app/services/search.py
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, ToolMessage, HumanMessage

from app.models.search import SearchRequestDTO, Profile, SearchResponseDTO
from app.agents.search.search_agent import search_agent_graph
from app.agents.search.prompts.system_prompt import build_search_system_prompt
# from app.utils.icp import convert_app_message_to_lc_message # If we had user messages in DTO

async def find_profiles_service(request_dto: SearchRequestDTO) -> SearchResponseDTO:
    icp_data = request_dto.icp_data
    system_prompt_content = build_search_system_prompt(icp_data)
    
    initial_messages: List[BaseMessage] = [
        SystemMessage(content=system_prompt_content),
        # Adding a human message can sometimes help steer the agent if the system prompt alone isn't enough
        # or if the LLM expects a human turn to start.
        HumanMessage(content="Please find and report profiles based on the ICP I provided in the system instructions.")
    ]

    input_data = {"messages": initial_messages}
    
    # Invoke the search agent graph
    # The graph will run until it hits an END state or max iterations
    final_state = await search_agent_graph.ainvoke(input_data)
    
    found_profiles_list: List[Profile] = []
    tool_output_message = None

    # Iterate through messages in reverse to find the arguments of the 'report_found_profiles_tool' call
    # or the output of the 'report_found_profiles_tool' execution.
    for msg in reversed(final_state.get("messages", [])):
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tool_call in msg.tool_calls:
                if tool_call["name"] == "report_found_profiles_tool":
                    profiles_arg = tool_call["args"].get("profiles")
                    if isinstance(profiles_arg, list):
                        for p_data in profiles_arg:
                            try:
                                # The LLM should format it correctly, but Pydantic validates
                                found_profiles_list.append(Profile(**p_data))
                            except Exception as e:
                                print(f"Error parsing profile data from tool call args: {p_data}, Error: {e}")
                        # Break once the relevant tool call is processed
                        break 
            if found_profiles_list: # If profiles were extracted from AIMessage tool_calls
                break
        
        # Also check ToolMessage in case the AIMessage above was the one *before* the final reporting
        # The final output of report_found_profiles_tool is a string, but we want its input arguments.
        # The AIMessage that *calls* report_found_profiles_tool is what we're primarily interested in.
        # If the graph ends *after* report_found_profiles_tool runs, its output might be in a ToolMessage.
        if isinstance(msg, ToolMessage) and msg.name == "report_found_profiles_tool":
            tool_output_message = msg.content # e.g., "Successfully reported 5 profiles."


    if not found_profiles_list and tool_output_message:
        # This means the tool was called (likely with an empty list if no profiles found),
        # and we have confirmation.
        return SearchResponseDTO(found_profiles=[], message=tool_output_message)
    elif not found_profiles_list:
        return SearchResponseDTO(found_profiles=[], message="No profiles were explicitly reported by the agent. The agent might not have found any or an issue occurred.")


    return SearchResponseDTO(found_profiles=found_profiles_list, message=tool_output_message or f"Successfully found {len(found_profiles_list)} profiles.")