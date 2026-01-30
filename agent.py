import yfinance as yf
from google.adk.agents import Agent
from dotenv import load_dotenv
import os

# --- 1. SETUP ---
load_dotenv()

# --- 2. DEFINE TOOLS ---

def get_stock_price(ticker: str):
    """
    Fetches the current live stock price for a given ticker symbol.
    
    Args:
        ticker: The stock symbol (e.g., 'AAPL' for Apple, 'TSLA' for Tesla, 'BTC-USD' for Bitcoin).
    """
    print(f"DEBUG: Fetching price for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        # Get 1 day of history to find the latest close
        data = stock.history(period="1d", interval="1m")
        
        if data.empty:
            return f"Error: Could not find data for symbol '{ticker}'. Are you sure it's correct?"
        
        # Get the very last price recorded
        current_price = data['Close'].iloc[-1]
        return f"${current_price:,.2f}"
    except Exception as e:
        return f"Error fetching price: {str(e)}"

def get_company_info(ticker: str):
    """
    Retrieves company summary, industry, and sector information.
    
    Args:
        ticker: The stock symbol (e.g., 'MSFT', 'NVDA').
    """
    print(f"DEBUG: Fetching info for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # We extract just the useful bits to keep the answer short
        name = info.get('longName', 'Unknown')
        industry = info.get('industry', 'Unknown')
        sector = info.get('sector', 'Unknown')
        summary = info.get('longBusinessSummary', 'No summary available')[:200] + "..." # First 200 chars
        
        return (f"Name: {name}\n"
                f"Sector: {sector}\n"
                f"Industry: {industry}\n"
                f"Summary: {summary}")
    except Exception as e:
        return f"Error fetching info: {str(e)}"

# --- 3. DEFINE THE AGENT ---
root_agent = Agent(
    model="gemini-2.5-flash",
    name="stock_analyst",
    instruction="""
    You are an expert Stock Market Analyst.
    
    YOUR GOAL:
    Help the user check real-time stock prices and learn about companies.
    
    YOUR RULES:
    1. ALWAYS use the 'get_stock_price' tool if the user asks for a price.
    2. If the user mentions a company name (like "Apple"), convert it to the ticker (AAPL) yourself.
    3. If the user asks "What does this company do?", use 'get_company_info'.
    4. Be professional and concise.
    """,
    tools=[get_stock_price, get_company_info]
)