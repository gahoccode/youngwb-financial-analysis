#!/usr/bin/env python
import sys
import warnings
import os
import pandas as pd

from datetime import datetime
from vnstock import Vnstock

from youngwb.crew import Youngwb
from youngwb.financial_analysis import format_dataframe

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file runs the financial analysis crew with the appropriate inputs
# You can specify ticker symbols and other parameters when calling the functions

def retrieve_financial_data(ticker, source='VCI'):
    """
    Retrieve financial statements data for analysis.
    
    Args:
        ticker (str): Stock ticker symbol
        source (str): Data source ('VCI', 'TCBS', etc.)
    
    Returns:
        tuple: (balance_sheet, income_statement, cash_flow)
    """
    print(f"Retrieving financial data for {ticker}...")
    
    # Initialize the stock data interface
    stock = Vnstock().stock(symbol=ticker, source=source)
    
    # Retrieve financial statements
    balance_sheet = stock.finance.balance_sheet(period='year', lang='en', dropna=True)
    income_statement = stock.finance.income_statement(period='year', lang='en', dropna=True)
    cash_flow = stock.finance.cash_flow(period='year')
    
    # Calculate Levered Free Cash Flow if possible
    if 'Net cash inflows/outflows from operating activities' in cash_flow.columns:
        cash_flow['Levered Free Cash Flow'] = (
            cash_flow['Net cash inflows/outflows from operating activities'] 
            - cash_flow.get('Purchase of fixed assets', 0)
            + cash_flow.get('Proceeds from disposal of fixed assets', 0)
            - (cash_flow.get('Repayment of borrowings', 0) - cash_flow.get('Proceeds from borrowings', 0))
        )
    
    return balance_sheet, income_statement, cash_flow


def run():
    """
    Run the financial analysis crew.
    
    Usage: youngwb [ticker_symbol]
    Example: youngwb REE
    """
    # Set default ticker or get from command line
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'REE'
    
    try:
        # Retrieve financial data
        balance_sheet, income_statement, cash_flow = retrieve_financial_data(ticker)
        
        # Calculate financial ratios
        financial_ratios = pd.DataFrame()
        if 'Levered Free Cash Flow' in cash_flow.columns and 'Dividends paid' in cash_flow.columns:
            financial_ratios['Dividend Coverage Ratio'] = cash_flow['Levered Free Cash Flow'] / cash_flow['Dividends paid'].abs()
        
        # Format for the agent
        inputs = {
            'topic': f"{ticker} Financial Analysis",
            'current_year': str(datetime.now().year),
            'ticker': ticker,
            'balance_sheet': format_dataframe(balance_sheet),
            'income_statement': format_dataframe(income_statement),
            'cash_flow': format_dataframe(cash_flow),
            'financial_ratios': format_dataframe(financial_ratios)
        }
        
        # Run the crew
        result = Youngwb().crew().kickoff(inputs=inputs)
        
        # Create output directory if it doesn't exist
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the analysis to a file
        output_file = f"{output_dir}/financial_analysis_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {ticker} Financial Analysis\n\n{result}\n\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        print(f"\nAnalysis saved to {output_file}")
        return result
        
    except Exception as e:
        raise Exception(f"An error occurred while running financial analysis: {e}")


def train():
    """
    Train the financial analysis crew for a given number of iterations.
    
    Usage: train [n_iterations] [filename] [ticker]
    Example: train 5 training_data.json REE
    """
    # Check command line args
    if len(sys.argv) < 3:
        raise ValueError("Please provide number of iterations and filename")
    
    # Get ticker from command line or use default
    ticker = sys.argv[3] if len(sys.argv) > 3 else 'REE'
    
    try:
        # Retrieve financial data
        balance_sheet, income_statement, cash_flow = retrieve_financial_data(ticker)
        
        # Calculate financial ratios
        financial_ratios = pd.DataFrame()
        if 'Levered Free Cash Flow' in cash_flow.columns and 'Dividends paid' in cash_flow.columns:
            financial_ratios['Dividend Coverage Ratio'] = cash_flow['Levered Free Cash Flow'] / cash_flow['Dividends paid'].abs()
        
        # Format inputs for training
        inputs = {
            'topic': f"{ticker} Financial Analysis",
            'current_year': str(datetime.now().year),
            'ticker': ticker,
            'balance_sheet': format_dataframe(balance_sheet),
            'income_statement': format_dataframe(income_statement),
            'cash_flow': format_dataframe(cash_flow),
            'financial_ratios': format_dataframe(financial_ratios)
        }
        
        # Run training
        Youngwb().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        print(f"Training completed for {ticker} financial analysis with {sys.argv[1]} iterations")
        
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    
    Usage: replay [task_id]
    Example: replay financial_analysis_task
    """
    if len(sys.argv) < 2:
        raise ValueError("Please provide a task_id to replay")
        
    try:
        result = Youngwb().crew().replay(task_id=sys.argv[1])
        print(f"Replayed task: {sys.argv[1]}")
        return result
        
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the financial analysis crew execution and returns the results.
    
    Usage: test [n_iterations] [eval_llm] [ticker]
    Example: test 3 gpt-4o REE
    """
    # Check command line args
    if len(sys.argv) < 3:
        raise ValueError("Please provide number of iterations and evaluation LLM")
    
    # Get ticker from command line or use default
    ticker = sys.argv[3] if len(sys.argv) > 3 else 'REE'
    
    try:
        # Retrieve financial data
        balance_sheet, income_statement, cash_flow = retrieve_financial_data(ticker)
        
        # Calculate financial ratios
        financial_ratios = pd.DataFrame()
        if 'Levered Free Cash Flow' in cash_flow.columns and 'Dividends paid' in cash_flow.columns:
            financial_ratios['Dividend Coverage Ratio'] = cash_flow['Levered Free Cash Flow'] / cash_flow['Dividends paid'].abs()
        
        # Format inputs for testing
        inputs = {
            'ticker': ticker,
            'current_year': str(datetime.now().year),
            'balance_sheet': format_dataframe(balance_sheet),
            'income_statement': format_dataframe(income_statement),
            'cash_flow': format_dataframe(cash_flow),
            'financial_ratios': format_dataframe(financial_ratios)
        }
        
        # Run test with the evaluation LLM
        results = Youngwb().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        print(f"Testing completed for {ticker} financial analysis")
        
        return results
        
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
