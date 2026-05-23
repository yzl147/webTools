from pydantic import BaseModel
from typing import Optional


class ConvertRequest(BaseModel):
    source_format: str
    target_format: str


class ProcessResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    file_name: Optional[str] = None
