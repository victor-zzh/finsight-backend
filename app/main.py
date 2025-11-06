from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from crew import run_analysis  # Assuming crew.py has a run_analysis function

app = FastAPI(title="Finsight Backend API", version="1.0.0")

# Load environment variables
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL")
INTERNAL_S2S_KEY = os.getenv("INTERNAL_S2S_KEY")

class AnalyzeRequest(BaseModel):
    query: str
    # Add other fields as needed

class AnalyzeResponse(BaseModel):
    result: str
    # Add other fields as needed

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        # Forward to internal AI service or run locally
        if AGENT_SERVICE_URL:
            # Forward logic here
            pass
        else:
            # Run CrewAI analysis locally
            result = run_analysis(request.query)
            return AnalyzeResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
