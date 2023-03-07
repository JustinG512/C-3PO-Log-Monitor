# Main.py
import discord
import os
import asyncio


from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
YOUR_CHANNEL_ID = os.getenv('CHANNEL_ID')
LOG_FILE = "/var/log/auth.log"
client = discord.Client(intents=discord.Intents.default())

# Words to search for in the log file
SEARCH_WORDS = ['cinnamon', 'authentication', 'failure']

# Keep track of the last position in the file
last_position = os.path.getsize(LOG_FILE)

# Check for new lines containing the search words in the log file
async def check_log_file():
    global last_position
    while True:
        with open(LOG_FILE, 'r') as file:
            file.seek(last_position)
            line = file.readline().strip()
            while line:
                if any(word in line.lower() for word in SEARCH_WORDS):
                    await send_log_message(line)
                line = file.readline().strip()
            last_position = file.tell()
        await asyncio.sleep(1)

# Send the log message to the designated channel
async def send_log_message(message):
    channel = client.get_channel(int(YOUR_CHANNEL_ID))
    await channel.send(message)

# Discord bot events
@client.event
async def on_ready():
    print(f'{client.user} is online!')
    await check_log_file()

client.run(TOKEN)