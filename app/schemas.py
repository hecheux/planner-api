from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)
    status: Literal["pending", "in_progress", "done"] = "pending"
    category: Literal["study", "work", "personal"] = "personal"
    deadline: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)
    status: Optional[Literal["pending", "in_progress", "done"]] = None
    category: Optional[Literal["study", "work", "personal"]] = None
    deadline: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    category: str
    deadline: Optional[date]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)