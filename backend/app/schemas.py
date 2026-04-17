from pydantic import BaseModel, Field


class ConsultationRequest(BaseModel):
    notes: str = Field(..., min_length=10, max_length=10_000)


class ConsultationResponse(BaseModel):
    summary: str
    next_steps: str
    patient_email: str
