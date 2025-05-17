from typing import List

from langchain_core.messages import BaseMessage

from app.agents.icp.icp import icp_chatbot

async def generate_icp_service(messages: List[BaseMessage]):
    llm_response = await icp_chatbot.invoke(messages)
    return llm_response