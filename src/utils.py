import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Загрузка данных из CSV."""
    return pd.read_csv(path)


def save_predictions(names, risks, output_path: str):
    """Сохранение результата."""
    df = pd.DataFrame({"name": names, "dropout_risk": risks})
    df.to_csv(output_path, index=False)
