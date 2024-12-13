from typing import Optional
from fastapi import Request, FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from typing import List, Tuple
import time
from nicegui import ui,app
import re
from modules.sqlwrapper import  *

def init(fastapi_app: FastAPI):
    logging.info("Initializing App")
    init_db()

    ui.run_with(fastapi_app,storage_secret="AAA",title="Zwitter", favicon='💀',reconnect_timeout=30)

online_users = {
    "user1": {"name": "tr1x_em", "status": "Online", "avatar": "https://i.ibb.co/L1svvRg/tr1x-em.png"},
}

# ff
clients = []


def handle_disconnect(user_id):
    if user_id and user_id in online_users:
        online_users.pop(user_id)
        update_user.refresh()  # Refresh to update the list after removal
        logging.info(f"User {user_id} disconnected and removed from the list.")
# Functions - Load and Save and Register


messages: List[Tuple[str, str, str, str]] = []


def register():
    name = name_input.value.strip()
    username = username_input.value.strip()
    password = password_input.value.strip()
    selected_option = option_input.value

    if username and password and name:
        if checkuser(username):
            registeruser(username, password, name, selected_option)
            ui.notify("Registration successful!", color='positive')
            username_input.set_value('')
            password_input.set_value('')
            name_input.set_value('')
            ui.navigate.to('/login')
        else:
            ui.notify("Username already exists.", color='negative')
    else:
        ui.notify("All fields are required.", color='negative')


def get_avatar(name, avatar_type):

    avatar_mapping = {
        "Robots": "set1",
        "Monster": "set2",
        "Cat": "set4",
        "Human": "set5"
    }

    avatar_set = avatar_mapping.get(avatar_type, "set1")

    link = f'https://robohash.org/{name}?set={avatar_set}&bgset=bg2'

    return link


# Auth - Middleware


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:

                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)

app.add_middleware(AuthMiddleware)
unrestricted_page_routes = {'/login','/','/register'}

# Web Endpoint


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

        name_input = ui.input("Name").props('rounded outlined').classes('w-full max-w-xs')
        username_input = ui.input("Username").props('rounded outlined').classes('w-full max-w-xs')
        password_input = ui.input("Password", password=True, password_toggle_button=True).props('rounded outlined').classes('w-full max-w-xs')

        option_input = ui.select(label="Avatar", options=["Robots", "Monster", "Cat", "Human"]).props('rounded outlined').classes('w-full max-w-xs')

        with ui.row().classes('items-center'):
            ui.button("Register",icon='home',on_click=register)
            ui.button('Log in', icon='login',on_click=lambda: ui.navigate.to('/login'))


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
    username = app.storage.user["username"]
    if  not checkuser(username):
        user_info = getuser(username)
        name = user_info[2]
        avatar = get_avatar(name,str(user_info[3]))
        with ui.column().classes('absolute-center items-center'):
            ui.image(avatar).classes('rounded-full w-48 h-48 ml-4')
            ui.label(f'Hello {name}!').classes('text-h3')
            ui.label(f'Username:{username}').classes('text-lg')
            ui.label(f'Avatar: {user_info[3]}').classes('text-lg')
            with ui.row().classes('items-center'):
                ui.button("Logout", on_click=logout, icon='logout')
            ui.button("chat", on_click=lambda: ui.navigate.to('/chat'), icon='chat')
    else:
        logout()


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

        if loginuser(username_value, password_value):
            app.storage.user.update({'username': username_value, 'authenticated': True})

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


# Online Users Implementation
def broadcast_message(message: str,current) -> None:
    """Send a message to all connected clients."""
    logging.info(f"User connected :{message}")
    update_user.refresh()
    for client in clients:
        if client != current:
            with client:
                time.sleep(1)
                ui.notify(message,postion="top")

