from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def kpis(database: Path) -> dict[str, object]:
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        totals = connection.execute(
            "SELECT COUNT(*) orders, ROUND(SUM(revenue),2) revenue, "
            "ROUND(SUM(profit),2) profit, ROUND(AVG(revenue),2) average_order_value FROM sales"
        ).fetchone()
        top_region = connection.execute(
            "SELECT region, ROUND(SUM(revenue),2) revenue FROM sales GROUP BY region ORDER BY revenue DESC LIMIT 1"
        ).fetchone()
        top_product = connection.execute(
            "SELECT product, ROUND(SUM(revenue),2) revenue FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 1"
        ).fetchone()
    return {**dict(totals), "top_region": dict(top_region), "top_product": dict(top_product)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("data/sales.db"))
    args = parser.parse_args()
    for key, value in kpis(args.database).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
