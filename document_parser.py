"""
Document Parser Module for LegalLens AI.
Supports PDF, DOCX, and Plain Text parsing.
"""

import io
from typing import Tuple, Optional

def extract_text_from_bytes(file_bytes: bytes, filename: str) -> Tuple[str, Optional[str]]:
    """
    Extracts text from uploaded file bytes according to file extension.
    Returns (extracted_text, error_message).
    """
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    if ext == 'txt' or ext == 'md':
        try:
            return file_bytes.decode('utf-8', errors='replace'), None
        except Exception as e:
            return "", f"Failed to decode text file: {str(e)}"
            
    elif ext == 'pdf':
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {i+1} ---\n" + page_text)
            extracted = "\n\n".join(text_parts).strip()
            if not extracted:
                return "", "The PDF appears to be empty or consists of scanned images without text."
            return extracted, None
        except Exception as e:
            return "", f"Error reading PDF: {str(e)}"
            
    elif ext in ['docx', 'doc']:
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            extracted = "\n\n".join(paragraphs).strip()
            if not extracted:
                return "", "The Word document appears to be empty."
            return extracted, None
        except Exception as e:
            return "", f"Error reading Word document: {str(e)}"
            
    else:
        # Fallback: try decoding as UTF-8
        try:
            return file_bytes.decode('utf-8', errors='replace'), None
        except Exception as e:
            return "", f"Unsupported file type .{ext}: {str(e)}"
