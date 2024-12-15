from nicegui import ui
from chat import *
dark = ui.dark_mode()
dark.enable()


with ui.header().classes("bg-green", replace="row items-center") as header:
    with ui.tabs() as tabs:
        ui.tab("Chat")
        ui.tab("Settings")
        ui.tab("C")
    ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props(
        "flat color=white"
    ).classes("items-end")

with ui.footer(value=False) as footer:
    ui.label("Footer")




with ui.right_drawer(top_corner=False, bottom_corner=True) as right_drawer:
    ui.item_label("Contacts").props("header").classes("text-bold")
    with ui.list().props("w-full separator").classes("w-full"):
        ui.separator()
        with ui.item(on_click=lambda: ui.notify("Selected contact 1")):
            with ui.item_section().props("avatar"):
                ui.icon("person")
            with ui.item_section():
                ui.item_label("Nice Guy")
                ui.item_label("name").props("caption")
            with ui.item_section().props("side"):
                ui.icon("chat")
        with ui.item(on_click=lambda: ui.notify("Selected contact 2")):
            with ui.item_section().props("avatar"):
                ui.icon("person")
            with ui.item_section():
                ui.item_label("Nice Person")
                ui.item_label("name").props("caption")
            with ui.item_section().props("side"):
                ui.icon("chat")


with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon="contact_support").props("fab")

with ui.tab_panels(tabs, value="Chat").classes(
    "w-full h-full  mx-auto items-center"
) as tab_panels:
    with ui.tab_panel("Chat"):
        with ui.column().classes('gap-4 w-full'):
            chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
            chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
            chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")
    with ui.tab_panel("Settings"):
        ui.label("Content of B")
        with ui.row().style("gap:10em"):
            with ui.column():
                ui.label("OpenAI Whisper (voice transcription)").classes("text-2xl")
                ui.upload(auto_upload=True).style("width: 20em")
                transcription = ui.label().classes("text-xl")
            with ui.column():
                ui.label("Stable Diffusion (image generator)").classes("text-2xl")
                prompt = ui.input("prompt").style("width: 20em")
                ui.button("Generate").style("width: 15em")
                image = ui.image().style("width: 60em")
    with ui.tab_panel("C"):
        ui.label("Content of C")
        ui.label("Switch mode:")
        with ui.row():
            ui.button("Dark", on_click=dark.enable)
            ui.button("Light", on_click=dark.disable)

with ui.footer().classes("bg-emerald-500"):
    with ui.column().classes("w-full items-center"):
        with ui.row().classes("w-fit"):
            text = (
                ui.input(placeholder="message")
                .on("keydown.enter", print("work"))
                .props("rounded outlined input-class=mx-3")
                .classes("mr-10 w-100 flex-grow ")
                .style("width: 20em")
            )
            ui.button("Send").classes("bg-red mr-10 w-100 flex-grow")
ui.run()
