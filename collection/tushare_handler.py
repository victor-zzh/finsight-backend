import tushare as ts
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

def get_company_list() -> List[str]:
    """Get list of A-share companies"""
    df = pro.stock_basic(exchange='', list_status='L')
    return df['ts_code'].tolist()

def get_financial_statements(ts_code: str) -> List[Dict[str, Any]]:
    """Get financial statements for a company"""
    # Balance sheet
    balance = pro.balancesheet(ts_code=ts_code, period='20231231')
    # Income statement
    income = pro.income(ts_code=ts_code, period='20231231')
    # Cash flow
    cashflow = pro.cashflow(ts_code=ts_code, period='20231231')

    # Combine and format data
    data = []
    # Add processing logic here
    return data

def get_announcements(ts_code: str, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """Get company announcements in batches"""
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y%m%d')

    df = pro.anns(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df.to_dict('records')

# Add more Tushare API wrappers as needed
