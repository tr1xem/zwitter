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
import re

def load_passwords(file_path):
    """Load passwords from a JSON file."""
    with open(file_path, 'r') as file:
        passwords = json.load(file)
    return passwords


# Specify the path to your JSON file

# Load the passwords

messages: List[Tuple[str, str, str, str]] = []  # Add Optional[str] for original_message_id
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
    name = name_input.value.strip()  # Get the name value
    username = username_input.value.strip()
    password = password_input.value.strip()
    selected_option = option_input.value  # Get the selected option

    if username and password and name:
        if username in users:
            ui.notify("Username already exists.", color='negative')
        else:
            users[username] = {
                'password': password,
                'name': name,
                'option': selected_option  # Store selected option
            }
            save_users(users)  # Save to JSON file
            ui.notify("Registration successful!", color='positive')
            username_input.set_value('')  # Clear input fields
            password_input.set_value('')
            name_input.set_value('')  # Clear name input
            ui.navigate.to('/login')
    else:
        ui.notify("All fields are required.", color='negative')


@ui.page('/register')
def register_page():
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.column().classes('absolute top-0 right-0 p-4'):
        with ui.element().classes('max-[420px]:hidden top-0 right'):
            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    with ui.column().classes('absolute-center items-center'):
        ui.label("Register").classes('text-5xl')

        global username_input
        global password_input
        global name_input
        global option_input

        name_input = ui.input("Name").props('rounded outlined').classes('w-full max-w-xs')  # Name input field
        username_input = ui.input("Username").props('rounded outlined').classes('w-full max-w-xs')
        password_input = ui.input("Password", password=True, password_toggle_button=True).props('rounded outlined').classes('w-full max-w-xs')

        # Dropdown for options
        option_input = ui.select(label="Avatar", options=["Robots", "Monster", "Cat", "Human"]).props('rounded outlined').classes('w-full max-w-xs')

        with ui.row().classes('items-center'):
            ui.button("Register",icon='home',on_click=register)
            ui.button('Log in', icon='login',on_click=lambda: ui.navigate.to('/login'))


unrestricted_page_routes = {'/login','/','/register'}


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

def get_avatar(name, avatar_type):
# Mapping of avatar types to their respective sets
    avatar_mapping = {
        "Robots": "set1",
        "Monster": "set2",
        "Cat": "set4",
        "Human": "set5"
    }

# Get the corresponding set for the given avatar type
    avatar_set = avatar_mapping.get(avatar_type, "set1")  # Default to "set1" if not found

# Construct the link using the name and the mapped set
    link = f'https://robohash.org/{name}?set={avatar_set}&bgset=bg2'

    return link
@ui.page('/me')
def me_page() -> None:
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.column().classes('absolute top-0 right-0 p-4'):
        with ui.element().classes('max-[420px]:hidden top-0 right'):
            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)


    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')
        ui.notify('You have been logged out.')
    username = app.storage.user["username"]  # Get the logged-in user's username
    user_info = users.get(username, {})  # Access user info based on username

    name = user_info.get('name', 'Unknown User')
    avatar = get_avatar(name,user_info.get('option'))

    with ui.column().classes('absolute-center items-center'):
        ui.image(avatar).classes('rounded-full w-48 h-48 ml-4')
        ui.label(f'Hello {user_info.get('name', 'Unknown User')}!').classes('text-h3')  # Display user's name
        ui.label(f'Username:{username}').classes('text-lg')
        ui.label(f'Avatar: {user_info.get('option', 'No Option Selected')}').classes('text-lg')  # Display selected option
        with ui.row().classes('items-center'):
           ui.button("Logout", on_click=logout, icon='logout')
           ui.button("chat", on_click=lambda: ui.navigate.to('/chat'), icon='chat')


@ui.page('/')
def main_page() -> None:

    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))

    with ui.element().classes('max-[420px]:hidden top-0 right'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)
    with ui.column().classes('absolute-center items-center'):
        ui.image('https://static.vecteezy.com/system/resources/thumbnails/000/602/787/small/83038926.jpg').classes('rounded-full w-48 h-48 ml-4')
        ui.label("Welcome to Zwitter!!").classes('text-6xl')
        with ui.row().classes('items-center').classes('text-2xl'):
            ui.button('Log in',icon='login', on_click=lambda: ui.navigate.to('/login'))
            ui.button('Register',icon='home', on_click=lambda: ui.navigate.to('/register'))

    with ui.column().classes('absolute bottom-0 right-0 p-4'):
        with ui.row():
            ui.html('Made with ❤️ by')
            ui.link('tr1x_em', 'https://trix.is-a.dev').classes('text-red-500 underline')

    if app.storage.user.get('authenticated', True):
        RedirectResponse('/me')


