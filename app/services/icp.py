from typing import List, Dict, Any

# Assuming these imports are correctly placed in your actual file structure
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage, ToolMessage
from app.models.icp import Message, ICPData  # Your application-specific models
from app.agents.icp.icp import icp_chatbot  # Your Langchain agent/graph
from app.agents.icp.prompts.system_prompt import build_system_prompt
from app.utils.icp import convert_app_message_to_lc_message


async def generate_icp_service(messages: List[Message], icpData: ICPData) -> Dict[str, Any]:
    """
    Generates an ICP and extracts specific information from the LLM response,
    including tool call arguments, tool output, and the final AI message.
    """
    system_prompt_content = build_system_prompt(icpData)
    lc_system_message = SystemMessage(content=system_prompt_content)

    converted_user_messages: List[BaseMessage] = []
    for app_msg in messages:
        converted_user_messages.append(convert_app_message_to_lc_message(app_msg))

    messages_for_graph: List[BaseMessage] = [lc_system_message] + converted_user_messages

    input_data = {"messages": messages_for_graph}

    # Store the number of messages before invoking the graph to easily find new messages
    num_messages_before_graph_output = len(messages_for_graph)

    llm_response = await icp_chatbot.ainvoke(input_data)

    all_messages_after_run = llm_response["messages"]
    newly_added_messages = all_messages_after_run[num_messages_before_graph_output:]

    # Initialize a dictionary to store the extracted data
    extracted_data = {
        "tool_call_args": None,
        "tool_call_output_content": None,
        # "ai_response_content": None  # This will hold the content of the last AI message
    }

    for msg in newly_added_messages:
        if isinstance(msg, AIMessage):
            extracted_data["ai_response_content"] = msg.content

            if msg.tool_calls and len(msg.tool_calls) > 0:
                print(msg.tool_calls)
                extracted_data["tool_call_args"] = msg.tool_calls[0]['args']

        # elif isinstance(msg, ToolMessage):
        #     # This is the content returned by the tool execution.
        #     extracted_data["tool_call_output_content"] = msg.content
        #     # The ai_response_content will likely be updated by a subsequent AIMessage
        #     # that processes this tool output.

    return extracted_data