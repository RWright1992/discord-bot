import discord
import requests
import asyncio
from discord.ext import commands
from discord.ext.commands.core import command

class Insult(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Insults the specified person")
    async def insult(self, ctx, *, person):
        insult = requests.get("https://insult.mattbas.org/api/insult")
        insult = insult.text.replace("Y", "y")
        async with ctx.channel.typing():
            await asyncio.sleep(3)
        await ctx.channel.send(f"{person}, {insult}")

def setup(client):
    client.add_cog(Insult(client))