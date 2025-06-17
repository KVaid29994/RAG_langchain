from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o")

# Correctly name the tool as "Intermediate Answer" (required by Self Ask With Search)
search_tool = DuckDuckGoSearchResults()

tools = [
    Tool(
        name="Intermediate Answer",  # REQUIRED name for SelfAskWithSearch agent
        func=search_tool.run,
        description="Useful for answering factual questions by searching the web."
    )
]

# Create the agent using SelfAskWithSearch pattern
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.SELF_ASK_WITH_SEARCH,
    verbose=True,
    handle_parsing_errors=True  # Helps in retrying on output parsing issues
)

# Ask the question
question = "Who is the current CEO of OpenAI and what was their role before this?"
response = agent.invoke(question)

# Print response
print("\n🧠 Answer:\n", response)
