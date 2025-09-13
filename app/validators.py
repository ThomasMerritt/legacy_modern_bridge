# validators.py
from pydantic import BaseModel, Field, validator
from datetime import date

class LedgerRow(BaseModel):
    txn_id: int
    txn_date: date
    dept_code: str
    gl_code: str
    amount: float
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    description: str

    @validator("dept_code", "gl_code")
    def upper_codes(cls, v): return v.upper()