from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .websocket_manager import connect_user, disconnect_user

router = APIRouter()

@router.websocket("/ws/{licence_number}")
async def websocket_endpoint(websocket: WebSocket, licence_number: str):
    await connect_user(licence_number, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive or ping messages
    except WebSocketDisconnect:
        disconnect_user(licence_number)
