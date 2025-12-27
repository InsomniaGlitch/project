from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import List
import pandas as pd
from .utils import save_predictions

from .model import load_model, predict_risk
from .schema import StudentInput, PredictionResponse


# Управление жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Загрузка модели при старте
    global model
    model = load_model()
    print("The model was loaded.")
    yield
    # Здесь можно добавить очистку при завершении (опционально)
    print("Stopped.")


app = FastAPI(
    title="Student Dropout Risk Prediction API",
    description=(
        "API для прогнозирования риска отчисления студентов с использованием "
        "Logistic Regression."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# Глобальная переменная для модели
model = None


@app.post("/predict", response_model=PredictionResponse)
def predict(students: List[StudentInput]):
    df = pd.DataFrame(
        [
            s.model_dump()
            if hasattr(s, "model_dump")
            else s.dict()
            for s in students
        ]
    )

    columns = [
        'attendance_rate',
        'avg_grade',
        'missed_assignments',
        'login_frequency',
    ]

    X = df[columns]

    risks = predict_risk(model, X)
    result = [
        {"name": row["name"], "dropout_risk": risk}
        for row, risk in zip(df.to_dict("records"), risks)
    ]

    # Сохраняем результат
    save_predictions(
        [r["name"] for r in result],
        [r["dropout_risk"] for r in result],
        "data/output.csv",
    )

    return {"predictions": result}


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "API работает. Используй /docs для просмотра документации.",
    }
