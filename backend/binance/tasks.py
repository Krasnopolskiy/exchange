import json
import logging
from time import sleep

from asgiref.sync import async_to_sync
from celery import current_app
from channels.layers import get_channel_layer
from django.conf import settings

from backend.binance.structs import BaseEvent, Stream
from backend.binance.utils import get_event_stream, parse_stream_event

logger = logging.getLogger(__name__)


def load_events() -> list[BaseEvent]:
    file = settings.BINANCE_LOG_FILE
    if not file.exists():
        raise ValueError(f"File {file} does not exist")
    with open(file, "r") as f:
        for line in f:
            base_event = BaseEvent.parse_raw(line)
            stream = get_event_stream(base_event)
            if stream == Stream.TRADE:
                yield parse_stream_event(stream, json.loads(line))
            elif stream == Stream.TICKER:
                yield parse_stream_event(stream, json.loads(line))
            elif stream == Stream.DEPTH:
                yield parse_stream_event(stream, json.loads(line))


def send_event(event: BaseEvent, previous_event_time: int | None) -> int:
    elapsed = (event.event_time - previous_event_time) if previous_event_time else 0
    elapsed = max(elapsed, 0)
    sleep(elapsed / 1000)  # milliseconds
    async_to_sync(get_channel_layer().group_send)(
        f"{event.symbol}-{event.stream}",
        {"type": "send_pair_data", "data": event.dict()},
    )
    logger.info(f"Sent {event.symbol}@{event.stream} event")
    return event.event_time


@current_app.task
def replay():
    events = load_events()

    last_event_time = None
    for event in events:
        last_event_time = send_event(event, last_event_time)
