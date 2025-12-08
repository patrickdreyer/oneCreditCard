from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:  # pylint: disable=too-many-instance-attributes
    category: str
    merchant: str
    date: datetime
    time: Optional[str]
    location: Optional[str]
    amount: float
    foreignAmount: Optional[float] = None
    foreignCurrency: Optional[str] = None

    def __post_init__(self):
        if self.amount == 0:
            raise ValueError("Transaction amount cannot be zero")
        if self.foreignAmount is not None and self.foreignCurrency is None:
            raise ValueError("Foreign currency must be specified with foreign amount")

    @property
    def description(self) -> str:
        return self.merchant

    @property
    def hasForeignCurrency(self) -> bool:
        return self.foreignAmount is not None and self.foreignCurrency is not None

    def __repr__(self) -> str:
        date = self.date.strftime("%d.%m.%Y")
        time = f" {self.time}" if self.time else ""
        location = f" {self.location}" if self.location else ""
        foreign = f" ({self.foreignCurrency} {self.foreignAmount})" if self.hasForeignCurrency else ""
        return (f"Transaction(category='{self.category}', merchant='{self.merchant}', date={date}{time}{location}, amountChf={self.amount}{foreign})")
