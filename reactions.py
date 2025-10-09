import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.id_list = [570974287859810314, 757956524327829615]
        self.girl_id = 707651921653268541
        self.yarik_id = 705164601280561212
        self.monika_id = 341275729255858177

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith('/'):
            return
        if message.content.startswith('Дестериус'):
            channel = message.channel
            await channel.send('Z')
        if message.author.id in self.id_list:
            await message.channel.send('Иди нахуй')
        elif message.author.id == self.girl_id:
            await message.channel.send('Тише сельдь')
        elif message.author.id == self.monika_id:
            await message.channel.send('Сильвана убила короля лича')
        elif message.author.id == self.yarik_id:
            await message.channel.send('Я не шмель')
        await self.bot.process_commands(message)