@ui.refreshable
def update_user():
    with ui.list().props('bordered separator'):
        ui.item_label('Online Users').props('header').classes('text-bold')
        ui.separator()

        for user_id, user_info in online_users.items():
            with ui.item():
                with ui.item_section().props('avatar').style('position: relative;'):
                    ui.image(user_info["avatar"]).classes('w-9 h-9 rounded-full')
                    ui.html('<span style="position: absolute; bottom: 2px; right: 20px; '
                            'width: 8px; height: 8px; background-color: green; border-radius: 50%;"></span>')

                with ui.item_section():
                    ui.item_label(f'{user_info["name"]}')



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
            username = app.storage.user["username"]
            user_info = getuser(username)
            user_name = user_info[2]




            with ui.row().classes('w-full items-center chat-message-container '):
                if own_id == user_id:

                        ui.chat_message(name=user_name, text=text.replace('\n', '<br>'), stamp=stamp,
                                    avatar=avatar, sent=True,text_html=True).classes('ml-auto')

                        with ui.button(icon="reply", on_click=lambda msg_text=text, sender_name=user_id: send_reply(msg_text, sender_name)).props('flat').classes('reply-button rounded-full mr-1'):
                            ui.label('').classes('hidden')
                else:

                    ui.chat_message(name=user_name, text=text.replace('\n', '<br>'), stamp=stamp,
                                    avatar=avatar, sent=False,text_html=True).classes('mr-auto')

                    with ui.button(icon="reply",on_click=lambda msg_text=text, sender_name=user_id: send_reply(msg_text, sender_name)).props('flat').classes('reply-button rounded-full ml-2'):
                        ui.label('').classes('hidden')

    else:
        ui.label('No messages yet').classes('mx-auto my-36')

    ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')


replying_to = None
def send_reply(msg_text, sender_name):
    global replying_to
    replying_to = (sender_name, msg_text)


@ui.page('/chat',response_timeout=30)
async def main():
    def send() -> None:
        global replying_to

        if text.value.strip():
            stamp = datetime.now().strftime('%X')

            max_length = 40
            reply_text = text.value

            if replying_to:
                if replying_to[1].startswith("<div style='color: gray; font-style: italic;'>"):
                    pattern = r'<div>(.*?)</div>'
                    matches = re.findall(pattern, replying_to[1])
                    formatted_message = f"<div style='color: gray; font-style: italic;'>Replying to {replying_to[0]}:<br>{matches[0][:max_length]}</div><div>{reply_text}</div>"
                else:
                    formatted_message = f"<div style='color: gray; font-style: italic;'>Replying to {replying_to[0]}:<br>{replying_to[1][:max_length] }</div><div>{reply_text}</div>"

                messages.append((username, avatar, formatted_message, stamp))
                replying_to=None
            else:

                messages.append((username, avatar, f"{text.value}", stamp))

            text.value = ''
            chat_messages.refresh()
    dark_mode = ui.dark_mode(value=app.storage.browser.get('dark_mode'))
    with ui.element().classes('max-[420px]:hidden top-0 right'):
        with ui.column().classes('absolute top-0 right-0 p-4'):
            ui.tooltip('Cycle theme mode through dark, light, and system/auto.')
            ui.button(icon='dark_mode', on_click=lambda: dark_mode.set_value(None)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', value=True)
            ui.button(icon='light_mode', on_click=lambda: dark_mode.set_value(True)).props('flat fab-mini color=black').bind_visibility_from(dark_mode, 'value', value=False)
            ui.button(icon='brightness_auto', on_click=lambda: dark_mode.set_value(False)).props('flat fab-mini color=white').bind_visibility_from(dark_mode, 'value', lambda mode: mode is None)

    username = app.storage.user["username"]
    if  not checkuser(username):
        user_info = getuser(username)
        name = user_info[2]
        avatar = get_avatar(name,user_info[3])

        clients.append(ui.context.client)

        with ui.footer().classes('bg-black'):
            with ui.column().classes('w-full max-w-3xl mx-auto my-6'):
                with ui.row().classes('w-full no-wrap items-center'):
                    with ui.avatar().on('click', lambda: ui.navigate.to(main)):
                        ui.image(avatar)

                    text = ui.input(placeholder='message').on('keydown.enter', send).props('rounded outlined input-class=mx-3').classes('flex-grow')

                    ui.button(icon="send",on_click=send).classes('ml-3 flex items-center').props('rounded')


        ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500; } {background-image: url("https://i.imgur.com/Gk3qlQ2.png"); background-size: cover; background-position: center; background-repeat: no-repeat;}')
        online_users[str(ui.context.client)] = {
            "name": name,
            "status": "online",
            "avatar": avatar
        }
        ui.run_javascript(f"""
            window.addEventListener('beforeunload', function(event) {{
                const userId = '{ui.context.client}'; // Dynamic user ID

                fetch('/api/user/disconnect', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ userId: userId }})
                }});
            }});
        """)
        broadcast_message(f"{name} is now connected.",ui.context.client)
        with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
            with ui.column().style("position: absolute; top: 0; left: 0; height: 80%; width: 30%; z-index: 1; padding: 10px;"):
                update_user()

            # Ensuring chat messages appear in the remaining space
            with ui.column().style("margin-left: 5%;"):
                chat_messages(username)
    else:
        ui.navigate.to('/login')

