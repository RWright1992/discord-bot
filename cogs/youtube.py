import discord
from discord import voice_client
from discord.player import FFmpegAudio, FFmpegPCMAudio
import youtube_dl
import asyncio
from discord.ext import commands

class Youtube(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.players = {}

    # A check to see if the user is a has the music role.
    async def has_music(ctx):
        return ctx.guild.get_role(int(os.getenv('MUSIC_ROLE'))) in ctx.author.roles

    @commands.command(brief="Bot will join voice for 10 mins and play link")
    async def play(self, ctx, url, length=600):
        channel = ctx.message.author.voice.channel
        await channel.connect()

        server = ctx.message.guild
        voice_channel = server.voice_client
        #song = FFmpegAudio(url)

        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: {player.title}')

        await asyncio.sleep(length)

        await voice_channel.disconnect()

    @commands.command(brief="Stop music playing and remove bot from voice")
    async def stop(self, ctx):
        voice_channel = ctx.message.guild.voice_client
        voice_channel.stop()
        await voice_channel.disconnect()

    @commands.command(brief="Pause music playing")
    async def pause(self, ctx):
        ctx.message.guild.voice_client.pause()

    @commands.command(brief="Resume paused music")
    async def resume(self, ctx):
        ctx.message.guild.voice_client.resume()
        

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

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def setup(client):
    client.add_cog(Youtube(client))