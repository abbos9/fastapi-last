from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
import json

class BookCreateSchema(BaseModel):
    id: int  # Adding an ID field
    name: str
    author: str
    is_active: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True

    @root_validator(pre=True)
    def update_timestamp(cls, values):
        values["updated_at"] = datetime.now()
        return values

class BookResponseSchema(BaseModel):
    id: int  # Adding an ID field
    name: str
    author: str
    created_at: str  # Converting datetime to string
    updated_at: str  # Converting datetime to string

    @root_validator(pre=True)
    def serialize_datetimes(cls, values):
        # Ensure created_at and updated_at are strings
        if isinstance(values.get("created_at"), datetime):
            values['created_at'] = values['created_at'].isoformat()
        if isinstance(values.get("updated_at"), datetime):
            values['updated_at'] = values['updated_at'].isoformat()
        return values