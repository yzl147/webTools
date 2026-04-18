import os
import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from app.services.converter import converter_service

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    """
    Convert uploaded file to target format.
    """
    allowed_formats = ["pdf", "docx", "md"]
    if target_format not in allowed_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported target format: {target_format}")

    file_ext = Path(file.filename).suffix.lower().replace(".", "")
    if file_ext not in ["pdf", "docx", "md"]:
        raise HTTPException(status_code=400, detail=f"Unsupported source format: {file_ext}")

    unique_id = uuid.uuid4().hex[:8]
    input_path = UPLOAD_DIR / f"{unique_id}_{file.filename}"
    output_format = target_format

    try:
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        converted_path = converter_service.convert(str(input_path), output_format)

        if not converted_path or not Path(converted_path).exists():
            raise HTTPException(status_code=500, detail="Conversion failed")

        output_filename = Path(file.filename).stem + "." + output_format

        return FileResponse(
            path=converted_path,
            filename=output_filename,
            media_type="application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
    finally:
        if input_path.exists():
            os.unlink(input_path)
