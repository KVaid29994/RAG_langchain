import yfinance as yf
from datetime import datetime, timedelta
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")



@tool
def get_stock_summary(ticker: str) -> str:
    """
    Fetches the current stock price and 1-year return percentage.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., AAPL, TSLA)
    
    Returns:
        str: A summary with the current price and return over 1 year.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        if hist.empty:
            return f"No historical data found for {ticker}."

        # Get current price and price from 1 year ago
        current_price = hist["Close"][-1]
        one_year_ago_price = hist["Close"][0]

        percent_return = ((current_price - one_year_ago_price) / one_year_ago_price) * 100

        return (
            f"📈 {ticker.upper()} Stock Summary:\n"
            f"Current Price: ${current_price:.2f}\n"
            f"Price 1 Year Ago: ${one_year_ago_price:.2f}\n"
            f"1-Year Return: {percent_return:.2f}%"
        )

    except Exception as e:
        return f"Error fetching data: {e}"

    
agent = initialize_agent(
    tools=[get_stock_summary],
    llm=llm,
    agent_type="openai-tools",
    verbose=True
)

agent.invoke("Give me the 1-year return and current price of AAPL.")