import os
import json
import csv
from backend.quote_adapter import quote_all


from datetime import datetime

EXPORT_ROOT = "C:/Curbonomix/curbonomix-public/exports/quotes"

def export_json(quotes):
    out_dir = f"{EXPORT_ROOT}/{datetime.today().strftime('%Y-%m-%d')}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/quotes.json"
    with open(out_path, "w") as f:
        json.dump(quotes, f, indent=2)
    print(f"✅ JSON exported: {out_path}")

def export_csv(quotes):
    out_dir = f"{EXPORT_ROOT}/{datetime.today().strftime('%Y-%m-%d')}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/quotes.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=quotes[0].keys())
        writer.writeheader()
        writer.writerows(quotes)
    print(f"✅ CSV exported: {out_path}")

quotes = quote_all()
export_json(quotes)
export_csv(quotes)
