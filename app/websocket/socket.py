from fastapi import WebSocket, WebSocketDisconnect

connections = {}

async def websocket_endpoint(websocket: WebSocket, tracking_id: str):
    await websocket.accept()

    if tracking_id not in connections:
        connections[tracking_id] = []

    connections[tracking_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        connections[tracking_id].remove(websocket)