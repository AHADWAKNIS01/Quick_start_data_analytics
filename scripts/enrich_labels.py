"""Enrich an existing Couchbase batch without rerunning Spark aggregations."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.app.db import collection

def main():
    col = collection()
    mode = col.get("quickcart::metadata").content_as[dict]["dataset"]
    folder = Path(__file__).resolve().parents[1] / "data" / mode
    with (folder / "departments.csv").open(encoding="utf-8", newline="") as source:
        names = {int(row["department_id"]): row["department"] for row in csv.DictReader(source)}
    with (folder / "products.csv").open(encoding="utf-8", newline="") as source:
        products = {int(row["product_id"]): int(row["department_id"]) for row in csv.DictReader(source)}
    for key in ("departments", "products"):
        document = col.get("quickcart::" + key).content_as[dict]
        for row in document["data"]:
            if key == "products":
                row["department_id"] = products[row["product_id"]]
            try:
                row["department_id"] = int(row["department_id"])
            except (ValueError, TypeError):
                row["department"] = "Invalid source category"
                continue
            row["department"] = names.get(row["department_id"], "Unknown source category")
        col.upsert("quickcart::" + key, document)
    print("Department names and product departments saved to Couchbase.")

if __name__ == "__main__":
    main()
