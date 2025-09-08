from typing import Optional, List
from pydantic import BaseModel


class AddTaskRequestType(BaseModel):
    title: str
    description: str
    category:  Optional[str] = None
    # tags are coma separated value
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
