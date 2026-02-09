import asyncio
import discord
import logging
import os
import time
from datetime import timedelta
from discord.ext import tasks

logger = logging.getLogger("Main")
streamHandler = logging.StreamHandler()
intents = discord.Intents.default()
client = discord.Client(intents=intents)

streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(logging.Formatter("[%(asctime)s - %(name)s]: %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(streamHandler)

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
    logger.info("Logged in as")
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info("-----")
    
    secondsSinceLastInterrogation = (int(time.time()) - 241200) % 604800
    
    if secondsSinceLastInterrogation > 0:
        secondsBeforeNextInterrogation = 604800 - secondsSinceLastInterrogation

        while secondsBeforeNextInterrogation > 0:
            logger.info(f"Awaiting {secondsBeforeNextInterrogation} seconds...")

            if secondsBeforeNextInterrogation > 10:
                await asyncio.sleep(10)

                secondsBeforeNextInterrogation = secondsBeforeNextInterrogation - 10
            else:
                await asyncio.sleep(secondsBeforeNextInterrogation)

                secondsBeforeNextInterrogation = 0

    logger.info("Starting poll...")
    startPoll.start()

client.run(os.getenv("API_KEY", ""))
