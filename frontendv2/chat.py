from nicegui import ui

# User profile image and chat layout
avatar="https://robohash.org/trix",
with ui.row().classes("items-start gap-2.5"):
    # Profile picture
    ui.image("/docs/images/people/profile-picture-3.jpg").classes(
        "w-8 h-8 rounded-full"
    )

    # Chat message container
    with ui.column().classes(
        "w-full max-w-[320px] leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700"
    ):
        # header with username and time
        with ui.row().classes("items-center space-x-2 rtl:space-x-reverse"):
            ui.label("bonnie green").classes(
                "text-sm font-semibold text-gray-900 dark:text-white"
            )
            ui.label("11:46").classes(
                "text-sm font-normal text-gray-500 dark:text-gray-400"
            )

        # chat message
        ui.label(
            "that's awesome. i think our users will really appreciate the improvements."
        ).classes("text-sm font-normal py-2.5 text-gray-900 dark:text-white")

        # delivery status
        ui.label("delivered").classes(
            "text-sm font-normal text-gray-500 dark:text-gray-400"
        )

    # dropdown button with menu
    with ui.button(icon="more_vert", color="white").props("flat round dense"):
        with ui.menu() as dropdown_menu:
            ui.menu_item("reply")
            ui.menu_item("forward")
            ui.menu_item("copy")
            ui.menu_item("report")
            ui.menu_item("delete")

# Chat bubble layout
with ui.row().classes('items-start gap-2.5 justify-start'):
    # Profile image
    ui.image('/docs/images/people/profile-picture-3.jpg').classes('w-8 h-8 rounded-full')

    # Message container
    with ui.column().classes('gap-1 w-full max-w-[320px]'):
        # Header: Name and Time
        with ui.row().classes('items-center space-x-2 rtl:space-x-reverse'):
            ui.label('Bonnie Green').classes('text-sm font-semibold text-gray-900 dark:text-white')
            ui.label('11:46').classes('text-sm font-normal text-gray-500 dark:text-gray-400')

        # Chat bubble
        with ui.column().classes('leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700'):
            ui.label("That's awesome. I think our users will really appreciate the improvements.").classes(
                'text-sm font-normal text-gray-900 dark:text-white'
            )

        # Delivery status
        ui.label('Delivered').classes('text-sm font-normal text-gray-500 dark:text-gray-400')

    # Dropdown Button
    with ui.button(icon='more_vert', color='white').props('flat round dense'):
        with ui.menu() as dropdown:
            ui.menu_item('Reply')
            ui.menu_item('Forward')
            ui.menu_item('Copy')
            ui.menu_item('Report')
            ui.menu_item('Delete')


def chat_bubble(message, sender=True):
    position_class = 'items-start' if sender else 'items-end'
    bubble_color = 'bg-blue-100 dark:bg-blue-700' if sender else 'bg-green-100 dark:bg-green-700'
    text_align = 'text-left' if sender else 'text-right'
    rounded_corner_sender = 'rounded-br-xl rounded-tl-xl' if sender else 'rounded-bl-xl rounded-tr-xl'
    image_url = 'https://robohash.org/{}.png'.format('sender' if sender else 'receiver')

    with ui.row().classes(f'gap-2.5 justify-start {position_class} w-full'):
        if sender:
            ui.image(image_url).classes('w-8 h-8 rounded-full')

        with ui.column().classes('gap-1 max-w-[300px]'):
            with ui.row().classes(f'items-center space-x-2 rtl:space-x-reverse {text_align}'):
                ui.label(username).classes('text-sm font-semibold text-gray-900 dark:text-white')
                ui.label('11:46').classes('text-sm font-normal text-gray-500 dark:text-gray-400')

            with ui.column().classes(f'leading-1.5 p-2 {bubble_color} {rounded_corner_sender}'):
                if reply_to:
                    with ui.column().classes(f'leading-1.5 p-1 {reply_color} rounded-lg w-full'):
                        ui.label(f"{username}: {reply_to}").classes('text-sm font-normal italic text-gray-700 dark:text-gray-300 p-1 rounded-lg')

                ui.label(message).classes('text-sm font-normal text-gray-900 dark:text-white p-2')

            ui.label('Delivered').classes('text-sm font-normal text-gray-500 dark:text-gray-400')

        if not sender:
            ui.image(image_url).classes('w-8 h-8 rounded-full')

# Example usage
with ui.column().classes('gap-4'):
    chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
    chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
    chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")

ui.run(title="Chat Interface", dark=True)
