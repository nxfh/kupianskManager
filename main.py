import discord
import time
import asyncio
from datetime import timedelta
from discord.ext import tasks

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(seconds=604800)
async def startPoll():
    await client.wait_until_ready()

    channel = client.get_channel(1469769978285916504)
    poll = discord.Poll(question="Время:?", duration=timedelta(hours=1.0))

    poll.add_answer(text="11pm")
    poll.add_answer(text="11.30pm")
    poll.add_answer(text="12pm+")
    poll.add_answer(text="Не приду")

    await channel.send(f"<@&1155111077189799986>\n`ГОЛОСОВАНИЕ.mp3`", file=discord.File("img/gif.gif"))
    await channel.send(poll=poll)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----")
    
    secondsSinceLastInterrogation = (int(time.time()) - 241200) % 604800
    
    if secondsSinceLastInterrogation > 0:
        secondsBeforeNextInterrogation = 604800 - secondsSinceLastInterrogation

        while secondsBeforeNextInterrogation > 0:
            print(f"Awaiting {secondsBeforeNextInterrogation} seconds...")

            if secondsBeforeNextInterrogation > 10:
                await asyncio.sleep(10)

                secondsBeforeNextInterrogation = secondsBeforeNextInterrogation - 10
            else:
                await asyncio.sleep(secondsBeforeNextInterrogation)

                secondsBeforeNextInterrogation = 0

    print("Starting poll...")
    startPoll.start()
