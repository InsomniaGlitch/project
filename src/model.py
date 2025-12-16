import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def predict_dropout_risk(df: dict) -> list:
    """
    Упрощённая модель на основе Isolation Forest + ручных правил.
    В реальности можно заменить на Logistic Regression или XGBoost.
    """
    features = np.array([
        df['attendance_rate'] / 100.0,
        df['avg_grade'] / 100.0,
        df['missed_assignments'] / 10.0,
        df['login_frequency'] / 5.0
    ]).T

    # Нормализация
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Модель аномалий (низкие показатели = аномалии = риск отчисления)
    model = IsolationForest(contamination=0.2, random_state=42)
    anomaly_scores = model.fit_predict(features_scaled)
    anomaly_proba = (anomaly_scores == -1).astype(float)  # 1 = высокий риск

    # Добавим простую логику
    manual_risk = (
        (df['attendance_rate'] < 60) |
        (df['avg_grade'] < 50) |
        (df['missed_assignments'] > 5)
    ).astype(float)

    # Комбинируем
    combined_risk = np.clip((anomaly_proba * 0.6 + manual_risk * 0.4), 0, 1)
    return np.round(combined_risk, 3).tolist()
