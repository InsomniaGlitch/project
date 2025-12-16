from utils import load_data, save_predictions
from model import predict_dropout_risk

INPUT_PATH = "data/input.csv"
OUTPUT_PATH = "data/output.csv"


def main():
    df = load_data(INPUT_PATH)
    risk_scores = predict_dropout_risk(df)
    save_predictions(df['name'], risk_scores, OUTPUT_PATH)
    print(f"Результат сохранён в {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
