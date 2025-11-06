from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    query: str
    companies: Optional[List[str]] = None
    time_period: Optional[str] = None
    analysis_type: Optional[str] = None

class FinancialMetric(BaseModel):
    name: str
    value: float
    unit: str
    period: str

class AnalysisSection(BaseModel):
    title: str
    content: str
    metrics: Optional[List[FinancialMetric]] = None

class AnalyzeResponse(BaseModel):
    executive_summary: str
    sections: List[AnalysisSection]
    metadata: Dict[str, Any]
    timestamp: str
