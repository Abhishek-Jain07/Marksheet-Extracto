from pydantic import BaseModel, Field
from typing import List, Optional

class Score(BaseModel):
    obtained: Optional[float] = Field(None, description="Marks or credits obtained")
    max_marks: Optional[float] = Field(None, description="Maximum marks or credits possible")
    grade: Optional[str] = Field(None, description="Grade received if applicable")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for this extraction")

class Subject(BaseModel):
    name: str = Field(..., description="Name of the subject")
    marks: Score = Field(..., description="Marks details for the subject")
    credits: Optional[Score] = Field(None, description="Credits details if applicable")

class CandidateDetails(BaseModel):
    name: Optional[str] = Field(None, description="Candidate's full name")
    father_name: Optional[str] = Field(None, description="Father's name")
    mother_name: Optional[str] = Field(None, description="Mother's name")
    roll_no: Optional[str] = Field(None, description="Roll number")
    registration_no: Optional[str] = Field(None, description="Registration number")
    dob: Optional[str] = Field(None, description="Date of birth")
    exam_year: Optional[str] = Field(None, description="Year of examination")
    board_university: Optional[str] = Field(None, description="Board or University name")
    institution: Optional[str] = Field(None, description="Institution or School name")
    confidence: float = Field(..., ge=0, le=1, description="Average confidence for candidate details")

class ExtractionResponse(BaseModel):
    candidate: CandidateDetails
    subjects: List[Subject]
    overall_result: Optional[str] = Field(None, description="Overall result/division/grade like 'PASS', 'First Division'")
    issue_date: Optional[str] = Field(None, description="Date of issue of the marksheet")
    issue_place: Optional[str] = Field(None, description="Place of issue if available")
    average_confidence: float = Field(..., ge=0, le=1, description="Overall confidence score for the entire document")
