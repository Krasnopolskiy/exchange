import json

from channels.generic.websocket import AsyncWebsocketConsumer

from backend.stream.structs import Action, InvalidDataResponse, SubscriptionRequest, SubscriptionResponse


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.subscriptions: set[str] = set()

    async def disconnect(self, close_code):
        for pair in self.subscriptions:
            await self.unsubscribe_pair(pair)

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if text_data is None:
            return

        try:
            request = SubscriptionRequest.parse_raw(text_data)
        except ValueError:
            response = InvalidDataResponse()
            await self.send(response.model_dump_json())
            return

        subscription = f"{request.pair}-{request.stream}"
        if request.action == Action.SUBSCRIBE:
            await self.subscribe_pair(subscription)
        elif request.action == Action.UNSUBSCRIBE:
            await self.unsubscribe_pair(subscription)

    async def subscribe_pair(self, subscription: str):
        response = SubscriptionResponse(action=Action.SUBSCRIBE, subscription=subscription)
        if subscription not in self.subscriptions:
            self.subscriptions.add(subscription)
            await self.channel_layer.group_add(subscription, self.channel_name)
        await self.send(response.json())

    async def unsubscribe_pair(self, subscription: str):
        response = SubscriptionResponse(action=Action.UNSUBSCRIBE, subscription=subscription)
        if subscription in self.subscriptions:
            self.subscriptions.remove(subscription)
            await self.channel_layer.group_discard(subscription, self.channel_name)
        await self.send(response.json())

    async def send_pair_data(self, event: dict):
        data = event["data"]
        await self.send(json.dumps(data))
