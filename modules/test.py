#!/usr/bin/env python3
from nicegui import ui, app
import asyncio
import websockets
import random

SERVER_URL = 'ws://localhost:8765'
USERNAME = f"user#{random.randint(1000, 9999)}"  # Default username

async def connect_to_server():
    """Connect to the WebSocket server and handle incoming messages."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            while True:
                message = await websocket.recv()
                sender, content = parse_message(message)
                if sender == USERNAME:
                    sender = "You"
                add_message_to_ui(content, sender=sender)
    except Exception as e:
        add_message_to_ui(f"Error: {e}", sender="System")

async def send_message_to_server(message: str):
    """Send a message to the WebSocket server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            formatted_message = f"{USERNAME}::{message}"
            await websocket.send(formatted_message)
    except Exception as e:
        add_message_to_ui(f"Error: {e}", sender="System")

def add_message_to_ui(message: str, sender: str):
    """Display a message in the chat area."""
    bubble_color = 'bg-blue-500 text-white' if sender == "You" else 'bg-gray-700 text-gray-200'
    alignment = 'items-end' if sender == "You" else 'items-start'
    username_color = 'text-gray-400 text-xs' if sender != "You" else 'text-gray-300 text-xs'

    with chat_area:
        with ui.column().classes(f'w-full {alignment} mb-2'):
            ui.label(sender).classes(username_color)
            with ui.card().classes(f'{bubble_color} px-4 py-2 rounded-2xl shadow text-sm max-w-xs w-full break-words'):
                ui.label(message).classes('break-words')
    ui.update()  # Refresh the UI

def handle_send():
    """Handle the send button click."""
    user_message = message_input.value.strip()
    if user_message:
        add_message_to_ui(user_message, sender="You")
        asyncio.create_task(send_message_to_server(user_message))
        message_input.value = ""  # Clear the input field

def handle_enter_key(event):
    """Send message when Enter key is pressed."""
    if event.args.get('key') == "Enter":
        handle_send()

def parse_message(raw_message: str):
    """Parse the raw message into sender and content."""
    if "::" in raw_message:
        return raw_message.split("::", 1)
    return "Unknown", raw_message  # Fallback if formatting is invalid

def update_username():
    """Update the username with the input value."""
    global USERNAME
    if username_input.value.strip():
        USERNAME = username_input.value.strip()

# Main Layout
with ui.row().classes('h-screen w-screen bg-gray-900 text-white'):
    # Sidebar for users
    with ui.column().classes('bg-gray-800 text-white w-1/4 h-full p-4'):
        ui.label('Users').classes('text-lg font-bold mb-4')
        for user in ['Alice', 'Bob', 'Charlie', 'David']:  # Static list of users
            ui.label(user).classes('p-2 hover:bg-gray-700 rounded')
        # Username input
        ui.separator().classes('my-4')
        ui.label('Set Your Username:').classes('text-sm mb-2')
        username_input = ui.input(value=USERNAME).classes(
            'w-full px-4 py-2 rounded bg-gray-700 text-white').on('blur', lambda: update_username())

    # Main chat area
    with ui.column().classes('flex-1 h-full'):
        # Chat header
        with ui.row().classes('bg-gray text-white p-4 shadow'):
            ui.label('Chat Room').classes('text-xl font-bold')

        # Chat display area
        with ui.column().classes('flex-1 overflow-y-auto p-4'):
            chat_area = ui.column().classes('w-full space-y-2')

        # Chat input area
        with ui.row().classes('bg-gray p-4 items-center justify-center shadow'):
            with ui.column().classes('w-full max-w-2xl'):
                message_input = ui.input(placeholder='Type your message...').classes(
                    'w-full px-4 py-4 rounded-full border-0 bg-gray-700 text-white text-lg')
                message_input.on('keydown', handle_enter_key)  # Listen for Enter key
                ui.button('Send', on_click=handle_send).classes(
                    'mt-2 w-full bg-blue-600 text-white px-4 py-2 rounded-full shadow hover:bg-blue-700')

# Start the connection on startup
app.on_startup(connect_to_server)

ui.run()

