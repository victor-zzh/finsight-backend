from crewai import Agent
from langchain_openai import ChatOpenAI
from prompts import INTENT_ANALYSIS_PROMPT, COMPREHENSIVE_ANALYSIS_PROMPT
from tools.db_tools import *
from tools.rag_tools import *
from tools.realtime_tools import *

# Initialize LLMs
fast_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)  # For Agent 1
powerful_llm = ChatOpenAI(model="gpt-4", temperature=0.2)  # For Agent 3

# Agent 1: Intent Parser
intent_parser = Agent(
    role="Intent Analyzer",
    goal="Analyze user query and determine intent for financial analysis",
    backstory="You are an expert in understanding financial queries and extracting key information.",
    llm=fast_llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 2: Data Retriever
data_retriever = Agent(
    role="Data Retriever",
    goal="Retrieve relevant financial data from databases and vector stores",
    backstory="You are skilled at querying structured and unstructured financial data.",
    llm=fast_llm,  # Or use a simple LLM if needed
    tools=[
        get_financial_trends,
        get_company_comparison,
        search_qualitative_info,
        get_realtime_quotes,
    ],
    verbose=True,
    allow_delegation=False,
)

# Agent 3: Comprehensive Analyzer
comprehensive_analyzer = Agent(
    role="Financial Analyst",
    goal="Provide comprehensive, factual financial analysis based on retrieved data",
    backstory="You are a senior financial analyst who provides objective, traceable insights.",
    llm=powerful_llm,
    verbose=True,
    allow_delegation=False,
)
