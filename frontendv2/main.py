from nicegui import ui
from chat import *

dark = ui.dark_mode()
dark.enable()

tabs = ui.tabs().classes("flex-grow")

with ui.header().classes("bg-gray-900 text-white p-4 shadow-md") as header:
    with tabs:
        ui.tab("Chat")
        ui.tab("Settings")
        ui.tab("C")
    ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props(
        "flat color=white"
    ).classes("ml-auto p-2 rounded-lg bg-blue-500 hover:bg-blue-700 text-white")

with ui.footer(value=False).classes("bg-gray-900 text-white p-4 shadow-md") as footer:
    ui.label("Footer").classes("text-center w-full")

with ui.right_drawer(top_corner=False, bottom_corner=True).classes("bg-gray-800 text-white shadow-lg w-64") as right_drawer:
    ui.item_label("Contacts").props("header").classes("text-bold text-xl p-4")
    with ui.list().props("w-full separator").classes("w-full"):
        ui.separator()
        with ui.item(on_click=lambda: ui.notify("Selected contact 1")).classes("p-2 flex items-center"):
            with ui.item_section().props("avatar"):
                ui.icon("person").classes("text-blue-500")
            with ui.item_section():
                ui.item_label("Nice Guy").classes("text-lg")
            with ui.item_section().props("side"):
                ui.icon("chat").classes("text-blue-500")
        with ui.item(on_click=lambda: ui.notify("Selected contact 2")).classes("p-2 flex items-center"):
            with ui.item_section().props("avatar"):
                ui.icon("person").classes("text-blue-500")
            with ui.item_section():
                ui.item_label("Nice Person").classes("text-lg")
            with ui.item_section().props("side"):
                ui.icon("chat").classes("text-blue-500")

with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon="contact_support").props("fab color=blue").classes("p-2 rounded-lg bg-blue-500 hover:bg-blue-700 text-white")

with ui.tab_panels(tabs, value="Chat").classes(
    "w-full h-full mx-auto items-center p-4"
) as tab_panels:
    with ui.tab_panel("Chat"):
        with ui.column().classes('gap-4 w-full h-full overflow-auto'):
            chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
            chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
            chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")
    with ui.tab_panel("Settings"):
        ui.label("Settings").classes("text-2xl mb-4")
        with ui.row().classes("gap-4"):
            with ui.column().classes("flex-grow"):
                ui.label("OpenAI Whisper (voice transcription)").classes("text-xl mb-2")
                ui.upload(auto_upload=True).classes("w-full mb-2")
                transcription = ui.label().classes("text-lg")
            with ui.column().classes("flex-grow"):
                ui.label("Stable Diffusion (image generator)").classes("text-xl mb-2")
                prompt = ui.input("prompt").classes("w-full mb-2")
                ui.button("Generate").classes("w-full mb-2 p-2 rounded-lg bg-green-500 hover:bg-green-700 text-white")
                image = ui.image().classes("w-full")

    with ui.tab_panel("C"):
        ui.label("Content of C").classes("text-2xl mb-4")
        ui.label("Switch mode:").classes("text-lg mb-2")
        with ui.row().classes("gap-4"):
            ui.button("Dark", on_click=dark.enable).classes("bg-gray-800 text-white p-2 rounded-lg")
            ui.button("Light", on_click=dark.disable).classes("bg-gray-200 text-black p-2 rounded-lg")

with ui.footer().classes("bg-gray-900 p-4 shadow-md"):
    with ui.column().classes("w-full items-center"):
        with ui.row().classes("w-full gap-2"):
            text = (
                ui.input(placeholder="message")
                .on("keydown.enter", print("work"))
                .props("rounded outlined input-class=mx-3")
                .classes("flex-grow p-2")
            )
            ui.button("Send").classes("bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-700")

ui.run(title="Chat Interface", dark=True)
