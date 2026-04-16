import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.chat import router as chat_router
from data_loader.loader import load_sales_data
from config import settings
from utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(title="S&OP AI Agent MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Loading data from {settings.DATA_DIR}...")
    load_sales_data(settings.DATA_DIR)
    logger.info("Data loaded and cached successfully.")

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
