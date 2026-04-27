import json

from channels.generic.websocket import AsyncWebsocketConsumer


class LocationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for location updates.
    Connects to 'location_updates' channel group and broadcasts location data.
    """

    async def connect(self):
        self.group_name = "location_updates"

        # Join the location_updates group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the location_updates group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # This consumer doesn't expect messages from clients,
        # but we handle it just in case
        pass

    # Receive message from channel group
    async def location_update(self, event):
        """
        Handler for location_update messages sent to the group.
        Broadcasts latitude and longitude to all connected WebSocket clients.
        """
        latitude = event['latitude']
        longitude = event['longitude']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude
        }))