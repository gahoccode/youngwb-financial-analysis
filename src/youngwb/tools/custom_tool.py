from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
import re


class FinancialAnalysisInput(BaseModel):
    """Input schema for financial analysis queries"""
    query: str = Field(..., description="Analysis query or specific financial question")


class FinancialDataTool(BaseTool):
    name: str = "Financial Data Analysis Tool"
    description: str = "Tool for analyzing financial statements and ratios. Provide type of analysis needed (profitability, liquidity, solvency, cash flow, dividends) and ticker symbol if applicable."
    args_schema: Type[BaseModel] = FinancialAnalysisInput
    
    def _run(self, query: str) -> str:
        """Run financial analysis based on the query provided.
        
        Args:
            query (str): The analysis query or financial question to address
            
        Returns:
            str: Detailed financial analysis response
        """
        try:
            # Parse the query to identify what kind of analysis is requested
            analysis_type = self._determine_analysis_type(query)
            
            # Extract any ticker symbol that might be in the query
            ticker = self._extract_ticker(query)
            
            # Enhanced debugging information
            print(f"Query received: '{query}'")
            print(f"Analysis type detected: {analysis_type}")
            print(f"Ticker detected: {ticker if ticker else 'None'}")
            
            # Based on the analysis type, generate appropriate financial insights
            if analysis_type == 'profitability':
                return self._profitability_analysis(ticker)
                
            elif analysis_type == 'liquidity':
                return self._liquidity_analysis(ticker)
                
            elif analysis_type == 'solvency':
                return self._solvency_analysis(ticker)
                
            elif analysis_type == 'cash_flow':
                return self._cash_flow_analysis(ticker)
                
            elif analysis_type == 'dividend':
                return self._dividend_analysis(ticker)
                
            else:
                return self._comprehensive_analysis(ticker)
            
        except Exception as e:
            print(f"Error in FinancialDataTool: {str(e)}")
            return f"## Financial Analysis Framework\n\nI can analyze financial statements and provide insights in the following areas:\n\n1. **Profitability Analysis**: Margins, ROE, ROA, ROCE\n2. **Liquidity Analysis**: Current ratio, quick ratio, working capital\n3. **Solvency Analysis**: Debt structure, leverage, interest coverage\n4. **Cash Flow Analysis**: Operating cash flow, free cash flow, cash flow quality\n5. **Dividend Analysis**: Yield, coverage, sustainability\n6. **Comprehensive Analysis**: All of the above plus integrated statement analysis\n\nPlease specify which type of analysis you'd like me to perform."
    
    def _determine_analysis_type(self, query: str) -> str:
        """Determine the type of analysis requested based on the query."""
        query = query.lower()
        
        if any(term in query for term in ['profit', 'margin', 'earnings', 'roe', 'roa', 'eps']):
            return 'profitability'
            
        elif any(term in query for term in ['liquid', 'current ratio', 'quick ratio', 'working capital']):
            return 'liquidity'
            
        elif any(term in query for term in ['solv', 'debt', 'leverage', 'interest coverage']):
            return 'solvency'
            
        elif any(term in query for term in ['cash flow', 'ocf', 'fcf', 'operating cash']):
            return 'cash_flow'
            
        elif any(term in query for term in ['dividend', 'payout', 'yield']):
            return 'dividend'
            
        else:
            return 'comprehensive'
    
    def _extract_ticker(self, query: str) -> str:
        """Extract ticker symbol from query if present."""
        # Simple regex pattern to find stock symbols (3-4 capital letters)
        import re
        
        # Try to find explicit ticker mentions first (e.g., "ticker: REE" or "symbol: REE")
        explicit_matches = re.findall(r'(?:ticker|symbol)\s*[:\-]?\s*([A-Z]{3,4})\b', query, re.IGNORECASE)
        if explicit_matches:
            return explicit_matches[0].upper()
        
        # Look for standalone 3-4 letter uppercase symbols
        matches = re.findall(r'\b[A-Z]{3,4}\b', query)
        if matches:
            return matches[0]
            
        return ""
    
    def _comprehensive_analysis(self, ticker: str = "") -> str:
        """Provide a comprehensive financial analysis covering all major aspects."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Comprehensive Financial Analysis {ticker_info}",
            
            "## 1. Asset Composition, Liabilities and Equity Structure",
            "A thorough analysis of the balance sheet reveals the company's financial position including asset composition, liability structure, and shareholders' equity. Key areas to examine include:",
            "- Current vs. non-current asset distribution",
            "- Debt-to-equity ratio and capital structure",
            "- Working capital adequacy",
            "- Asset quality and potential impairments",
            
            "## 2. Profitability Analysis",
            "An examination of the income statement and profitability metrics including:",
            "- Gross, operating, and net profit margins",
            "- Return on Capital Employed (ROCE)",
            "- Return on Equity (ROE)",
            "- Return on Invested Capital (ROIC)",
            "- Earnings per Share (EPS) trends",
            
            "## 3. Cash Flow Quality and Trends",
            "Analysis of operating, investing, and financing cash flows to evaluate:",
            "- Cash conversion cycle",
            "- Free cash flow generation",
            "- Cash flow to net income ratio",
            "- Capital expenditure intensity",
            
            "## 4. Liquidity and Solvency Analysis",
            "Assessment of the company's ability to meet short-term and long-term obligations:",
            "- Current and quick ratios",
            "- Interest coverage ratio",
            "- Debt service coverage ratio",
            "- Long-term debt to total assets",
            
            "## 5. Working Capital Management",
            "Evaluation of operational efficiency in managing working capital:",
            "- Inventory turnover",
            "- Accounts receivable days",
            "- Accounts payable days",
            "- Cash conversion cycle",
            
            "## 6. Year-over-Year Changes",
            "Analysis of significant changes in key financial items over time:",
            "- Revenue growth trends",
            "- Margin expansions or contractions",
            "- Changes in operational efficiency",
            "- Balance sheet composition shifts",
            
            "## 7. Integrated Statement Analysis",
            "Connections between the three financial statements to identify:",
            "- Quality of earnings",
            "- Consistency in reporting",
            "- Potential accounting issues",
            "- Financial strategy alignment",
            
            "## 8. Dividend Sustainability",
            "Analysis of the company's ability to maintain and grow dividends:",
            "- Dividend coverage ratio",
            "- Payout ratio trends",
            "- Free cash flow to dividend ratio",
            "- Historical dividend growth"
        ]
        
        return "\n\n".join(analysis)
    
    def _profitability_analysis(self, ticker: str = "") -> str:
        """Provide analysis focusing on profitability metrics."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Profitability Analysis {ticker_info}",
            
            "## Profit Margins",
            "Analysis of various profit margins to assess operational efficiency:",
            "- **Gross Profit Margin**: Indicates efficiency in production and pricing strategy",
            "- **Operating Profit Margin**: Shows operational efficiency excluding non-operating items",
            "- **Net Profit Margin**: Reflects overall profitability after all expenses",
            
            "## Return Metrics",
            "Key return metrics to evaluate management effectiveness:",
            "- **Return on Assets (ROA)**: Efficiency in using assets to generate profits",
            "- **Return on Equity (ROE)**: Return generated on shareholders' investments",
            "- **Return on Invested Capital (ROIC)**: Effectiveness of capital allocation",
            "- **Return on Capital Employed (ROCE)**: Profitability relative to capital employed",
            
            "## Earnings Analysis",
            "Assessment of earnings quality and trends:",
            "- **Earnings Per Share (EPS)**: Profitability on a per-share basis",
            "- **Earnings Growth Rate**: Consistency and momentum in earnings",
            "- **EBITDA Margin**: Earnings before interest, tax, depreciation, and amortization margin"
        ]
        
        return "\n\n".join(analysis)
    
    def _liquidity_analysis(self, ticker: str = "") -> str:
        """Provide analysis of the company's liquidity position."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Liquidity Analysis {ticker_info}",
            
            "## Short-term Liquidity Ratios",
            "Analysis of the company's ability to meet short-term obligations:",
            "- **Current Ratio**: Current assets divided by current liabilities",
            "- **Quick Ratio**: Liquid assets divided by current liabilities",
            "- **Cash Ratio**: Cash and cash equivalents divided by current liabilities",
            
            "## Working Capital Analysis",
            "Evaluation of operational liquidity through working capital:",
            "- **Net Working Capital**: Current assets minus current liabilities",
            "- **Working Capital Ratio**: Current assets to current liabilities",
            "- **Working Capital to Sales**: Working capital efficiency relative to revenue",
            
            "## Cash Conversion Cycle",
            "Assessment of how efficiently the company converts investments into cash:",
            "- **Days Inventory Outstanding (DIO)**: Average time to sell inventory",
            "- **Days Sales Outstanding (DSO)**: Average time to collect receivables",
            "- **Days Payables Outstanding (DPO)**: Average time to pay suppliers"
        ]
        
        return "\n\n".join(analysis)
    
    def _solvency_analysis(self, ticker: str = "") -> str:
        """Provide analysis of long-term solvency and debt structure."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Solvency Analysis {ticker_info}",
            
            "## Debt Structure",
            "Analysis of the company's debt composition and levels:",
            "- **Debt-to-Equity Ratio**: Total debt divided by shareholders' equity",
            "- **Debt-to-Assets Ratio**: Total debt divided by total assets",
            "- **Long-term Debt to Capital**: Long-term debt divided by total capital",
            
            "## Interest Coverage",
            "Evaluation of the company's ability to meet interest obligations:",
            "- **Interest Coverage Ratio**: EBIT divided by interest expenses",
            "- **EBITDA to Interest Expenses**: EBITDA divided by interest expenses",
            
            "## Debt Servicing Capacity",
            "Assessment of the company's ability to repay debt:",
            "- **Debt Service Coverage Ratio**: Operating income divided by debt service",
            "- **Cash Flow to Debt Ratio**: Operating cash flow divided by total debt",
            "- **Free Cash Flow to Debt**: Free cash flow divided by total debt"
        ]
        
        return "\n\n".join(analysis)
    
    def _cash_flow_analysis(self, ticker: str = "") -> str:
        """Provide analysis of cash flow statements and metrics."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Cash Flow Analysis {ticker_info}",
            
            "## Operating Cash Flow",
            "Analysis of cash generated from core business operations:",
            "- **Operating Cash Flow to Sales**: OCF divided by total revenue",
            "- **Cash Flow Quality**: OCF compared to reported net income",
            "- **Operating Cash Flow Growth**: Trend in operating cash flow over time",
            
            "## Free Cash Flow",
            "Evaluation of cash available after capital expenditures:",
            "- **Free Cash Flow (FCF)**: OCF minus capital expenditures",
            "- **FCF Yield**: FCF divided by enterprise value or market capitalization",
            "- **FCF to Sales**: FCF divided by total revenue",
            
            "## Cash Flow Components",
            "Breakdown of cash flow statement components:",
            "- **Cash Flow from Operations**: Sources and uses in operating activities",
            "- **Cash Flow from Investing**: Capital expenditures and investment activities",
            "- **Cash Flow from Financing**: Debt and equity financing activities",
            
            "## Capital Allocation",
            "Assessment of how the company allocates its cash:",
            "- **Capital Expenditure Ratio**: CapEx divided by depreciation",
            "- **Dividend Payout from FCF**: Dividends divided by free cash flow",
            "- **Share Repurchase Activity**: Cash used for share buybacks"
        ]
        
        return "\n\n".join(analysis)
    
    def _dividend_analysis(self, ticker: str = "") -> str:
        """Provide analysis of dividend policies and sustainability."""
        ticker_info = f"for {ticker} " if ticker else ""
        
        analysis = [
            f"# Dividend Analysis {ticker_info}",
            
            "## Dividend Metrics",
            "Analysis of key dividend-related metrics:",
            "- **Dividend Yield**: Annual dividends divided by share price",
            "- **Payout Ratio**: Dividends divided by net income",
            "- **Dividend Growth Rate**: Historical growth in dividend payments",
            
            "## Dividend Sustainability",
            "Evaluation of the company's ability to maintain dividend payments:",
            "- **Dividend Coverage Ratio**: Free cash flow or earnings divided by dividends paid",
            "- **Cash Dividend Coverage Ratio**: Operating cash flow divided by dividends paid",
            
            "## Dividend History",
            "Assessment of the company's historical dividend policy:",
            "- **Dividend Consistency**: Record of consistent dividend payments",
            "- **Special Dividends**: History of special or extraordinary dividends",
            "- **Dividend Policy Changes**: Historical changes in dividend strategy"
        ]
        
        return "\n\n".join(analysis)
    
    # These old helper methods are now replaced by the more comprehensive methods above