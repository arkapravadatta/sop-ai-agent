import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import settings
from data_loader.loader import load_sales_data
from tools.plotly_tool import execute_plotly_code

def run_visualization(user_message: str) -> dict | None:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "visualization.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    df, schema = load_sales_data(settings.DATA_DIR)
    
    system_prompt = prompt_text.replace("{schema}", schema)
    
    llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY, temperature=0.0)
    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser Request: {user_message}")
    
    chain = prompt | llm
    result = chain.invoke({"system_prompt": system_prompt, "user_message": user_message})
    
    code = result.content.strip()
    chart_json = execute_plotly_code(code, df)
    return chart_json
