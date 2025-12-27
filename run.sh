#!/bin/bash
python -c "from src.model import train_and_save_model; train_and_save_model()" 2>/dev/null || echo "Модель будет обучена при старте"
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload