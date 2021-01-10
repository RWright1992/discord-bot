import discord
import asyncio
import time
import requests
import os

client = discord.Client()

@client.event
async def on_ready():
    with open("bengo.txt", "w") as file:
        pass
    print(f"We have logged in as {client.user}")

@client.event
async def on_member_join(member):
    try:
        role = member.guild.get_role(int(os.getenv("CANNON_FODDER")))
        await member.add_roles(role)
    except:
        print(f"Could not give the role {role} to {member}")

@client.event
async def on_message(message):
    print(f"{message.author.id}")
    if message.mention_everyone:
        insult = requests.get("https://insult.mattbas.org/api/insult")
        hashtag = str(message.author).find("#")
        person = str(message.author)[0:hashtag]
        async with message.channel.typing():
            await asyncio.sleep(3)
        await message.channel.send(f"{insult.text}, {person}")

    elif str(message.author) == os.getenv("HATED_USER"):
        time.sleep(1)
        with open("bengo.txt", "a") as file:
            text = f"Message: {message.content}. Time(UTC): {message.created_at} \r\n"
            file.write(text)
        await message.delete()
        async with message.channel.typing():
            await asyncio.sleep(3)
        await message.channel.send(f"simp")

    elif "bennybot.mute(" in message.content.lower():
        user_name = message.content.replace("bennybot.mute(", "")
        user_name = user_name.replace(")", "")
        user = message.guild.get_member_named(user_name)
        try:
            await user.edit(mute=True)
        except:
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"Oops, it seems that command didn't work, let me go ahead and clean it up for you.")
            print(f"Could not mute user {user}.")
        await message.delete()

    elif "bennybot.unmute(" in message.content.lower():
        user_name = message.content.replace("bennybot.mute(", "")
        user_name = user_name.replace(")", "")
        user = message.guild.get_member_named(user_name)
        try:
            await user.edit(mute=True)
        except:
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"Oops, it seems that command didn't work, let me go ahead and clean it up for you.")
            print(f"Could not unmute user {user}.")
        await message.delete()

    elif "bennybot.get_messages(bengo)" == message.content.lower():
        with open("bengo.txt", "r") as file:
            text = file.readlines()

            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send("\r\n".join(text))

    elif message.content.lower().startswith("bennybot.set_hated_user("):
        user_name = message.content.replace("bennybot.mute(", "")
        user_name = user_name.replace(")", "")
        os.environ("HATED_USER") = user_name
        message.delete()
    
    elif message.content.lower() == "bennybot.unset_hated_user()":
        os.environ("HATED_USER") = ""
        message.delete()

    elif "bennybot.logout()" == message.content.lower():
        await client.close()

    elif str(message.content).startswith("bennybot."):
        async with message.channel.typing():
            await asyncio.sleep(3)
        await message.channel.send(f"Oops, it seems that isn't a valid command, please try a different command.")

client.run(os.getenv('BOT_TOKEN'))