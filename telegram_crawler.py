from telethon import TelegramClient, events, utils, types
from telethon.errors import (
    InviteHashExpiredError, InviteHashInvalidError, FloodWaitError,
    ChannelPrivateError, ChannelInvalidError
)
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import debugpy
import os
import asyncio
import re
import json

# Define the API ID and Hash from my.telegram.org
api_id = os.environ.get('TELEGRAM_API_ID')
api_hash = os.environ.get('TELEGRAM_API_HASH')

# Make usernames_to_process a global variable
usernames_to_process = []

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)
# URL regex pattern
url_pattern = r'(https?://[^\s]+)'

async def join_channel_or_chat(link):
    try:
        if 'joinchat' in link:
            invite_code = utils.resolve_invite_link(link).invite_code
            await client(ImportChatInviteRequest(invite_code))
            print(f"Joined the private entity {link}")
        elif 't.me/' in link:
            entity = await client.get_entity(link)
            if isinstance(entity, types.Channel):
                await client(JoinChannelRequest(entity))
                print(f"Joined the public channel {link}")
            else:
                print(f"The link {link} is not a channel or a group.")
    except (InviteHashExpiredError, InviteHashInvalidError):
        print(f"The invite link is invalid or expired: {link}")
    except (ChannelPrivateError, ChannelInvalidError):
        print(f"The channel is private or invalid: {link}")
    except FloodWaitError as e:
        print(f"Rate-limited. Must wait: {e.seconds} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")

async def message_to_json(message):
    # Create a dictionary to hold message data
    message_data = {
        'id': message.id,
        'text': message.text,
        'sender_id': message.sender_id,
        'date': message.date.isoformat() if message.date else None,
        'chat_id': message.chat_id,
        'is_reply': message.is_reply,
        'reply_to_msg_id': message.reply_to_msg_id,
        # Add any other attributes you need
    }
    # If the message has a sender, try to get the sender's username
    if message.sender_id:
        sender = await client.get_entity(message.sender_id)
        message_data['sender_username'] = getattr(sender, 'username', None)

    # Serialize the dictionary to a JSON string
    return json.dumps(message_data, ensure_ascii=False)

async def process_historical_messages_from_accounts(accounts):
    for account in accounts:
        print(f"Processing historical messages for {account}...")
        user = await client.get_entity(account)
        async for message in client.iter_messages(user):
            print(f"Processing message: {message.id} with content: {message.text}")
            links = re.findall(url_pattern, message.text)
            if links:
                for link in links:
                    print(f"Found link: {link}")
                    await join_channel_or_chat(link)
            else:
                print(f"No links found in message: {message.id}")
            
async def fetch_top_messages_from_each_channel_or_group():
    # Get all the dialogs (conversations, groups, channels)
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        # Check if the dialog is a channel or a group
        if isinstance(dialog.entity, (types.Channel, types.Chat)):
            print(f"\nFetching messages from {dialog.name} ({dialog.entity.id}):")

            # Fetch the top 5 messages from the channel or group
            async for message in client.iter_messages(dialog.entity, limit=5):
                message_json = await message_to_json(message)
                print(message_json)
                
async def main():
    global usernames_to_process
    # Start the debug server listening on the given port
    debugpy.listen(('0.0.0.0', 5678))
    print("⏳ Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("✅ Debugger attached!")

    await client.start()
    print("Client Created")
    
    # Get the list of usernames from the environment variable
    # assuming the environment variable is named 'TELEGRAM_USERNAMES' and the usernames are comma-separated
    usernames_to_process_env = os.getenv('TELEGRAM_USERNAMES', '')
    usernames_to_process = usernames_to_process_env.split(',')
    print(f"Usernames to process: {usernames_to_process}")

    # Ensure that empty strings are not included in case there are trailing commas
    usernames_to_process = [username.strip() for username in usernames_to_process if username.strip()]

    # Process historical messages from the specified list of accounts
    await process_historical_messages_from_accounts(usernames_to_process)

    # Fetch top messages from each channel or group
    await fetch_top_messages_from_each_channel_or_group()
    
    # Add this before 'await client.run_until_disconnected()' to start the event loop
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
