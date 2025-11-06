from crewai import tool
import tushare as ts
import os
from typing import List, Dict, Any

# Initialize Tushare
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

@tool
def get_realtime_quotes(ts_codes: List[str]) -> str:
    """Get real-time stock quotes for given codes"""
    df = pro.daily(ts_code=','.join(ts_codes), start_date='20240101', end_date='20241201')  # Adjust dates
    return df.to_json(orient='records')

@tool
def get_market_data(ts_code: str, start_date: str, end_date: str) -> str:
    """Get historical market data for a stock"""
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df.to_json(orient='records')

# Add more realtime tools as needed
