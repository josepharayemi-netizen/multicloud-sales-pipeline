from pathlib import Path

import pandas as pd

from src.pipeline import run, transform


def test_transform_calculates_metrics_and_rejects_bad_rows():
    frame = pd.DataFrame([
        {"transaction_id": "T1", "order_date": "2026-01-01", "region": "West", "product": "Laptop", "quantity": 2, "unit_price": 1000, "unit_cost": 700},
        {"transaction_id": "T2", "order_date": "bad", "region": "East", "product": "Mouse", "quantity": 1, "unit_price": 20, "unit_cost": 10},
    ])
    clean, rejected = transform(frame)
    assert clean.iloc[0]["revenue"] == 2000
    assert clean.iloc[0]["profit"] == 600
    assert rejected.iloc[0]["rejection_reason"] == "invalid_date"


def test_pipeline_writes_outputs(tmp_path: Path):
    source = tmp_path / "sales.csv"
    pd.DataFrame([{"transaction_id": "T1", "order_date": "2026-01-01", "region": "West", "product": "Laptop", "quantity": 1, "unit_price": 10, "unit_cost": 5}]).to_csv(source, index=False)
    result = run(source, tmp_path / "out", tmp_path / "sales.db")
    assert result["accepted_rows"] == 1
    assert (tmp_path / "out" / "clean_sales.csv").exists()
    assert (tmp_path / "sales.db").exists()
