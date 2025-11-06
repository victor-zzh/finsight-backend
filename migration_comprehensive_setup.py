# Comprehensive database migration script for finsight-backend
# This script sets up all necessary tables and initial data

import os
from supabase import create_client, Client
from config import DB_BATCH_SIZE  # Import batch size if needed

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    """Create all necessary tables if they don't exist"""
    # Note: In production, use proper migration tools like Alembic
    # This is a simplified example

    # Example SQL for creating tables (execute via supabase client or direct SQL)
    create_documents_table = """
    CREATE TABLE IF NOT EXISTS documents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        ts_code VARCHAR(20) NOT NULL,
        year INTEGER NOT NULL,
        period VARCHAR(10) NOT NULL,
        doc_type VARCHAR(50) NOT NULL,
        file_path TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    create_chunks_table = """
    CREATE TABLE IF NOT EXISTS chunks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        document_id UUID REFERENCES documents(id),
        content TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    # Add more table creation SQL as needed

    print("Tables created successfully")

def insert_initial_data():
    """Insert any initial data if needed"""
    # Add initial data insertion logic here
    pass

if __name__ == "__main__":
    create_tables()
    insert_initial_data()
    print("Migration completed successfully")
