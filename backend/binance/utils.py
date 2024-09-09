from backend.binance.structs import BaseEvent, Depth, Stream, Ticker, Trade


def get_event_stream(event: BaseEvent) -> Stream:
    streams = {
        "trade": Stream.TRADE,
        "24hrTicker": Stream.TICKER,
        "depthUpdate": Stream.DEPTH,
    }
    if stream := streams.get(event.event):
        return stream
    raise ValueError(f"Unknown event stream: {event.event}")


def parse_stream_event(stream: str, data: dict) -> BaseEvent:
    events = {
        "trade": Trade,
        "ticker": Ticker,
        "depth": Depth,
    }
    if event := events.get(stream):
        return event(**data)
    raise ValueError(f"Unknown stream type: {stream}")
