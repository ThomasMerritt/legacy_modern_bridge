from datetime import date

def normalize_ledger_row(model):
    dept = model.dept_code.upper()
    gl   = model.gl_code.upper()
    txn_date = model.txn_date  
    fiscal_month = f"{txn_date.year}-{txn_date.month:02d}"
    return {
        "txn_id": model.txn_id,
        "txn_data": txn_date.isoformat(),
        "dept_code": dept,
        "gl_code": gl,
        "amount": float(model.amount),
        "currency": model.currency,
        "description": model.description.strip(),
        "fiscal_month": fiscal_month
    }