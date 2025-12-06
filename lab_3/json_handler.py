import json
import pandas as pd


def save_result(filename: str, result: dict):

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def read_csv(filename: str) -> pd.DataFrame:
    try:
        with open(filename, mode="r", encoding="utf-16") as file:
            df = pd.read_csv(file, delimiter=";")
            return df
    except Exception as exc:
        print(f"Error reading CSV: {exc}")
        return pd.DataFrame()

def read_json(filename: str) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
