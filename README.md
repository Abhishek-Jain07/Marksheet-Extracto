# AI Marksheet Extraction API

An AI-powered FastAPI application that extracts structured data from marksheet images and PDFs using Google Gemini.

## Features
- **Accurate Extraction**: Uses LLM (Gemini 2.5 Flash) to parse candidate details, subjects, and marks.
- **Robustness**: Handles Images (JPG, PNG, WEBP) and PDFs.
- **Validation**: Enforces JSON schema using Pydantic models.
- **Confidence Scoring**: Provides confidence levels for extracted fields.
- **Demo UI**: Simple web interface for testing.

## Setup

1. **Clone/Navigate to directory**:
   ```bash
   cd Maksheet
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For PDF processing, ensure `pymupdf` is installed (included in requirements).*

3. **Environment Variables**:
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key
   ```

## Usage

### Run Server
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

### Frontend Demo
Open `http://127.0.0.1:8000/static/index.html` in your browser to inspect the UI.

### API Endpoint
**POST** `/extract`
- **Body**: `multipart/form-data` with `file` field.
- **Response**: JSON object.

### Example Response
```json
{
  "candidate": {
    "name": "John Doe",
    "roll_no": "12345",
    "confidence": 0.95
  },
  "subjects": [
    {
      "name": "Mathematics",
      "marks": {
        "obtained": 95,
        "max_marks": 100,
        "grade": "A",
        "confidence": 0.98
      }
    }
  ],
  "overall_result": "PASS",
  "average_confidence": 0.96
}
```

## Testing
Run the provided tests (requires `pytest`):
```bash
pip install pytest httpx
pytest tests/
```
