from nicegui import ui

def chat_bubble(message, sender=True, reply_to=None, username="User Name"):
    position_class = 'justify-start' if sender else 'justify-end'
    bubble_color = 'bg-blue-100 dark:bg-blue-700' if sender else 'bg-green-100 dark:bg-green-700'
    reply_color = 'bg-blue-200 dark:bg-blue-800' if sender else 'bg-green-200 dark:bg-green-800'
    text_align = 'text-left' if sender else 'text-right'
    rounded_corner_sender = 'rounded-br-xl rounded-tl-xl' if sender else 'rounded-bl-xl rounded-tr-xl'
    image_url = 'https://robohash.org/{}.png'.format('sender' if sender else 'receiver')

    with ui.row().classes(f'gap-2.5 {position_class} w-full'):
        if sender:
            ui.image(image_url).classes('w-8 h-8 rounded-full')

        with ui.column().classes(f'gap-1 max-w-[300px] {position_class}'):
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
# with ui.column().classes('gap-4 w-full'):
#     chat_bubble("That's awesome. I think our users will really appreciate the improvements.", sender=True, username="Bonnie Green")
#     chat_bubble("I agree! Let's move forward with the updates.", sender=False, username="Alex Brown")
#     chat_bubble("Sure, I'll handle that right away.", sender=True, reply_to="I agree! Let's move forward with the updates.", username="Bonnie Green")

ui.run(title="Chat Interface", dark=True)
