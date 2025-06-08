"""
YoungWB Financial Analysis Entry Point

This script demonstrates the use of refactored components for financial analysis
using CrewAI instead of LangChain.
"""
import os
import pandas as pd
from vnstock import Vnstock
import warnings
from datetime import datetime

# Import refactored components
from youngwb.financial_analysis import analyze_financial_statements
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please set your OpenAI API key in .env file or as an environment variable.")
    # Using a placeholder is not recommended for production
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Silence warnings
warnings.filterwarnings("ignore")

# Define parameters
ticker = 'REE'  # Example ticker
# Function to retrieve financial data for a specific ticker
def retrieve_financial_data(ticker, source='VCI'):
    """Retrieve financial statements for the specified ticker"""
    print(f"Retrieving financial data for {ticker}...")
    
    # Initialize the stock data interface
    stock = Vnstock().stock(symbol=ticker, source=source)
    
    # Retrieve financial statements
    balance_sheet = stock.finance.balance_sheet(period='year', lang='en', dropna=True)
    income_statement = stock.finance.income_statement(period='year', lang='en', dropna=True)
    cash_flow = stock.finance.cash_flow(period='year')
    
    # Calculate Levered Free Cash Flow
    if 'Net cash inflows/outflows from operating activities' in cash_flow.columns:
        cash_flow['Levered Free Cash Flow'] = (
            cash_flow['Net cash inflows/outflows from operating activities'] 
            - cash_flow.get('Purchase of fixed assets', 0)
            + cash_flow.get('Proceeds from disposal of fixed assets', 0)
            - (cash_flow.get('Repayment of borrowings', 0) - cash_flow.get('Proceeds from borrowings', 0))
        )
    
    # Return the data
    return balance_sheet, income_statement, cash_flow


# Main execution block
if __name__ == "__main__":
    try:
        # Retrieve financial data for the specified ticker
        balance_sheet, income_statement, cash_flow = retrieve_financial_data(ticker)
        
        print(f"\nAnalyzing financial data for {ticker}...\n")
        
        # Perform financial analysis using the refactored function
        analysis_result = analyze_financial_statements(
            balance_sheet_df=balance_sheet,
            income_statement_df=income_statement,
            cash_flow_df=cash_flow,
            ticker=ticker,
            output_dir="./output"
        )
        
        print("\n=== Analysis Complete ===\n")
        
    except Exception as e:
        print(f"Error during financial analysis: {e}")