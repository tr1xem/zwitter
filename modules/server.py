#!/usr/bin/env python3
import asyncio
from typing import Set
from websockets.server import WebSocketServerProtocol
import websockets

CONNECTIONS: Set[WebSocketServerProtocol] = set()


async def broadcast(message: str):
    """Send a message to all connected clients."""
    to_remove = []
    for websocket in CONNECTIONS:
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            to_remove.append(websocket)
    # Remove disconnected clients
    for websocket in to_remove:
        CONNECTIONS.remove(websocket)


async def handle_connect(websocket: WebSocketServerProtocol):
    """Register the new websocket connection, handle incoming messages, and remove the connection when it is closed."""
    try:
        CONNECTIONS.add(websocket)
        # print(f"New connection. Total: {len(CONNECTIONS)}")
        async for data in websocket:
            print(f"{data}")
            await broadcast(f"{data}")
    except websockets.ConnectionClosed as e:
        print(f"Connection closed with error: {e}")
    finally:
        # Ensure websocket is in CONNECTIONS before removing
        if websocket in CONNECTIONS:
            CONNECTIONS.remove(websocket)
            print(f"Connection closed. Total: {len(CONNECTIONS)}")


async def start_websocket_server():
    async with websockets.serve(handle_connect, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_websocket_server())
