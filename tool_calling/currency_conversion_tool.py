from langchain_core.tools import tool , InjectedToolArg
import requests
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage ,ToolMessage, AIMessage
from typing import Annotated
import json



load_dotenv()

# Tool 1: Get conversion factor
@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:

    ''' gets the conversion factor between based and target currency'''
    url = f"https://v6.exchangerate-api.com/v6/2b1e2cc04d173c927765f0e3/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    return response.json()["conversion_rate"]

# Tool 2: Convert value
@tool
def convert(base_currency_value: float, conversion_rate: float) -> float:
    ''' converts
    '''
    return base_currency_value * conversion_rate

# Setup LLM with both tools
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools([get_conversion_factor, convert])

# Start conversation
messages = [HumanMessage(content="What is the conversion factor between USD and INR, and based on that can you convert 10 USD to INR")]

# First LLM call to get tool suggestions
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

# Loop through the tool calls
for tool_call in ai_response.tool_calls:
    if tool_call['name'] == "get_conversion_factor":
        tool_result = get_conversion_factor.invoke(tool_call['args'])
        messages.append(ToolMessage(tool_call_id=tool_call['id'], content=str(tool_result)))
        conversion_rate = tool_result  # capture for use in next tool

# Second LLM call after tool result
ai_response2 = llm_with_tools.invoke(messages)
messages.append(ai_response2)

# Second tool call
for tool_call in ai_response2.tool_calls:
    if tool_call['name'] == "convert":
        tool_call['args']["conversion_rate"] = conversion_rate
        tool_result = convert.invoke(tool_call['args'])
        messages.append(ToolMessage(tool_call_id=tool_call['id'], content=str(tool_result)))

# Final LLM response
final_response = llm_with_tools.invoke(messages)
print(final_response.content)
