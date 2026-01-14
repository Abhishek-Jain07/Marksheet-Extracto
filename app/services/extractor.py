import os
import google.generativeai as genai
from PIL import Image
from app.models import ExtractionResponse
import json

def get_model():
    """Configures and returns the Gemini model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please add it to your .env file.")
    
    genai.configure(api_key=api_key)
    
    # We use gemini-1.5-flash for low latency and cost.
    # response_schema ensures strict JSON adherence to our Pydantic model.
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": ExtractionResponse
        }
    )
    return model

async def extract_from_image(image: Image.Image) -> ExtractionResponse:
    """
    Sends the image to Gemini and returns the structured extraction data.
    """
    model = get_model()
    
    prompt = """
    You are an expert OCR and data extraction system for academic marksheets.
    Analyze the provided marksheet image and extract the data strictly according to the requested JSON schema.
    
    Guidelines:
    1. **Text Extraction**: Be precise with spelling, especially for Names and Subjects.
    2. **Structure**: 
       - Identify the Candidate Details (Name, Roll No, etc.).
       - Identify the Subject Table. Extract each row carefully into the 'subjects' list.
       - Identify the Overall Result (Pass/Fail, Division).
    3. **Confidence Scoring**:
       - Assign a confidence score (0.0 to 1.0) for each field.
       - 1.0 = Perfectly clear text.
       - < 0.8 = Blurry, ambiguous, or handwritten text.
       - < 0.5 = Guessing based on context.
    4. **Normalization**:
       - Ensure numerical values are parsed as numbers where appropriate.
       - If a field is missing or unreadable, set it to null. Do not hallucinate.
    
    Output the result matching the JSON schema.
    """
    
    try:
        response = model.generate_content([prompt, image])
        # The response.text should be valid JSON due to response_schema
        # We model_validate_json to converting it into our Pydantic object
        return ExtractionResponse.model_validate_json(response.text)
    except Exception as e:
        # Wrap API errors
        raise RuntimeError(f"AI Extraction failed: {str(e)}")
