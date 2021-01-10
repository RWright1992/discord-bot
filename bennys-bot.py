import discord
import asyncio
import time
import request

client = discord.Client()

@client.event
async def on_ready():
    with open("bengo.txt", "w") as file:
        pass
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"{message.author.id}")
    if "@everyone" in message.content.lower():
        insult = request.get("https://insult.mattbas.org/api/insult")
	async with message.channel.typing():
	    await asyncio.sleep(3)
	await message.channel.send(f"{insult})

    elif str(message.author) == "bengo#4992":
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
        await user.edit(mute=True)
        await message.channel.delete()

    elif "bennybot.unmute(" in message.content.lower():
        user_name = message.content.replace("bennybot.mute(", "")
        user_name = user_name.replace(")", "")
        user = message.guild.get_member_named(user_name)
        await user.edit(mute=False)
        await message.channel.delete()

    elif "bennybot.get_messages(bengo)" == message.content.lower():
        with open("bengo.txt", "r") as file:
            text = file.readlines()

            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send("\r\n".join(text))

    elif "bennybot.logout()" == message.content.lower():
        await client.close()

client.run("")