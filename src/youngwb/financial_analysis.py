"""
Financial analysis module for YoungWB.
This module provides functions for analyzing financial statements using CrewAI.
"""
import pandas as pd
import os
from datetime import datetime
from crewai import Crew

def format_dataframe(df):
    """
    Format a DataFrame as a string for inclusion in prompts.
    
    Args:
        df (pandas.DataFrame): The DataFrame to format
        
    Returns:
        str: Formatted string representation of the DataFrame
    """
    return df.to_string()

def analyze_financial_statements(balance_sheet_df, income_statement_df, cash_flow_df, ticker="", output_dir="./output"):
    """
    Analyze financial statements using CrewAI.
    
    Args:
        balance_sheet_df (pandas.DataFrame): Balance sheet data
        income_statement_df (pandas.DataFrame): Income statement data
        cash_flow_df (pandas.DataFrame): Cash flow statement data
        ticker (str, optional): Stock ticker symbol. Defaults to "".
        output_dir (str, optional): Directory to save output. Defaults to "./output".
        
    Returns:
        str: Analysis result
    """
    # Calculate key financial ratios
    financial_ratios = pd.DataFrame()
    
    # Add dividend coverage ratio if dividends paid exists in cash flow
    if 'Dividends paid' in cash_flow_df.columns and 'Net cash inflows/outflows from operating activities' in cash_flow_df.columns:
        levered_fcf = (
            cash_flow_df['Net cash inflows/outflows from operating activities'] 
            - cash_flow_df.get('Purchase of fixed assets', 0)
            + cash_flow_df.get('Proceeds from disposal of fixed assets', 0)
            - (cash_flow_df.get('Repayment of borrowings', 0) - cash_flow_df.get('Proceeds from borrowings', 0))
        )
        financial_ratios['Dividend Coverage Ratio'] = levered_fcf / cash_flow_df['Dividends paid'].abs()
    
    # Format the DataFrames as strings
    balance_sheet_string = format_dataframe(balance_sheet_df)
    income_statement_string = format_dataframe(income_statement_df)
    cash_flow_string = format_dataframe(cash_flow_df)
    financial_ratios_string = format_dataframe(financial_ratios)
    
    # Use CrewAI YAML configuration
    from youngwb.crew import Youngwb
    
    # Prepare inputs for the crew
    inputs = {
        "topic": f"{ticker} Financial Analysis",
        "current_year": str(datetime.now().year),
        "ticker": ticker,
        "balance_sheet": balance_sheet_string,
        "income_statement": income_statement_string,
        "cash_flow": cash_flow_string,
        "financial_ratios": financial_ratios_string
    }
    
    # Create the crew instance
    crew_instance = Youngwb()
    
    # Run the analysis with the inputs
    result = crew_instance.crew().kickoff(inputs=inputs)
    
    # Create markdown formatted content
    markdown_content = f"""# {ticker} Comprehensive Financial Analysis

## Analysis
{result}

---
*Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Save the output as a markdown file in the output directory
    output_filename = f"{output_dir}/financial_analysis_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_filename, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

    print(f"\nAnalysis saved to {output_filename}")
    return result
