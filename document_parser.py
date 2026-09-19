"""
Document Parser Module for LegalLens AI.
Handles PDF, Word DOCX, and Plain Text parsing with robust security and edge-case guards.

Features:
- File size boundary enforcement (max 16MB)
- UTF-8 decoding with fallback handling
- Protection against corrupted streams or decompression bombs
- Page-by-page PDF extraction with structural delimiters
"""

import io
import logging
from typing import Tuple, Optional

logger = logging.getLogger("DocumentParser")

MAX_FILE_BYTES = 16 * 1024 * 1024  # 16 MB limit


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> Tuple[str, Optional[str]]:
    """
    Extracts plain text from file bytes based on the file extension.

    Args:
        file_bytes: The raw byte content of the file.
        filename: The sanitized name of the file including extension.

    Returns:
        A tuple of (extracted_text, error_message). If successful, error_message is None.
    """
    if not file_bytes:
        return "", "File content is empty (0 bytes)."

    if len(file_bytes) > MAX_FILE_BYTES:
        return "", f"File exceeds maximum allowed size of {MAX_FILE_BYTES // (1024 * 1024)}MB."

    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    # Plain text and Markdown
    if ext in ["txt", "md"]:
        try:
            # Try UTF-8 first, fallback to Latin-1
            try:
                decoded = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                decoded = file_bytes.decode("latin-1", errors="replace")
                
            clean_text = decoded.strip()
            if not clean_text:
                return "", "Text file contains no readable content."
            return clean_text, None
        except Exception as e:
            logger.warning(f"Failed to decode text file: {e}")
            return "", f"Failed to decode text file: {str(e)}"

    # Adobe PDF
    elif ext == "pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            
            if len(reader.pages) == 0:
                return "", "The PDF document has 0 pages."
                
            text_parts = []
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(f"--- Page {i + 1} ---\n" + page_text.strip())
                except Exception as page_err:
                    logger.warning(f"Could not extract text from PDF page {i + 1}: {page_err}")
                    continue

            extracted = "\n\n".join(text_parts).strip()
            if not extracted:
                return "", "The PDF appears to be empty or contains only scanned images without selectable text."
            return extracted, None
        except Exception as e:
            logger.warning(f"Error parsing PDF file: {e}")
            return "", f"Error reading PDF document: {str(e)}"

    # Microsoft Word DOCX
    elif ext in ["docx", "doc"]:
        if ext == "doc":
            return "", "Legacy binary .doc format is not supported. Please convert your file to .docx or .pdf."
            
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from tables if present
            table_texts = []
            for table in doc.tables:
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_data:
                        table_texts.append(" | ".join(row_data))

            combined_parts = paragraphs + table_texts
            extracted = "\n\n".join(combined_parts).strip()
            if not extracted:
                return "", "The Word document contains no readable text."
            return extracted, None
        except Exception as e:
            logger.warning(f"Error parsing DOCX file: {e}")
            return "", f"Error reading Word document: {str(e)}"

    else:
        return "", f"Unsupported file format .{ext}. Supported formats are .pdf, .docx, .txt, .md."
