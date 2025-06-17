from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import requests
from langchain_community.tools import DuckDuckGoSearchResults


load_dotenv()

llm = ChatOpenAI()

@tool
def count_words(text: str)->str:
    '''
    Counts the number of words in the final answer
    '''
    word_count = len(text.split())
    return f"The total word count is: {word_count}"

# def translate_text(text : str)  -> str:
#     '''
#     Translates the given text into Hindi, Spanish, and French using an external API.
#     '''
#     languages = ["hi", "es", "fr"]
#     url = "https://libretranslate.de/translate"
#     translated = {}



search_tool = DuckDuckGoSearchResults()
prompt = hub.pull("hwchase17/react")

tools = [search_tool, count_words]
agent = create_react_agent(llm = llm, tools =[search_tool], prompt=prompt)

agent_executor = AgentExecutor(agent= agent, tools= [search_tool], verbose= True)

response = agent_executor.invoke({
    "input": "Give a 5 pointer preview for upcoming test series of India? and count the number of words in the output"
})


print (response)