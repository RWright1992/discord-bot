import discord
import os
import asyncio
from discord.ext import commands

class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    # A check to see if the user is me.
    async def is_benny(ctx):
        return int(os.getenv('BENNY')) in ctx.author.roles
    
    @commands.command()
    @commands.check(is_benny)
    async def mute(self, ctx, person: discord.member):
        try:
            await person.edit(mute=True)
        except:
            async with ctx.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send(f"Oops, it seems that command didn't work, let me go ahead and clean it up for you.")
            print(f"Could not mute user {person}.")
        await ctx.message.delete()

    @commands.command()
    @commands.check(is_benny)
    async def unmute(self, ctx, person: discord.member):
        try:
            await person.edit(mute=False)
        except:
            async with ctx.message.channel.typing():
                await asyncio.sleep(3)
            await ctx.message.channel.send(f"Oops, it seems that command didn't work, let me go ahead and clean it up for you.")
            print(f"Could not unmute user {person}.")
        await ctx.message.delete()

def setup(client):
    client.add_cog(Mute(client))