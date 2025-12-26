from pydantic import BaseModel
from typing import List


class StudentInput(BaseModel):
    student_id: int
    name: str
    attendance_rate: float
    avg_grade: float
    missed_assignments: int
    login_frequency: float


class StudentOutput(BaseModel):
    name: str
    dropout_risk: float


class PredictionResponse(BaseModel):
    predictions: List[StudentOutput]
