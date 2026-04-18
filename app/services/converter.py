import os
import subprocess
import uuid
from pathlib import Path
from typing import Optional


class ConverterService:
    def __init__(self, upload_dir: str = "uploads", output_dir: str = "outputs"):
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert(self, file_path: str, target_format: str) -> Optional[str]:
        """
        Convert file to target format.
        Supports: docx, pdf, md
        """
        file_path = Path(file_path)
        source_format = file_path.suffix.lower().replace(".", "")

        if source_format == target_format:
            return str(file_path)

        output_name = f"{file_path.stem}_{uuid.uuid4().hex[:8]}.{target_format}"
        output_path = self.output_dir / output_name

        try:
            if source_format == "docx" and target_format == "pdf":
                return self._convert_docx_to_pdf(file_path, output_path)
            elif source_format == "pdf" and target_format == "docx":
                return self._convert_pdf_to_docx(file_path, output_path)
            elif source_format == "md":
                return self._convert_md(file_path, output_path, target_format)
            elif target_format == "md":
                return self._convert_to_md(file_path, output_path, source_format)
            else:
                return None
        except Exception as e:
            print(f"Conversion error: {e}")
            return None

    def _convert_docx_to_pdf(self, file_path: Path, output_path: Path) -> Optional[str]:
        """Convert DOCX to PDF using docx2pdf."""
        try:
            from docx2pdf import convert
            convert(str(file_path), str(output_path))
            if output_path.exists():
                return str(output_path)
            return None
        except Exception as e:
            print(f"docx2pdf conversion error: {e}")
            return None

    def _convert_pdf_to_docx(self, file_path: Path, output_path: Path) -> Optional[str]:
        """Convert PDF to DOCX using pdf2docx."""
        try:
            from pdf2docx import Converter
            cv = Converter(str(file_path))
            cv.convert(str(output_path), start=0, end=None)
            cv.close()
            if output_path.exists():
                return str(output_path)
            return None
        except Exception as e:
            print(f"pdf2docx conversion error: {e}")
            return None

    def _convert_md(self, file_path: Path, output_path: Path, target_format: str) -> Optional[str]:
        """Convert MD to target format using Pandoc."""
        try:
            result = subprocess.run(
                ["pandoc", str(file_path), "-o", str(output_path), "-t", target_format],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and output_path.exists():
                return str(output_path)
            return None
        except Exception as e:
            print(f"Pandoc conversion error: {e}")
            return None

    def _convert_to_md(self, file_path: Path, output_path: Path, source_format: str) -> Optional[str]:
        """Convert to MD using Pandoc."""
        try:
            result = subprocess.run(
                ["pandoc", str(file_path), "-o", str(output_path), "-f", source_format, "-t", "markdown"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and output_path.exists():
                return str(output_path)
            return None
        except Exception as e:
            print(f"Pandoc conversion error: {e}")
            return None


converter_service = ConverterService()
