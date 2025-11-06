import logging
from typing import List, Optional
from config import LOOKBACK_DAYS, DB_BATCH_SIZE
from db_handler import upsert_financial_data, update_document_status
from tushare_handler import get_company_list, get_financial_statements, get_announcements
from pdf_processor import download_and_process_pdfs
from vector_handler import embed_and_store_chunks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_data_collection(mode: str, companies: Optional[List[str]] = None,
                       start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Main data collection pipeline"""

    try:
        # Step 1: Get list of companies
        if companies is None:
            companies = get_company_list()

        logger.info(f"Processing {len(companies)} companies")

        # Step 2: For each company, collect data
        for ts_code in companies:
            try:
                logger.info(f"Processing {ts_code}")

                # Update status to processing
                update_document_status(ts_code, "processing")

                # Collect structured financial data
                financial_data = get_financial_statements(ts_code)
                upsert_financial_data(financial_data)

                # Collect announcements and process PDFs
                announcements = get_announcements(ts_code, start_date, end_date)
                pdf_chunks = download_and_process_pdfs(announcements)

                # Store in vector database
                embed_and_store_chunks(pdf_chunks)

                # Update status to completed
                update_document_status(ts_code, "completed")

            except Exception as e:
                logger.error(f"Error processing {ts_code}: {str(e)}")
                update_document_status(ts_code, "failed")
                continue  # Continue with next company

        logger.info("Data collection pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise
