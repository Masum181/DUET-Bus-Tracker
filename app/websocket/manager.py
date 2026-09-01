from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict

from app.schemas.websocket import BusLocationBroadcast
from app.utils.data_class import live_bus_store
from app.utils.logger import logging

@dataclass
class TripRoom:
    connections: dict[WebSocket, str] = field(default_factory=dict)  # ws -> student_id
    last_bus_location:BusLocationBroadcast | None = None
    lock:asyncio.Lock = field(default_factory=asyncio.Lock)


class ConnectionManager:
    def __init__(self):
        self._rooms:dict[str, TripRoom] = {}

    def _get_room(self, trip_id:str) -> TripRoom:
        return self._rooms.setdefault(trip_id, TripRoom())

    async def connect(self, trip_id:str, student_id:str, websocket:WebSocket) -> None:
        await websocket.accept()
        room = self._get_room(trip_id)
        async with room.lock:
            room.connections[websocket] = student_id
        # send the last known bus location right way so the student doesn't have to wait for the next bus ping
        if room.last_bus_location is not None:
            await websocket.send_json(room.last_bus_location.model_dump(mode="json"))

    def disconnect(self, trip_id:str, websocket:WebSocket) -> None:
        room = self._get_room(trip_id)
        if room is None:
            return
        room.connections.pop(websocket, None)

        if not room.connections and room.last_bus_location is None:
            self._rooms.pop(trip_id, None)

    async def update_bus_location(self, trip_id:str, location:BusLocationBroadcast) -> None:
        room = self._get_room(trip_id)
        room.last_bus_location = location
        await self.broadcast(trip_id, location.model_dump(mode="json"))

    async def broadcast(self, trip_id:str, message:dict) -> None:
        room = self._get_room(trip_id)
        if room is None:
            return
        async with room.lock:
            targets = list(room.connections.keys())
        dead:list[WebSocket] = []
        for ws in targets:
            try:
                await ws.send_json(message)
            except Exception:
                logging.warning("Dropping dead websocket for trip %s", trip_id)
                dead.append(ws)
        for ws in dead:
            self.disconnect(trip_id, ws)

    async def send_to(self, websocket: WebSocket, payload: dict) -> None:
        await websocket.send_json(payload)

    def get_last_bus_location(self, trip_id: str) -> BusLocationBroadcast | None:
        room = self._rooms.get(trip_id)
        return room.last_bus_location if room else None


manager = ConnectionManager()

    