@ui.page('/login')
def login() -> Optional[RedirectResponse]:

    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right'):
        with ui.column().classes('absolute top-0 right-0 p-4'):

            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    def try_login() -> None:
        """Function to attempt login."""
        username_value = username.value.strip()
        password_value = password.value.strip()

        # Check if username exists and validate password
        if username_value in users and users[username_value]['password'] == password_value:
            app.storage.user.update({'username': username_value, 'authenticated': True})
            # Redirect to the page where the user wanted to go
            ui.navigate.to(app.storage.user.get('referrer_path', '/me'))
        else:
            ui.notify('Wrong username or password', color='negative')
    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/me')
    with ui.column().classes('absolute-center items-center'):
        ui.label("Login").classes('text-5xl')
        global username
        username = ui.input('Username').on('keydown.enter', try_login).props('rounded outlined').classes('w-full max-w-xs')

        password = ui.input('Password', password=True, password_toggle_button=True).on(
            'keydown.enter', try_login).props('rounded outlined').classes('w-full max-w-xs')

        with ui.row().classes('items-center'):
            ui.button('Log in',icon='login', on_click=try_login)
            ui.button('Register', icon='home',on_click=lambda: ui.navigate.to('/register'))
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
@ui.refreshable
def chat_messages(own_id: str) -> None:
    ui.add_css("""
.chat-message-container {
    position: relative;  /* Allows absolute positioning of child elements */
}

.reply-button {
    display: none; /* Initially hide the button */
}

.chat-bg {
               background-image: url('https://i.imgur.com/Gk3qlQ2.png');
               background-size: cover; /* Cover the entire area */
        background-position: center; /* Center the image */
            background-repeat: no-repeat; /* Do not repeat the image */
}


.chat-message-container:hover .reply-button {
    display: block; /* Show button on hover */
}
""")
    if messages:
        for user_id, avatar, text, stamp in messages:
            # Retrieve the user's name from the users dictionary
            user_name = users.get(user_id, {}).get('name', user_id)

            # Create a container for each message
            with ui.row().classes('w-full items-center chat-message-container '):
                # Check if the message is from the current user
                if own_id == user_id:
                        # Display chat message on the right
                        ui.chat_message(name=user_name, text=text.replace('\n', '<br>'), stamp=stamp,
                                    avatar=avatar, sent=True,text_html=True).classes('ml-auto')

                    # Add a reply button that appears on hover, aligned to the left of this message
                        with ui.button(icon="reply", on_click=lambda msg_text=text, sender_name=user_id: send_reply(msg_text, sender_name)).props('flat').classes('reply-button rounded-full mr-1'):
                            ui.label('').classes('hidden')  # Placeholder to make it a button
                else:

                # Display chat message on the left
                    ui.chat_message(name=user_name, text=text.replace('\n', '<br>'), stamp=stamp,
                                    avatar=avatar, sent=False,text_html=True).classes('mr-auto')

                    # Add a reply button that appears on hover, aligned to the right of this message
                    with ui.button(icon="reply",on_click=lambda msg_text=text, sender_name=user_id: send_reply(msg_text, sender_name)).props('flat').classes('reply-button rounded-full ml-2'):
                        ui.label('').classes('hidden')  # Placeholder to make it a button

    else:
        ui.label('No messages yet').classes('mx-auto my-36')

    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

replying_to = None
def send_reply(msg_text, sender_name):
    global replying_to  # Access the global variable
    replying_to = (sender_name, msg_text)  # Set the message and sender being replied to
    print(f"Replying to: {sender_name}: {msg_text}")
@ui.page('/chat',response_timeout=30)
async def main():
    def send() -> None:
        global replying_to  # Access the global variable

        if text.value.strip():
            stamp = datetime.now().strftime('%X')

            # Limit the length of the reply message
            max_length = 40  # Set your desired maximum length
            reply_text = text.value  # Truncate if necessary

            # Check if replying to a message
            if replying_to:
                if replying_to[1].startswith("<div style='color: gray; font-style: italic;'>"):
                    pattern = r'<div>(.*?)</div>'
                    matches = re.findall(pattern, replying_to[1])
                    print(matches)
                    formatted_message = f"<div style='color: gray; font-style: italic;'>Replying to {replying_to[0]}:<br>{matches[0][:max_length]}</div><div>{reply_text}</div>"

                    print(f"Reply 1 : {formatted_message}")
                else:
                    formatted_message = f"<div style='color: gray; font-style: italic;'>Replying to {replying_to[0]}:<br>{replying_to[1][:max_length] }</div><div>{reply_text}</div>"
                    print(f"Reply 2 : {formatted_message}")


                messages.append((user_id, avatar, formatted_message, stamp))
                replying_to=None
            else:
                # Append message with sender's name included
                messages.append((user_id, avatar, f"{text.value}", stamp))

            text.value = ''
            chat_messages.refresh()
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right'):
        with ui.column().classes('absolute top-0 right-0 p-4'):
            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    username = app.storage.user["username"]  # Get the logged-in user's username
    user_info = users.get(username, {})  # Access user info based on username
    name = user_info.get('name', 'Unknown User')
    #    ui.label(f'Hello {user_info.get('name', 'Unknown User')}!').classes('text-h3')  # Display user's name
    user_id = app.storage.user["username"]
    avatar = get_avatar(name,user_info.get('option'))
    clients.append(ui.context.client)


    # Notify all clients that a new user has connected
    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500; } {background-image: url("https://i.imgur.com/Gk3qlQ2.png"); background-size: cover; background-position: center; background-repeat: no-repeat;}')
    with ui.footer().classes('bg-black'):
        with ui.column().classes('w-full max-w-3xl mx-auto my-6'):
            with ui.row().classes('w-full no-wrap items-center'):
                with ui.avatar().on('click', lambda: ui.navigate.to(main)):
                    ui.image(avatar)

                text = ui.input(placeholder='message').on('keydown.enter', send).props('rounded outlined input-class=mx-3').classes('flex-grow')

                # Add a send button for mobile users
                ui.button(icon="send",on_click=send).classes('ml-3 flex items-center').props('rounded')
   # await ui.context.client.connected(response_timeout=10)
    await broadcast_message(f"{name} is now connected.",ui.context.client)

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        chat_messages(user_id)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED',
           title="Zwitter", favicon='💀',port=80,reconnect_timeout=30)
