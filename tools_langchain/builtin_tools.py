from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

search_tools = DuckDuckGoSearchRun()

tools = [Tool(name="DuckDuckGo Search",
        func=search_tools.run,
        description="Use this tool to search the web using natural language queries")]

# Create a conversational agent with tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Conversation loop
while True:
    user_input = input("Ask me anything (or type 'end' to quit): ")
    if user_input.lower() == "end":
        print("Conversation ended.")
        break
    response = agent.run(user_input)
    print("\n🔍 Answer:\n", response)

# results = search_tools.invoke('top news in india today')
# print(results)
# print(search_tools.name)
# print(search_tools.description)
# print(search_tools.args)

## Built-in Tool - Shell Tool

# from langchain_community.tools import ShellTool
# shell_tool = ShellTool()
# result = shell_tool.invoke("dir")
# print (result)

###