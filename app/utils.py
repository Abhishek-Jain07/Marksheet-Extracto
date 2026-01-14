import io
import fitz  # PyMuPDF
from PIL import Image
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

async def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, WEBP, and PDF are allowed.")
    
    # Check size (requires reading the stream or checking headers if trustworthy, reading is safer for small limit)
    # Since we need to read it anyway, we can check size after reading.
    return True

def convert_pdf_to_image(pdf_bytes: bytes) -> Image.Image:
    """
    Converts the first page of a PDF to a PIL Image.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if doc.page_count < 1:
            raise ValueError("PDF has no pages.")
        
        page = doc[0]  # Get first page
        pix = page.get_pixmap(dpi=150) # moderate DPI for LLM
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")
