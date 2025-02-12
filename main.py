import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is online")
    

# Loads all cogs file from the ./cogs folder
async def load_extensions() -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main() -> None:
    await load_extensions()
    await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
