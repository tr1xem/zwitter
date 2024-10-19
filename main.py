#!/usr/bin/env python3

from typing import Optional

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from typing import List, Tuple
import time
from nicegui import app, ui
import json

def load_passwords(file_path):
    """Load passwords from a JSON file."""
    with open(file_path, 'r') as file:
        passwords = json.load(file)
    return passwords


# Specify the path to your JSON file

# Load the passwords

messages: List[Tuple[str, str, str, str]] = []
# File to store users and passwords
PASSWORD_FILE = 'logins.json'


def load_users():
    """Load users from the JSON file."""
    try:
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    """Save users to the JSON file."""
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(users, file)


# Initialize user storage
users = load_users()


def register():
    username = username_input.value.strip()
    password = password_input.value.strip()

    if username and password:
        if username in users:
            ui.notify("Username already exists.", color='negative')
        else:
            users[username] = password  # Store the username and password
            save_users(users)  # Save to JSON file
            ui.notify("Registration successful!", color='positive')
            username_input.set_value('')  # Clear input fields
            password_input.set_value('')
    else:
        ui.notify("Both fields are required.", color='negative')

# Create the registration page


@ui.page('/register')
def register_page():
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right').tooltip('Cycle theme mode through dark, light, and system/auto.'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)
    with ui.column().classes('absolute-center items-center'):
        ui.label("Register").classes('text-2xl')

        global username_input
        global password_input

        username_input = ui.input("Username").props('rounded outlined').classes('w-full max-w-xs')
        password_input = ui.input("Password", password=True, password_toggle_button=True).props('rounded outlined').classes('w-full max-w-xs')

        ui.button("Register", on_click=register).classes('mt-4')


unrestricted_page_routes = {'/login','/','/register'}


@ ui.refreshable
def chat_messages(own_id: str) -> None:
    if messages:
        for user_id, avatar, text, stamp in messages:
            ui.chat_message(name=user_id, text=text, stamp=stamp,
                            avatar=avatar, sent=own_id == user_id)
    else:
        ui.label('No messages yet').classes('mx-auto my-36')
    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                # remember where the user wanted to go
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ ui.page('/me')
def me_page() -> None:

    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))

    with ui.element().classes('max-[420px]:hidden top-0 right').tooltip('Cycle theme mode through dark, light, and system/auto.'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')
        ui.notify('You have been logged out.')
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button("Logout", on_click=logout, icon='logout')
        ui.button("Chat", on_click=lambda: ui.navigate.to('/chat'), icon='chat')



@ ui.page('/')
def main_page() -> None:
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right').tooltip('Cycle theme mode through dark, light, and system/auto.'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)
    with ui.column().classes('absolute-center items-center'):
        ui.label("Welcome to Zwitter!!").classes('text-2xl')
        ui.button('Log in', on_click=lambda: ui.navigate.to('/login'))
        ui.button('Register', on_click=lambda: ui.navigate.to('/register'))

    with ui.column().classes('absolute bottom-0 right-0 p-4'):
        with ui.row():
            ui.html('Made with ❤️ by')
            ui.link('tr1x_em', 'https://trix.is-a.dev').classes('text-red-500 underline')


@ ui.page('/login')
def login() -> Optional[RedirectResponse]:

    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right').tooltip('Cycle theme mode through dark, light, and system/auto.'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if users.get(username.value) == password.value:
            app.storage.user.update(
                {'username': username.value, 'authenticated': True})
            # go back to where the user wanted to go
            ui.navigate.to(app.storage.user.get('referrer_path', '/me'))
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/me')
    with ui.column().classes('absolute-center items-center'):
        ui.label("Login").classes('text-2xl')
        global username
        username = ui.input('Username').on('keydown.enter', try_login).props('rounded outlined').classes('w-full max-w-xs')

        password = ui.input('Password', password=True, password_toggle_button=True).on(
            'keydown.enter', try_login).props('rounded outlined').classes('w-full max-w-xs')

        ui.button('Log in', on_click=try_login)
        ui.button('Register', on_click=lambda: ui.navigate.to('/register'))
    return None


# Global list to hold all connected clients
clients = []


async def broadcast_message(message: str,current):
    """Send a message to all connected clients."""
    for client in clients:
        if client != current:
            with client:
                time.sleep(1)
                ui.notify(message,postion="top")



@ ui.page('/chat')
async def main():
    def send() -> None:
        if text.value.strip():

            print(f"[{user_id}]: {text.value}")
            stamp = datetime.now().strftime('%X')
            messages.append((user_id, avatar, text.value, stamp))
            text.value = ''
            chat_messages.refresh()
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right').tooltip('Cycle theme mode through dark, light, and system/auto.'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    user_id = app.storage.user["username"]
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'
    clients.append(ui.context.client)

    # Notify all clients that a new user has connected
    ui.add_css(
        r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')
    with ui.footer().classes('bg-black'):
        with ui.column().classes('w-full max-w-3xl mx-auto my-6'):
            with ui.row().classes('w-full no-wrap items-center'):
                with ui.avatar().on('click', lambda: ui.navigate.to(main)):
                    ui.image(avatar)

                text = ui.input(placeholder='message').on('keydown.enter', send).props('rounded outlined input-class=mx-3').classes('flex-grow')

                # Add a send button for mobile users
                ui.button(icon="send",on_click=send).classes('ml-3 flex items-center').props('rounded')
    await ui.context.client.connected()
    await broadcast_message(f"{user_id} is now connected.",ui.context.client)

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        chat_messages(user_id)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED',
           title="Zwitter", favicon='💀')
