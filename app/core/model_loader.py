from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL = joblib.load(BASE_DIR / "models" / "ensemble.pkl")