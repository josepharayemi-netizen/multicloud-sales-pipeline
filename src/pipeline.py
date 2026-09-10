from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "transaction_id", "order_date", "region", "product",
    "quantity", "unit_price", "unit_cost",
}


def transform(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Validate transactions and return clean and rejected records."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    data = frame.copy()
    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    for column in ("quantity", "unit_price", "unit_cost"):
        data[column] = pd.to_numeric(data[column], errors="coerce")

    duplicate = data["transaction_id"].duplicated(keep="first")
    missing_text = data[["transaction_id", "region", "product"]].isna().any(axis=1)
    invalid_date = data["order_date"].isna()
    invalid_numbers = (
        data[["quantity", "unit_price", "unit_cost"]].isna().any(axis=1)
        | (data["quantity"] <= 0)
        | (data["unit_price"] < 0)
        | (data["unit_cost"] < 0)
    )
    invalid = duplicate | missing_text | invalid_date | invalid_numbers

    rejected = data.loc[invalid].copy()
    reasons = pd.Series("", index=data.index)
    reasons.loc[duplicate] += "duplicate_transaction;"
    reasons.loc[missing_text] += "missing_required_text;"
    reasons.loc[invalid_date] += "invalid_date;"
    reasons.loc[invalid_numbers] += "invalid_numeric_value;"
    rejected["rejection_reason"] = reasons.loc[invalid].str.rstrip(";")

    clean = data.loc[~invalid].copy()
    clean["quantity"] = clean["quantity"].astype(int)
    clean["revenue"] = (clean["quantity"] * clean["unit_price"]).round(2)
    clean["profit"] = (clean["quantity"] * (clean["unit_price"] - clean["unit_cost"])).round(2)
    clean["order_date"] = clean["order_date"].dt.strftime("%Y-%m-%d")
    return clean, rejected


def load_sqlite(clean: pd.DataFrame, database: Path) -> None:
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute("DROP TABLE IF EXISTS sales")
        clean.to_sql("sales", connection, index=False)
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_sales_id ON sales(transaction_id)")


def run(input_path: Path, output_dir: Path, database: Path) -> dict[str, float | int]:
    frame = pd.read_csv(input_path)
    clean, rejected = transform(frame)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_dir / "clean_sales.csv", index=False)
    rejected.to_csv(output_dir / "rejected_sales.csv", index=False)
    load_sqlite(clean, database)
    return {
        "input_rows": len(frame),
        "accepted_rows": len(clean),
        "rejected_rows": len(rejected),
        "revenue": round(float(clean["revenue"].sum()), 2),
        "profit": round(float(clean["profit"].sum()), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Process retail sales data")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    parser.add_argument("--database", type=Path, default=Path("data/sales.db"))
    args = parser.parse_args()
    print(run(args.input, args.output, args.database))


if __name__ == "__main__":
    main()
