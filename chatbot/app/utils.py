import os
from typing import List, Optional

from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory


def load_chain(
    api_key: Optional[str] = None, tool_names: List[str] = ["wikipedia"]
) -> AgentExecutor:
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = OpenAI(temperature=0, openai_api_key=api_key)
    tools = load_tools(tool_names, llm=llm)
    chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )
    return chain


def set_openai_api_key(api_key: str) -> Optional[AgentExecutor]:
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        chain = load_chain(api_key=api_key, tool_names=["wikipedia"])
        os.environ["OPENAI_API_KEY"] = ""
        return chain
