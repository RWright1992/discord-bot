import discord
from discord import voice_client
from discord.player import FFmpegAudio, FFmpegPCMAudio
import youtube_dl
import glob
import os
import asyncio
from discord.ext import commands

class Youtube(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = []

    # A check to see if the user is in a voice channel
    async def in_voice(ctx):
        return ctx.message.author.voice != None

    async def play_songs(self, ctx, voice_channel):
        while self.queue != []:
            async with ctx.typing():
                player = self.queue[0]
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send(f'Now playing: {player.title}')

            self.queue.remove(self.queue[0])

            while voice_channel.is_playing():
                await asyncio.sleep(1)
            
            await asyncio.sleep(3)

        await voice_channel.disconnect()

    @commands.command(brief="Bot will join voice and play specified song or queue song")
    @commands.check(in_voice)
    async def play(self, ctx, *, url):
        song = await YTDLSource.from_url(url)
        self.queue.append(song)

        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()

            server = ctx.message.guild
            voice_channel = server.voice_client
            await self.play_songs(ctx, voice_channel)
        except:
            async with ctx.typing():
                await asyncio.sleep(1)
            await ctx.send(f'Added to queue: {song.title}')

        await asyncio.sleep(5)

        delete()

    @commands.command(brief="Stop music playing and remove bot from voice")
    @commands.check(in_voice)
    async def stop(self, ctx):
        voice_channel = ctx.message.guild.voice_client
        voice_channel.stop()
        await voice_channel.disconnect()

        await asyncio.sleep(5)
        self.queue = []
        delete()

    @commands.command(brief="Pause music playing")
    @commands.check(in_voice)
    async def pause(self, ctx):
        ctx.message.guild.voice_client.pause()

    @commands.command(brief="Resume paused music")
    @commands.check(in_voice)
    async def resume(self, ctx):
        ctx.message.guild.voice_client.resume()

    @commands.command(brief="Show play queue")
    @commands.check(in_voice)
    async def queue(self, ctx):
        songs = [ song.title for song in self.queue ]
        newline = "\r\n"
        await ctx.send(f'Play queue is: {newline}{newline.join(songs)}')

    @commands.command(brief="Skip the current song")
    @commands.check(in_voice)
    async def skip(self, ctx):
        voice_channel = ctx.message.guild.voice_client
        voice_channel.stop()
        await self.play_songs(ctx, voice_channel)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def delete():
    webm = glob.glob('*.webm')
    m4a = glob.glob('*.m4a') 
    
    files = [x for x in webm] + [x for x in m4a]
    [os.remove(file) for file in files]

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def setup(client):
    client.add_cog(Youtube(client))