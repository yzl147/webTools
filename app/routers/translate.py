import os
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

from app.services.translator import translator_service

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/translate")
async def translate_file(
    file: UploadFile = File(...),
    mode: str = Form(...),
    target_language: str = Form(...),
    # LibreTranslate config
    lt_host: Optional[str] = Form(None),
    lt_port: Optional[int] = Form(None),
    lt_api_key: Optional[str] = Form(None),
    # LLM config
    llm_type: Optional[str] = Form(None),
    api_base: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
):
    """
    Translate uploaded file using specified translation mode.
    """
    file_ext = Path(file.filename).suffix.lower().replace(".", "")
    if file_ext not in ["pdf", "docx", "md"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}")

    if mode not in ["libretranslate", "llm"]:
        raise HTTPException(status_code=400, detail=f"Unknown translation mode: {mode}")

    if mode == "libretranslate" and not lt_host:
        raise HTTPException(status_code=400, detail="LibreTranslate host is required")

    if mode == "llm":
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required for LLM translation")
        if not model:
            raise HTTPException(status_code=400, detail="Model name is required for LLM translation")
        if not llm_type:
            raise HTTPException(status_code=400, detail="LLM type (openai/anthropic) is required")

    unique_id = uuid.uuid4().hex[:8]
    input_path = UPLOAD_DIR / f"{unique_id}_{file.filename}"

    try:
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        translated_path, message = translator_service.translate_file(
            file_path=str(input_path),
            file_extension=file_ext,
            mode=mode,
            target_language=target_language,
            lt_host=lt_host,
            lt_port=lt_port,
            lt_api_key=lt_api_key,
            llm_type=llm_type,
            api_base=api_base,
            api_key=api_key,
            model=model,
        )

        if not translated_path or not Path(translated_path).exists():
            raise HTTPException(status_code=500, detail=message)

        output_filename = f"translated_{Path(file.filename).stem}.{file_ext}"

        return FileResponse(
            path=translated_path,
            filename=output_filename,
            media_type="application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")
    finally:
        if input_path.exists():
            os.unlink(input_path)
