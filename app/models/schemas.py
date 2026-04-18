from pydantic import BaseModel
from typing import Optional


class TranslateRequest(BaseModel):
    mode: str  # "libretranslate" or "llm"
    file_extension: str
    target_language: str
    # LibreTranslate config
    lt_host: Optional[str] = None
    lt_port: Optional[int] = None
    lt_api_key: Optional[str] = None
    # LLM config
    llm_type: Optional[str] = None  # "openai" or "anthropic"
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None


class ConvertRequest(BaseModel):
    source_format: str
    target_format: str


class ProcessResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    file_name: Optional[str] = None
