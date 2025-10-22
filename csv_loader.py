import pandas as pd
from functools import lru_cache

REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

class CSVLoaderError(Exception):
    pass

def validate_columns(df: pd.DataFrame):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise CSVLoaderError(f"Missing required columns: {missing}")

def clean_dataframe(df: pd.DataFrame):
    df = df.dropna(subset=REQUIRED_COLUMNS)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close", "volume"])
    return df

def normalize_dataframe(df: pd.DataFrame, timezone="UTC"):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert(timezone)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

@lru_cache(maxsize=32)
def load_csv(path: str, timezone="UTC") -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise CSVLoaderError(f"Error reading CSV: {e}")

    validate_columns(df)
    df = clean_dataframe(df)
    df = normalize_dataframe(df, timezone)
    return df
