from nicegui import ui
from chat import *

dark = ui.dark_mode()
dark.enable()

tabs = ui.tabs().classes("flex-grow")

# Toggle Dark/Light Mode Function
def toggle_mode():
    if dark.enabled:
        dark.disable()
    else:
        dark.enable()

# Minimal Header
with ui.header().classes("bg-gray-900 text-white p-2 shadow-md flex items-center"):
    ui.label("Chat App").classes("text-lg font-medium ml-2")
    with tabs:
        ui.tab("Chat")
        ui.tab("Settings")
        ui.tab("C")
    with ui.row().classes("ml-auto gap-2"):
        ui.button(icon="light_mode", on_click=dark.disable()).props("flat color=white").classes("p-2")
        ui.button(icon="dark_mode", on_click=dark.enable()).props("flat color=white").classes("p-2")
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props("flat color=white").classes("p-2")
# Right Drawer
with ui.right_drawer(top_corner=False, bottom_corner=True).classes("bg-gray-800 text-white shadow-lg w-64") as right_drawer:
    ui.item_label("Contacts").props("header").classes("text-bold text-xl p-4")
    with ui.list().props("w-full separator").classes("w-full"):
        ui.separator()
        with ui.item(on_click=lambda: ui.notify("Selected contact 1")).classes("p-2 flex items-center"):
            with ui.item_section().props("avatar"):
                ui.icon("person").classes("text-blue-400")
            with ui.item_section():
                ui.item_label("Nice Guy").classes("text-lg")
        with ui.item(on_click=lambda: ui.notify("Selected contact 2")).classes("p-2 flex items-center"):
            with ui.item_section().props("avatar"):
                ui.icon("person").classes("text-blue-400")
            with ui.item_section():
                ui.item_label("Nice Person").classes("text-lg")

# Tab Panels
with ui.tab_panels(tabs, value="Chat").classes("w-full h-full mx-auto p-4") as tab_panels:
    with ui.tab_panel("Chat"):
        with ui.column().classes('gap-4 w-full h-full overflow-auto'):
            chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
            chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
            chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")
            chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
            chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
            chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
            chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")
            chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
            chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")

    with ui.tab_panel("Settings"):
        ui.label("Settings").classes("text-2xl mb-4")
        with ui.column().classes("gap-4"):
            ui.label("OpenAI Whisper (voice transcription)").classes("text-xl")
            ui.upload(auto_upload=True).classes("w-full")
            ui.label("Stable Diffusion (image generator)").classes("text-xl")
            ui.input("Prompt").classes("w-full")
            ui.button("Generate").classes("bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700")

    with ui.tab_panel("C"):
        ui.label("Content of C").classes("text-2xl mb-4")
        with ui.row().classes("gap-4"):
            ui.button("Dark", on_click=dark.enable).classes("bg-gray-800 text-white p-2 rounded-lg")
            ui.button("Light", on_click=dark.disable).classes("bg-gray-200 text-black p-2 rounded-lg")

# Footer with Rounded Rectangle Input and Aligned Send Button
with ui.footer().classes("bg-gray-900 p-3 shadow-md"):
    with ui.row().classes("w-full max-w-3xl mx-auto items-center"):
        ui.input(placeholder="Type your message...").props(
            'rounded input-class="px-4 py-3 text-white border-0"'
        ).classes("flex-grow bg-gray-800 text-white rounded-lg")
        ui.button(icon="send", on_click=lambda: ui.notify("Message sent")).props(
            "flat color=white"
        ).classes("bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 ml-1 rounded-lg")

ui.run(title="Modern Chat Interface", dark=True)

