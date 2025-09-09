from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class ExportTask(BaseModel):
    id: Optional[UUID]
    title: str
    description: str
    status: str
    priority: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    is_active: bool
    
    def __init__(self, **kwargs):
        # Check if 'tags' exists and is a string in the incoming data
        if "tags" in kwargs and isinstance(kwargs.get("tags"), str):
            tags_string = kwargs["tags"]
            # Split the string, strip whitespace, and filter out empty parts.
            # This correctly turns an empty string '' into an empty list [].
            kwargs["tags"] = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        super().__init__(**kwargs)


class ExportTaskList(BaseModel):
    subject_list: List[ExportTask]
