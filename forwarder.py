from time import sleep
from os import getenv

from pyrogram import Client
from pyrogram.errors import FloodWait, UnknownError

API_ID = getenv('API_ID', None) or int(input('Enter your Telegram API id: '))
API_HASH = getenv('API_HASH', None) or input('Enter your Telegram API hash: ')

app = Client("client", api_id=API_ID, api_hash=API_HASH)
app.start()


class Forwarder:

    def __init__(self):
        self.search_chunk_size = 100

    @staticmethod
    def get_all_channels():
        dialogs = app.get_dialogs(pinned_only=True)

        dialog_chunk = app.get_dialogs()
        while len(dialog_chunk) > 0:
            dialogs.extend(dialog_chunk)
            dialog_chunk = app.get_dialogs(offset_date=dialogs[-1].top_message.date)

        return [d.chat for d in dialogs]

    def run(self):
        chats = self.get_all_channels()
        channels = [c for c in chats if c.type in 'channel']

        print('Copy all messages and posts in:')
        for i, channel in enumerate(channels):
            print(f'  {i + 1}. {channel.title}')

        n = int(input('Insert option number: '))

        if not 1 <= n <= len(channels):
            print('Invalid option selected. Exiting...')
            exit(-1)

        channel_to_copy = channels[n - 1]

        created_channel = app.create_channel("{title}_copy".format(title=channel_to_copy.title),
                                             "Posts from {title} channel".format(title=channel_to_copy.title))

        add_offset = 0

        while True:
            q = app.get_history(channel_to_copy.id, offset=add_offset, reverse=True)
            message_ids = [msg.message_id for msg in q]
            messages_count = len(q)
            print(f'Found {messages_count} of messages in "{channel_to_copy.title}"')

            while True:

                try:
                    app.forward_messages(chat_id=created_channel.id,
                                         from_chat_id=channel_to_copy.id,
                                         message_ids=message_ids,
                                         disable_notification=True)

                    print(f'Forwarded {messages_count} of messages to "{created_channel.title}"')

                    break

                except FloodWait as flood_exception:
                    sleep(flood_exception.x)

            if messages_count < self.search_chunk_size:
                break
            add_offset += self.search_chunk_size


if __name__ == '__main__':
    try:
        forwarder = Forwarder()
        forwarder.run()
    except UnknownError as e:
        print(f'UnknownError occured: {e}')
        print('Probably API has changed, ask developers to update this utility')
    finally:
        app.stop()
