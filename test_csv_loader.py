import pytest
import pandas as pd
from io import StringIO
from csv_loader import load_csv, CSVLoaderError

VALID_CSV = """timestamp,open,high,low,close,volume
2025-10-12 10:00:00,100,105,95,102,1000
2025-10-12 11:00:00,102,106,101,104,1500
"""

MISSING_COL_CSV = """timestamp,open,high,close,volume
2025-10-12 10:00:00,100,105,102,1000
"""

CORRUPT_CSV = """timestamp,open,high,low,close,volume
2025-10-12 10:00:00,100,105,95,abc,1000
"""

def test_valid_csv(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(VALID_CSV)
    df = load_csv(str(csv_file))
    assert not df.empty
    assert all(col in df.columns for col in ["timestamp", "open", "high", "low", "close", "volume"])

def test_missing_columns(tmp_path):
    csv_file = tmp_path / "missing.csv"
    csv_file.write_text(MISSING_COL_CSV)
    try:
        load_csv(str(csv_file))
    except CSVLoaderError as e:
        assert "Missing required columns" in str(e)

def test_corrupt_rows(tmp_path):
    csv_file = tmp_path / "corrupt.csv"
    csv_file.write_text(CORRUPT_CSV)
    df = load_csv(str(csv_file))
    assert "abc" not in df["close"].values
