# Suggested placement: app/services/icp.py or a new utils file for message conversion

import base64
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage, ToolMessage
from app.models.icp import Message as AppMessage, TextContent, FileContent # Your custom types
from app.utils.types import MessageRole # Your MessageRole enum

def convert_app_message_to_lc_message(app_msg: AppMessage) -> BaseMessage:
    lc_content_parts = []

    if isinstance(app_msg.content, str):
        lc_content_parts.append({"type": "text", "text": app_msg.content})
    elif isinstance(app_msg.content, list):
        for part in app_msg.content:
            if isinstance(part, TextContent):
                lc_content_parts.append({"type": "text", "text": part.text})
            elif isinstance(part, FileContent):
                if "file" in part.type:
                    lc_content_parts.append({
                        "type": "file",
                        "source_type": "base64",
                        "mime_type": "application/pdf",
                        "data": part.data,
                        "image_url": {"url": f"data:{part.mime_type};base64,{part.data}"}
                    })
                elif "text" in part.mime_type: # e.g. text/plain that was base64 encoded
                    try:
                        decoded_text = base64.b64decode(part.data).decode('utf-8')
                        lc_content_parts.append({"type": "text", "text": decoded_text})
                    except Exception as e:
                        print(f"Warning: Could not decode base64 FileContent (mime: {part.mime_type}) as text: {e}")
                        lc_content_parts.append({"type": "text", "text": f"[File content: {part.mime_type}, unable to decode as text]"})
                else:
                    print(f"Warning: FileContent with mime_type '{part.mime_type}' might not be directly processable by the LLM as is. Consider text extraction upstream.")
                    lc_content_parts.append({"type": "text", "text": f"[Non-image file content: {part.mime_type}]"})
            else:
                raise ValueError(f"Unsupported content part type: {type(part)}")
    else:
        raise ValueError(f"Message content must be a string or a list of content parts. Got: {type(app_msg.content)}")

    final_lc_content = lc_content_parts
    if len(lc_content_parts) == 1 and lc_content_parts[0]["type"] == "text":
        final_lc_content = lc_content_parts[0]["text"]


    if app_msg.role == MessageRole.user:
        return HumanMessage(content=final_lc_content)
    elif app_msg.role == MessageRole.assistant:
        return AIMessage(content=final_lc_content)
    elif app_msg.role == MessageRole.tool:
        return ToolMessage(content=final_lc_content)
    else:
        raise ValueError(f"Unsupported message role for conversion: {app_msg.role}")