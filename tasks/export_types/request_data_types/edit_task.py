from typing import Optional, List
from pydantic import BaseModel


class EditTaskRequestType(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    is_active: Optional[bool] = None
