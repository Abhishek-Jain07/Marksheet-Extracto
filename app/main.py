from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import io
from PIL import Image

# Import local modules
from app.utils import validate_file, convert_pdf_to_image, MAX_FILE_SIZE
from app.services.extractor import extract_from_image

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Marksheet Extraction API",
    description="AI-powered API to extract structured data from academic marksheets.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend demo
# Check if static directory exists first to avoid errors during initial run if manual creation skipped
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/extract", summary="Extract data from marksheet")
async def extract_marksheet(file: UploadFile = File(...)):
    """
    Upload a marksheet image (JPG, PNG) or PDF to extract structured data.
    """
    # 1. Validate File
    await validate_file(file)
    
    # Read file content
    content = await file.read()
    
    # Check size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum allowed size is 10MB.")

    # 2. Preprocess / Convert to Image
    image = None
    try:
        if file.content_type == "application/pdf":
            image = convert_pdf_to_image(content)
        else:
            image = Image.open(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")

    # 3. AI Extraction
    try:
        result = await extract_from_image(image)
        return result
    except RuntimeError as re:
        # Client-facing error for AI failure
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        # General server error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "running", "message": "Marksheet Extractor API is active. Go to /static/index.html to test."}
