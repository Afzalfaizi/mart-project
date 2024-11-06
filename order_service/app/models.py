from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSON

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    quantity: int
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    items: list[OrderItem] = Field(default_factory=list, sa_column=Column(JSON))
    status: str
