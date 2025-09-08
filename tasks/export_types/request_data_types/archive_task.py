from pydantic import BaseModel


class ArchiveTaskRequestType(BaseModel):
    id: str
