from supabase import create_client, Client
import os
from typing import List, Dict, Any
from config import DB_BATCH_SIZE

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upsert_financial_data(data: List[Dict[str, Any]]):
    """Upsert financial data in batches"""
    for i in range(0, len(data), DB_BATCH_SIZE):
        batch = data[i:i + DB_BATCH_SIZE]
        supabase.table("financial_data").upsert(batch, on_conflict="ts_code,end_date").execute()

def update_document_status(ts_code: str, status: str):
    """Update document processing status"""
    supabase.table("documents").update({"status": status}).eq("ts_code", ts_code).execute()

def batch_insert_chunks(chunks: List[Dict[str, Any]]):
    """Insert text chunks in batches"""
    for i in range(0, len(chunks), DB_BATCH_SIZE):
        batch = chunks[i:i + DB_BATCH_SIZE]
        supabase.table("chunks").insert(batch).execute()

# Add more database operations as needed
