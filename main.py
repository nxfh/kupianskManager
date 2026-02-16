import asyncio
import discord
import hashlib
import logging
import math
import os
import time
from datetime import timedelta
from discord.ext import tasks

logger = logging.getLogger("Main")
streamHandler = logging.StreamHandler()
intents = discord.Intents.default()
client = discord.Client(intents = intents)
secondsBeforeNextPoll = 0

streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(logging.Formatter("[%(asctime)s - %(name)s]: %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(streamHandler)

@tasks.loop(seconds = 604800)
async def createPollTimer():
    createPoll()

@client.event
async def on_ready():
    logger.info("Logged in as")
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info("-----")
    logger.info(f"Hash: {getHash()}")
    logger.info("-----")

    secondsSinceLastPoll = (int(time.time()) - 212400) % 604800

    if secondsSinceLastPoll > 0:
        secondsBeforeNextPoll = 604800 - secondsSinceLastPoll

        if secondsSinceLastPoll <= 32400:
            createPoll()

    await wait(secondsBeforeNextPoll)
    logger.info("Starting poll timer...")
    createPollTimer.start()

async def createPoll():
    await client.wait_until_ready()
    logger.info("Creating poll...")

    pollDuration = math.ceil((32400 - (int(time.time()) - 212400) % 604800) / 3600)
    channel = client.get_channel(1469769978285916504)
    poll = discord.Poll(question = "Время:?", duration = timedelta(hours = pollDuration))

    poll.add_answer(text="11pm")
    poll.add_answer(text="11.30pm")
    poll.add_answer(text="12pm+")
    poll.add_answer(text="Не приду")

    await channel.send(f"<@&1155111077189799986>\n`ГОЛОСОВАНИЕ.mp3`", file = discord.File("img/gif.gif"))
    await channel.send(poll = poll)
    logger.info("Poll created")

async def wait(seconds):
    while seconds > 0:
        logger.info(f"Awaiting {seconds} seconds...")

        if seconds > 10:
            await asyncio.sleep(10)

            seconds -= 10
        else:
            await asyncio.sleep(seconds)

            seconds = 0

def getHash():
    hash = hashlib.new("md5")

    with open("main.py", "rb") as file:
        chunk = 0

        while chunk != b"":
            chunk = file.read(1024)

            hash.update(chunk)

        return hash.hexdigest()

client.run(os.getenv("API_KEY", ""))
