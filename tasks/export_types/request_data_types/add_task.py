from typing import Optional
import datetime
from pydantic import BaseModel


class AddTaskRequestType(BaseModel):
    title: str
    description: str
    category:  Optional[str] = None
    # tags are coma separated value
    tags: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
