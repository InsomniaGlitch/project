# src/model.py
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

MODEL_PATH = "models/logistic_regression_model.pkl"


def create_training_data(df):
    dropped_out = (
        (df['attendance_rate'] < 60) |
        (df['avg_grade'] < 50) |
        (df['missed_assignments'] > 6)
    ).astype(int)
    X = df[['attendance_rate',
            'avg_grade',
            'missed_assignments',
            'login_frequency']]
    return X, dropped_out


def train_and_save_model():
    """Обучает и сохраняет модель."""
    df_train = pd.read_csv("data/input.csv")
    X, y = create_training_data(df_train)

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(random_state=42))
    ])

    model.fit(X, y)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Модель сохранена в {MODEL_PATH}")


def load_model():
    """Загружает модель или обучает, если не существует."""
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)


def predict_risk(model, X):
    """Предсказывает вероятность отчисления."""
    proba = model.predict_proba(X)[:, 1]
    return np.round(proba, 3)
