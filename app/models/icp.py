from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any, Literal
from app.utils.types import MessageRole
# import base64

# Define content types
class TextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str

class FileContent(BaseModel):
    type: Literal["file"] = "file"
    source_type: str = 'base64'
    data: str = Field(..., description="Base64 encoded file data")
    mime_type: str

ContentType = Union[TextContent, FileContent]

# Message can now contain different content types
class Message(BaseModel):
    role: MessageRole
    content: Union[str, List[ContentType]]  # Can be simple string or list of content objects

class GenerateICPDTO(BaseModel):
    messages: List[Message] = Field(default_factory=list)