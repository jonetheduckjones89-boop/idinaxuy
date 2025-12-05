from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Action(BaseModel):
    id: str
    title: str
    priority: str
    details: str
    effort: str

class Lab(BaseModel):
    name: str
    value: str
    unit: str
    normalRange: str

class PatientDetails(BaseModel):
    name: str
    dob: str
    encounterDates: List[str]
    medications: List[str]
    diagnoses: List[str]
    labs: List[Lab]
    attending: str

class RiskFlag(BaseModel):
    id: str
    severity: str
    message: str

class Stats(BaseModel):
    wordCount: int
    sections: int
    readingScore: float
    confidence: float

class AnalysisResult(BaseModel):
    jobId: str
    filename: str
    uploadedAt: str
    summary: str
    topActions: List[Action]
    patientDetails: PatientDetails
    riskFlags: List[RiskFlag]
    suggestions: List[str]
    stats: Stats

class ChatRequest(BaseModel):
    jobId: str
    message: str
    history: List[Dict[str, str]]

class RewriteRequest(BaseModel):
    text: str
    style: str

class NextStepsRequest(BaseModel):
    jobId: str

class ProcessDocumentResponse(BaseModel):
    jobId: str
    status: str
    data: Optional[AnalysisResult] = None
