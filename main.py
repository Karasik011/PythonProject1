
import pandas as pd
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from stats import *
from reactions import Reactions
from commands import Commands
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True # Enable message content intent for commands
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    print(f'Guild owner:\n - {guild.owner}')


async def setup_bot():
    await bot.add_cog(Commands(bot))
    await bot.add_cog(Reactions(bot))

async def main():
    async with bot:
        await setup_bot()
        await bot.start(TOKEN)

if __name__ == "__main__":
     asyncio.run(main())



