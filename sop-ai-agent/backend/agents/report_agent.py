import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import settings
from agents.data_query_agent import run_data_query

def run_report(user_message: str) -> dict:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "report_writer.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    # Step 1: Use the data_query agent purely to fetch raw contextual pandas data
    raw_data_context = run_data_query(user_message)

    # Step 2: Use the report_writer prompt to digest data & format as JSON
    llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY, temperature=0.2)
    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser Request: {user_message}")
    
    chain = prompt | llm
    
    system_prompt = prompt_text.replace("{raw_data}", raw_data_context)
    result = chain.invoke({"system_prompt": system_prompt, "user_message": user_message})
    
    try:
        content = result.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return json.loads(content.strip())
    except Exception as e:
        print(f"Error parsing JSON from report LLM: {e}")
        return {
            "bot_message": "Failed to extract insights cleanly.",
            "markdown_report": f"# Error Processing Report\nAn error occurred while compiling the markdown context.\n\nRaw Context Extracted:\n{raw_data_context}"
        }
