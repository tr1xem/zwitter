#!/usr/bin/env python3
from nicegui import ui,app
import asyncio
import websockets

SERVER_URL = 'ws://localhost:8765'

async def connect_to_server():
    """Connect to the WebSocket server and handle incoming messages."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            ui.label(f"Connected to {SERVER_URL}").classes('text-green-600')
            while True:
                message = await websocket.recv()
                with messages:
                    ui.label(str(message))
    except Exception as e:
        ui.label(f"Error: {e}").classes('text-red-600')

async def send_message(message: str):
    """Send a message to the WebSocket server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            await websocket.send(message)
    except Exception as e:
        ui.label(f"Error: {e}").classes('text-red-600')

ui.label('WebSocket Client Demo').classes('text-2xl')
ui.label(f"Server URL: {SERVER_URL}").classes('text-sm')
with ui.row().classes('items-center'):
    name = ui.input(value='name').props('clearable')
    message = ui.input(value='message').props('clearable')
    formatted_message = f"[{name.value}]: {message.value}"
    ui.button('Send', on_click=lambda: asyncio.create_task(send_message(f"[{name.value}]: {message.value}")))
ui.separator().classes('mt-6')
ui.label('Incoming messages:')

messages = ui.column().classes('ml-4')
# Schedule the connection task when NiceGUI starts
app.on_startup(connect_to_server)

ui.run()

