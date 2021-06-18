import discord
import asyncio
import youtube_dl
from discord.ext import commands

# Suppress noise about console usage from errors
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
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicSFX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join(self, ctx):
        """Joins a voice channel"""
        # checks to see if the author is in a voice channel
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            return await ctx.send("You must be in a voice channel to use voice commands.")

        # if there is already a voice client existing in the guild
        if ctx.voice_client is not None:
            # moves the client to the current voice channel
            return await ctx.voice_client.move_to(channel)
        # if there is no currently existing voice client in the guild
        await channel.connect()

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Makes the bot leave voice"""
        await ctx.voice_client.disconnect()

    async def autostop(self, ctx):
        """Disconnects the bot from a voice channel when it stops playing audio"""
        # while the bot is playing something
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        await self.stop(ctx)

    async def play(self, ctx, *args, url, message: str = None):
        """Plays the audio from a Youtube video given the URL"""
        async with ctx.typing():
            await self.join(ctx)
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        if message:
            await ctx.send(message)
        await self.autostop(ctx)

    @commands.command(name="btr")
    async def btr(self, ctx):
        """Plays the funny Big Time Rush Theme song"""
        url = "https://www.youtube.com/watch?v=GUf7pPiZSNY"
        message = "Someone just got epicly styled on."
        await self.play(ctx, url=url, message=message)


    @commands.command(name="btrf")
    async def btrf(self, ctx):
        """Plays the full version of the Big Time Rush theme song"""
        url = "https://www.youtube.com/watch?v=XLZP1BbR9XI"
        message = "Someone just got very epicly styled on."
        await self.play(ctx, url=url, message=message)

    @commands.command(name="what")
    async def what(self, ctx):
        """what"""
        url = "https://www.youtube.com/watch?v=C_JR8U_YQEE"
        message = "what"
        await self.play(ctx, url=url, message=message)

    @commands.command(name="debate")
    async def debate(self, ctx):
        """Can be used during an intense argument"""
        url = "https://www.youtube.com/watch?v=UxnvGDK0WGM"
        message = "alright who's winning the argument"
        await self.play(ctx, url=url, message=message)

    @commands.command(name="damedane")
    async def damedane(self, ctx):
        """pain"""
        url = "https://www.youtube.com/watch?v=CAxFsO4ejMU"
        message = "pain :pain:"
        await self.play(ctx, url=url, message=message)






