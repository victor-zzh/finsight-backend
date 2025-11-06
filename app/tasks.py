from crewai import Task
from agents import intent_parser, data_retriever, comprehensive_analyzer
from prompts import INTENT_ANALYSIS_PROMPT, COMPREHENSIVE_ANALYSIS_PROMPT

# Task 1: Intent Analysis
intent_analysis_task = Task(
    description="Analyze the user's financial query to understand their intent and extract key parameters.",
    expected_output="A structured summary of the query intent, including companies, time periods, and analysis type.",
    agent=intent_parser,
)

# Task 2: Data Retrieval
data_retrieval_task = Task(
    description="Retrieve all relevant financial data based on the intent analysis, including structured data, qualitative info, and real-time quotes.",
    expected_output="A comprehensive dataset containing all relevant financial information for the analysis.",
    agent=data_retriever,
    context=[intent_analysis_task],  # Depends on intent analysis
)

# Task 3: Comprehensive Analysis
comprehensive_analysis_task = Task(
    description="Perform comprehensive financial analysis based on retrieved data, providing objective and traceable insights.",
    expected_output="A detailed financial analysis report in structured JSON format.",
    agent=comprehensive_analyzer,
    context=[data_retrieval_task],  # Depends on data retrieval
)
