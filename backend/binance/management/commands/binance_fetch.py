import asyncio
import json
import logging
import ssl
from datetime import timedelta

import certifi
import websockets
from django.core.management import BaseCommand
from django.utils import timezone

from backend import settings
from backend.binance.structs import BaseEvent, BinanceEvent, Stream, SubscribeMessage, Symbol
from backend.binance.utils import parse_stream_event

logger = logging.getLogger(__name__)

streams = [f"{symbol}@{stream}" for symbol in Symbol for stream in Stream]

# Create an SSL context that doesn't verify certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


class Command(BaseCommand):
    help = "Fetches data from Binance for the specified period of time."

    def add_arguments(self, parser):
        parser.add_argument("period", type=int, help="The number of minutes to fetch data for")

    def handle(self, *args, **options):
        period = options["period"]
        asyncio.run(fetch(period))


async def fetch(period: int):
    start_time = timezone.now()
    end_time = start_time + timedelta(minutes=period)

    async with websockets.connect(settings.BINANCE_WS_URL, ssl=ssl_context) as websocket:
        await websocket.send(SubscribeMessage(params=streams, id=1).json())
        while timezone.now() < end_time:
            raw_event = await websocket.recv()
            try:
                binance_event = BinanceEvent.parse_raw(raw_event)
                symbol, stream = binance_event.stream.split("@")
                event = parse_stream_event(stream, binance_event.data)
            except ValueError:
                continue
            write_to_file(event)
            logger.info("Processed %s@%s", event.symbol, event.stream)

        logger.info("%s minutes have passed. Stopping the script.", period)


def write_to_file(event: BaseEvent):
    file = settings.BINANCE_LOG_FILE
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "a") as f:
        json.dump(event.dict(by_alias=True), f)
        f.write("\n")
