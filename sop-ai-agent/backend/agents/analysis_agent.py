import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import settings
from agents.data_query_agent import run_data_query
from utils.logger import get_logger

logger = get_logger("analysis_agent")

def run_deep_analysis(user_message: str, history_str: str = "") -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "deep_analysis.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    # Step 1: Pre-aggregation via standard data query agent for raw stats (Multi-hop emulation)
    logger.info("Deep Analysis Node evaluating context data requirements...")
    raw_aggregated_data = run_data_query(user_message, history_str)

    # Step 2: Push aggregated stats into the analytical evaluator
    system_prompt = prompt_text.replace("{raw_data}", raw_aggregated_data).replace("{history}", history_str)
    
    llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY, temperature=0.3)
    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser Request: {user_message}")
    
    chain = prompt | llm
    
    logger.info("Executing complex reasoning framework over extracted context...")
    try:
        result = chain.invoke({"system_prompt": system_prompt, "user_message": user_message})
        return result.content.strip()
    except Exception as e:
        logger.error(f"Error during deep analysis LLM invocation: {e}")
        return "Failed to complete deep analytical reasoning."
