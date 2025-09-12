# loader.py
import csv
from datetime import datetime
from pathlib import Path
from app.validators import LedgerRow
from app.transform import normalize_ledger_row
from app.models import insert_ledger_rows, begin_load

def load_ledger_csv(csv_path: str):
    csv_path = Path(csv_path)
    source_tag = f"{csv_path.stem}@{datetime.now(datetime.timezone.utc).isoformat()}Z"
    load_id = begin_load(source_tag, schema_version="ledger_v1")

    valid_rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            model = LedgerRow(**raw)              
            norm = normalize_ledger_row(model)    
            valid_rows.append(norm)

    insert_ledger_rows(load_id, valid_rows)
    return load_id, len(valid_rows), source_tag

