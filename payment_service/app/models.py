from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int
    amount: float
    status: str
    payment_method: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
