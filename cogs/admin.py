import discord
import os
import time
import asyncio
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    # A check to see if the user is a TMT member
    async def is_tmt(ctx):
        return ctx.guild.get_role(int(os.getenv('TMT_MEMBER'))) in ctx.author.roles

    # A check to see if the user is an Admin
    async def is_admin(ctx):
        return (ctx.guild.get_role(int(os.getenv('BENNY'))) in ctx.author.roles) or (ctx.guild.get_role(int(os.getenv('MATT'))) in ctx.author.roles)

    # Add to Cannon Fodder on join.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            role = member.guild.get_role(int(os.getenv("CANNON_FODDER")))
            await member.add_roles(role)
        except:
            print(f"Could not give the role to {member}")

    # Reply to messages which mention everyone.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mention_everyone:
            hashtag = str(message.author).find("#")
            person = str(message.author)[0:hashtag]

            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"{person}, please be considerate of other users' notifications when using this tag.")

    # Set the environment variable 'HATED_USER' to ignore have all their messages deleted.
    @commands.command(brief="Sets value of key to value")
    @commands.check(is_tmt)
    async def set(self, ctx, value: str="User#0000", key: str="HATED_USER"):
        os.environ[key] = value
        await ctx.message.delete()

    # Unset the environment variable 'HATED_USER'
    @commands.command(brief="Unsets value of key")
    @commands.check(is_tmt)
    async def unset(self, ctx, key: str="HATED_USER"):
        os.environ[key] = ""
        await ctx.message.delete()

    # Remove any messages from the hated user and store in messages.txt
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) == os.getenv("HATED_USER"):
            time.sleep(1)
            with open("./messages.txt", "a") as file:
                text = f"Message: {message.content}. Time(UTC): {message.created_at} \r\n"
                file.write(text)
            await message.delete()
            async with message.channel.typing():
                await asyncio.sleep(1)
            await message.channel.send(f"simp")

    # Retrieve hated user's messages
    @commands.command(brief="Retrieve recent deleted messages from hated user")
    @commands.check(is_tmt)
    async def get_messages(self, ctx):
        with open("./messages.txt", "r") as file:
            text = file.readlines()
        async with ctx.message.channel.typing():
            await asyncio.sleep(3)
        await ctx.message.channel.send("\r\n".join(text))

    @commands.command(brief="Logs the bot out - use if broken")
    @commands.check(is_admin)
    async def logout(self, ctx):
        await self.client.close()

def setup(client):
    client.add_cog(Admin(client))
