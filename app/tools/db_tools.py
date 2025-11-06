from crewai import tool
from supabase import create_client, Client
import os
from typing import List, Dict, Any

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@tool
def get_financial_trends(company_code: str, metric: str, years: int = 5) -> str:
    """Get financial trends for a specific company and metric over time"""
    # Query logic here
    result = supabase.table("financial_data").select("*").eq("ts_code", company_code).order("end_date", desc=True).limit(years)
    return str(result.data)

@tool
def get_company_comparison(companies: List[str], metric: str, period: str) -> str:
    """Compare financial metrics between companies for a specific period"""
    # Query logic here
    result = supabase.table("financial_data").select("*").in_("ts_code", companies).eq("period", period)
    return str(result.data)

# Add more database tools as needed
