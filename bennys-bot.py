import discord
import asyncio
import time
import requests
import os

client = discord.Client()
me = os.getenv('BOT_USER')
commands = "- `bennybot.insult(name)`"
players = {}

@client.event
async def on_ready():
    with open("messages.txt", "w") as file:
        pass
    print(f"We have logged in as {client.user}")

@client.event
async def on_member_join(member):
    try:
        role = member.guild.get_role(int(os.getenv("CANNON_FODDER")))
        await member.add_roles(role)
    except:
        print(f"Could not give the role to {member}")

@client.event
async def on_message(message):
    if str(message.author) != me:
        if message.mention_everyone:
            hashtag = str(message.author).find("#")
            person = str(message.author)[0:hashtag]
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"{person}, please be considerate of other users' notifications when using this tag.")

        if str(message.author) == os.getenv("HATED_USER"):
            time.sleep(1)
            with open("messages.txt", "a") as file:
                text = f"Message: {message.content}. Time(UTC): {message.created_at} \r\n"
                file.write(text)
            await message.delete()
            async with message.channel.typing():
                await asyncio.sleep(1)
            await message.channel.send(f"simp")
        
        elif message.content.lower().startswith("bennybot.insult("):
            person = message.content.replace("bennybot.insult(", "")
            person = person.replace(")", "")
            insult = requests.get("https://insult.mattbas.org/api/insult")
            insult = insult.text.replace("Y", "y")
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"{person}, {insult}")

        elif message.content.lower().startswith("bennybot.mute("):
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

        elif message.content.lower().startswith("bennybot.unmute("):
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

        elif "bennybot.get_messages()" == message.content.lower():
            with open("messages.txt", "r") as file:
                text = file.readlines()
                async with message.channel.typing():
                    await asyncio.sleep(3)
                await message.channel.send("\r\n".join(text))

        elif message.content.lower().startswith("bennybot.set_hated_user("):
            user_name = message.content.replace("bennybot.set_hated_user(", "")
            user_name = user_name.replace(")", "")
            os.environ["HATED_USER"] = user_name
            await message.delete()
        
        elif message.content.lower() == "bennybot.unset_hated_user()":
            os.environ["HATED_USER"] = ""
            await message.delete()

        elif "bennybot.logout()" == message.content.lower():
            await client.close()

        elif message.content.lower().startswith("bennybot.play("):
            link = message.content.replace("bennybot.play(", "")
            link = link.replace(")", "")
            channel = message.author.voice.voice_channel
            server = message.server
            await client.join_voice_channel(channel)
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(link)
            players[server.id] = player
            player.start()   

        elif message.content.lower() == "bennybot.commands()":
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"Hi, try out one of these commands: \r\n{commands}")

        elif str(message.content).startswith("bennybot."):
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f"Oops, it seems that isn't a valid command, run `bennybot.commands()` for a list of commands you can run.")

client.run(os.getenv('BOT_TOKEN'))