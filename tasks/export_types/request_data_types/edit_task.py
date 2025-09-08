from typing import Optional
import datetime
from pydantic import BaseModel


class EditTaskRequestType(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    category:  Optional[str] = None
    status:  Optional[str] = None
    priority:  Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
