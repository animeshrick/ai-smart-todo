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
    due_date: Optional[List[datetime]] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    is_active: bool

    def __init__(self, with_id: bool = True, **kwargs):
        if not with_id:
            kwargs["id"] = None
        if kwargs.get("tags"):
            tags_dict = kwargs["author"].model_to_dict()

        super().__init__(**kwargs)


class ExportTaskList(BaseModel):
    subject_list: List[ExportTask]
