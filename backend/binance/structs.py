from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class Symbol(str, Enum):
    BTCUSDT = "btcusdt"
    ETHUSDT = "ethusdt"
    BNBUSDT = "bnbusdt"

    def __str__(self) -> str:
        return self.value


class Stream(str, Enum):
    TRADE = "trade"
    TICKER = "ticker"
    DEPTH = "depth"

    def __str__(self) -> str:
        return self.value


class SubscribeMessage(BaseModel):
    method: str = "SUBSCRIBE"
    params: list[str]
    id: int


class BaseEvent(BaseModel):
    event: Annotated[str, Field(alias="e")]
    event_time: Annotated[int, Field(alias="E")]
    symbol: Annotated[str, Field(alias="s")]

    @property
    def stream(self):
        raise NotImplemented


class Trade(BaseEvent):
    price: Annotated[float, Field(alias="p")]
    quantity: Annotated[float, Field(alias="q")]
    trade_time: Annotated[int, Field(alias="T")]
    market_marker: Annotated[bool, Field(alias="m")]
    ignore: Annotated[bool | None, Field(alias="M", default=None)]

    @property
    def stream(self):
        return "trade"


class Ticker(BaseEvent):
    price_change: Annotated[float, Field(alias="p")]
    price_change_percent: Annotated[float, Field(alias="P")]
    weighted_avg_price: Annotated[float, Field(alias="w")]
    last_price: Annotated[float, Field(alias="c")]
    last_quantity: Annotated[float, Field(alias="Q")]
    open_price: Annotated[float, Field(alias="o")]
    high_price: Annotated[float, Field(alias="h")]
    low_price: Annotated[float, Field(alias="l")]
    volume: Annotated[float, Field(alias="v")]
    quote_volume: Annotated[float, Field(alias="q")]
    open_time: Annotated[int, Field(alias="O")]
    close_time: Annotated[int, Field(alias="C")]
    number_of_trades: Annotated[int, Field(alias="n")]
    first_trade_price: Annotated[float | None, Field(alias="x", default=None)]
    first_trade_id: Annotated[str | None, Field(alias="F", default=None)]
    last_trade_id: Annotated[str | None, Field(alias="L", default=None)]
    best_bid_price: Annotated[float | None, Field(alias="b", default=None)]
    best_bid_quantity: Annotated[float | None, Field(alias="B", default=None)]
    best_ask_price: Annotated[float | None, Field(alias="a", default=None)]
    best_ask_quantity: Annotated[float | None, Field(alias="A", default=None)]

    @property
    def stream(self):
        return "ticker"


class OrderBookEntry(BaseModel):
    price: str
    quantity: str

    @classmethod
    def from_pair(cls, pair: tuple[str, str]) -> "OrderBookEntry":
        price, quantity = pair
        return cls(price=price, quantity=quantity)


class Depth(BaseEvent):
    first_update_id: Annotated[int, Field(alias="U")]
    final_update_id: Annotated[int, Field(alias="u")]
    bids: Annotated[list[OrderBookEntry], Field(alias="b")]
    asks: Annotated[list[OrderBookEntry], Field(alias="a")]

    @field_validator("asks", "bids", mode="before")
    @classmethod
    def parse_pairs(cls, v):
        return [OrderBookEntry.from_pair(pair) for pair in v]

    @property
    def stream(self):
        return "depth"


class BinanceEvent(BaseModel):
    stream: str
    data: dict
