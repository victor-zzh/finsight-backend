from crewai import Crew, Process
from agents import intent_parser, data_retriever, comprehensive_analyzer
from tasks import intent_analysis_task, data_retrieval_task, comprehensive_analysis_task

# Create the sequential crew
crew = Crew(
    agents=[intent_parser, data_retriever, comprehensive_analyzer],
    tasks=[intent_analysis_task, data_retrieval_task, comprehensive_analysis_task],
    process=Process.sequential,  # Sequential assembly line
    verbose=True,
)

def run_analysis(query: str) -> str:
    """Run the financial analysis crew with the given query"""
    result = crew.kickoff(inputs={"query": query})
    return result
