from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool
from langchain_core.messages import HumanMessage
import requests


load_dotenv()

@tool
def multiplytool(a:int,b:int) -> int:
    '''
    Multiply the 2 numbers a and b '''
    return a*b


llm = ChatOpenAI()

llm_with_tools = llm.bind_tools([multiplytool])

query = HumanMessage("can you multiply 3 with 10000")
messages = [query]

result = llm_with_tools.invoke(messages)
messages.append(result)


tool_result = multiplytool.invoke(result.tool_calls[0])
messages.append(tool_result)

result_final = llm_with_tools.invoke(messages)
print (result_final.content)
print (messages)