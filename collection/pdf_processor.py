import requests
import pdfplumber
import os
from typing import List, Dict, Any
from urllib.parse import urljoin

def download_pdf(url: str, filename: str) -> str:
    """Download PDF from URL"""
    response = requests.get(url)
    filepath = f"/tmp/{filename}.pdf"
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath

def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from PDF"""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def download_and_process_pdfs(announcements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Download and process PDF announcements"""
    chunks = []
    for ann in announcements:
        try:
            pdf_url = ann.get('pdf_url')
            if pdf_url:
                filename = f"{ann['ts_code']}_{ann['ann_date']}_{ann['title'][:20]}"
                filepath = download_pdf(pdf_url, filename)
                text = extract_text_from_pdf(filepath)
                text_chunks = chunk_text(text)

                for i, chunk in enumerate(text_chunks):
                    chunks.append({
                        "ts_code": ann["ts_code"],
                        "year": ann["ann_date"][:4],
                        "period": "announcement",
                        "doc_id": ann["ann_id"],
                        "content": chunk,
                        "chunk_index": i,
                        "metadata": ann
                    })

                os.remove(filepath)  # Clean up

        except Exception as e:
            print(f"Error processing {ann.get('title')}: {str(e)}")
            continue

    return chunks
