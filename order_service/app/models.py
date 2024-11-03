from sqlmodel import SQLModel, Field
from typing import List, Optional

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    quantity: int
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    items: List[OrderItem] = []
    status: str
