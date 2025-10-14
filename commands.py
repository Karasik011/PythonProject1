import sqlite3
import discord
from discord.ext import commands
from stats import *
import pandas as pd
from stats import get_info

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def table(self,ctx,summoner_name,tag_name,count):
        try:
            result = await get_info(summoner_name, tag_name, count)
            table = pd.DataFrame(result)
            table.to_csv('table.csv')
            await ctx.send('Table created.', file=discord.File('table.csv'))
        except Exception as e:
            await ctx.send(f'Mistake {e}')


    @commands.command()
    async def stats(self, ctx, summoner_name: str, tag: str, count: int):
        try:
            result = await get_info(summoner_name, tag, count)
            table = pd.DataFrame(result)
            show_table = table.to_string(index=False)
            await ctx.send(f"```\n{show_table}\n```")
        except Exception as e:
            await ctx.send(f'Mistake {e}')

    @commands.command()
    async def test(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command()
    async def sums(self, ctx, arg: int, arg1: int):
        await ctx.send(arg + arg1)