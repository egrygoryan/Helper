from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.Tools import weather, task_creator

load_dotenv()
def get_agent_executor() -> AgentExecutor:
    _tools = [weather, task_creator]
    _model = ChatOpenAI()
    _prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", 
                         "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!."),
                        MessagesPlaceholder("chat_history", optional=False),
                        ("human", "{input}"),
                        MessagesPlaceholder("agent_scratchpad"),
                    ]
                )

    _agent = create_openai_tools_agent(llm=_model, tools=_tools, prompt=_prompt)
    _agent_executor = AgentExecutor(agent=_agent, tools=_tools, verbose=True, max_iterations=2)
    return _agent_executor
