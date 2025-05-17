from enum import Enum

class MessageRole(Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"