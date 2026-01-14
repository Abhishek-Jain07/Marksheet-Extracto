import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import ExtractionResponse, CandidateDetails, Subject, Score
from unittest.mock import patch, AsyncMock
import io
from PIL import Image

client = TestClient(app)

# Dummy extraction result for mocking
dummy_response = ExtractionResponse(
    candidate=CandidateDetails(name="Test User", roll_no="123", confidence=0.9),
    subjects=[
        Subject(
            name="Math",
            marks=Score(obtained=90, max_marks=100, grade="A", confidence=0.95)
        )
    ],
    overall_result="PASS",
    average_confidence=0.92
)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

@patch("app.main.extract_from_image", new_callable=AsyncMock)
def test_extract_endpoint_image(mock_extract):
    """Test extracting from a valid image (mocked LLM)"""
    mock_extract.return_value = dummy_response
    
    # Create a dummy image in memory
    img_byte_arr = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='white')
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    files = {"file": ("test.jpg", img_byte_arr, "image/jpeg")}
    response = client.post("/extract", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["candidate"]["name"] == "Test User"
    assert data["overall_result"] == "PASS"

def test_extract_invalid_file_type():
    """Test uploading a text file"""
    files = {"file": ("test.txt", io.BytesIO(b"dummy text"), "text/plain")}
    response = client.post("/extract", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
