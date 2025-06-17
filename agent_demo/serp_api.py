import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.utilities import SerpAPIWrapper
import textwrap

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o")

# Initialize SerpAPI wrapper
search = SerpAPIWrapper()

# Define tools
tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="Useful for answering questions by searching Google."
    )
]

# Create the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True ,handle_parsing_errors=True
)

# Take user input
user_query = input("💬 Ask your question: ")

# Run the agent
response = agent.invoke(user_query)

# Extract and format the output
output_text = response.get("output", str(response)) if isinstance(response, dict) else str(response)

# Show final result
wrapped = textwrap.fill(output_text, width=90)

print("\n🧠 Answer:\n", wrapped)
