from enum import Enum

from pydantic import BaseModel


class Action(str, Enum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"


class SubscriptionRequest(BaseModel):
    action: Action
    pair: str
    stream: str


class SubscriptionResponse(BaseModel):
    action: Action
    subscription: str
    result: bool = True


class InvalidDataResponse(BaseModel):
    error: str = "Invalid data"


class PairData(BaseModel):
    pair: str
    price: float
