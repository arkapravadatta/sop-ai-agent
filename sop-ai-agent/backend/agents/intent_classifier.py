import json
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import settings

def classify_intent(user_message: str, history_str: str = "") -> dict:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "intent_classifier.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    prompt_text = prompt_text.replace("{history}", history_str)
    
    llm = ChatOpenAI(model=settings.MODEL_NAME, api_key=settings.OPENAI_API_KEY, temperature=0.0)
    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser Message: {user_message}")
    
    chain = prompt | llm
    result = chain.invoke({"system_prompt": prompt_text, "user_message": user_message})
    
    content = result.content.strip().replace('```json', '').replace('```', '').strip()
    try:
        return json.loads(content)
    except:
        return {"intent": "general", "requires_notification": False, "region_mentioned": None}
