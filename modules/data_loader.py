import pandas as pd
import os

DATA_PATH = os.path.join("data", "breaches.csv")


def load_data():
    """
    Loads breach dataset and validates required structure.
    """

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Dataset not found at data/breaches.csv")

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "email",
        "domain",
        "breach",
        "breach_date",
        "attack_type",
        "data_exposed",
        "password_hint",
        "password_exposed"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Normalize for search
    df["email"] = df["email"].str.lower().str.strip()
    df["domain"] = df["domain"].str.lower().str.strip()

    return df