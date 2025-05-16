import json
from fastapi import WebSocket
from typing import Dict

active_connections: Dict[str, WebSocket] = {}

async def connect_user(licence_number: str, websocket: WebSocket):
    await websocket.accept()
    active_connections[licence_number] = websocket
    print(f"WebSocket connected for {licence_number}")


def disconnect_user(licence_number: str):
    active_connections.pop(licence_number, None)

async def send_notification_to_user(licence_number: str, message: str):
    websocket = active_connections.get(licence_number)
    print("this is the websocket",websocket)
    print(message)
    if websocket:
        await websocket.send_text(json.dumps({"message": message}))
