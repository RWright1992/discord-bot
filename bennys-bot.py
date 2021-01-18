import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix="/b ")

@client.event
async def on_ready():
    with open("messages.txt", "w") as file:
        pass
    print(f"We have logged in as {client.user}")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('BOT_TOKEN'))