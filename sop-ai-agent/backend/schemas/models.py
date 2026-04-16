from pydantic import BaseModel
from typing import Optional, Any

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class NotificationPayload(BaseModel):
    person_in_charge: str
    role: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    chart: Optional[Any] = None
    report: Optional[str] = None
    notification: Optional[NotificationPayload] = None
    intent: str
