from discord.ext import commands
import asyncio
import random

class Random(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(brief='Sends happy matt or unhappy matt, randomly chosen')
    async def emoji(self, ctx):
        options = ["downmatt", "happymatt"]
        emote = random.choice(options)
        async with ctx.channel.typing():
            await asyncio.sleep(1)
        emoji = [x for x in ctx.guild.emojis if x.name == emote]
        await ctx.channel.send(f"<:{emoji[0].name}:{emoji[0].id}>")
    
    @commands.command(brief='roll a standard 6 sided dice')
    async def roll(self, ctx):
        async with ctx.channel.typing():
            await asyncio.sleep(1)
        await ctx.channel.send(f"{random.randint(1,6)}")

    @commands.command(brief='choose random item from a comma separated list')
    async def random(self, ctx, *, input: str):
        options = input.split(",")
        async with ctx.channel.typing():
            await asyncio.sleep(1)
        await ctx.channel.send(f"{random.choice(options)}")

def setup(client):
    client.add_cog(Random(client))