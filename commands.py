import sqlite3
import os
import discord
from discord.ext import commands
from stats import *
import pandas as pd
from stats import get_info

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def table(self,ctx,summoner_name,tag_name,count, mode):
        try:
            result = await get_info(summoner_name, tag_name, count, mode)
            file = f'{summoner_name}.csv'
            result.to_csv(file)
            await ctx.send('Table created.', file=discord.File(file))
            os.remove(file)
        except Exception as e:
            await ctx.send(f'Mistake {e}')

    @commands.command()
    async def counter(self,ctx, cnt: int):
        rofl_cnt = []

        await ctx.send(f'Количество хуевых шуток дестериуса:{rofl_cnt}')




    @commands.command()
    async def stats(self, ctx, summoner_name: str, tag: str, count: int, mode: str):
        try:
            result = await get_info(summoner_name, tag, count, mode)
            show_table = result.to_string(index=False)
            await ctx.send(f"```\n{show_table}\n```")
        except Exception as e:
            await ctx.send(f'Mistake {e}')

    @commands.command()
    async def test(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command()
    async def sums(self, ctx, arg: int, arg1: int):
        await ctx.send(arg + arg1)

    # @commands.command()
    # async def plot(self, ctx, summoner_name, tag_name, count, x_label, y_label, title):

