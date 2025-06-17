from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import requests
from langchain_community.tools import DuckDuckGoSearchResults


load_dotenv()

llm = ChatOpenAI()

search_tool = DuckDuckGoSearchResults()
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm = llm, tools =[search_tool], prompt=prompt)

agent_executor = AgentExecutor(agent= agent, tools= [search_tool], verbose= True)

agent_executor.invoke({"input": "Give a 5 pointer preview for upcoming test series of India?"})
