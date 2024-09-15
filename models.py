from pydantic import BaseModel
from typing import Optional, Dict

class SearchRequest(BaseModel):
    user_id: str
    text: str
    top_k: int = 5
    threshold: float = 0.5

class Document(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
