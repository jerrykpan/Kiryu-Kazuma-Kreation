import discord
import asyncio
import youtube_dl
import os
from dotenv import load_dotenv
from discord import ChannelType
from discord.ext import commands, tasks
import random
from datetime import datetime

load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')

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
        # self.friday_night.start()

    @commands.command(name="join")
    async def join(self, ctx, chnl=None):
        """Joins a voice channel"""
        # checks to see if the author is in a voice channel
        if chnl:
            channel = chnl
        elif ctx.author.voice and ctx.author.voice.channel:
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

    async def play(self, ctx, *args, url, message: str = None, chnl=None):
        """Plays the audio from a Youtube video given the URL"""
        if chnl:
            await self.join(ctx, chnl)
        else:
            await self.join(ctx)
        async with ctx.typing():
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
        url = "https://www.youtube.com/watch?v=ihl4iHN2Ni4"
        message = "Someone just got __***very***__ epicly styled on."
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
        emoji = discord.utils.get(ctx.guild.emojis, name="pain")
        message = "pain " + str(emoji)
        await self.play(ctx, url=url, message=message)

    @commands.command(name="fridaynightost")
    async def fnost(self, ctx):
        """Ladies and gentlemen... the weekend."""
        url = "https://www.youtube.com/watch?v=IernJ-2gZ_U"
        message = "Ladies and gentlemen... the weekend."
        await self.play(ctx, url=url, message=message)

    @commands.command(name="seinfeld")
    async def seinfeld(self, ctx):
        """*slaps bass*"""
        url = "https://www.youtube.com/watch?v=EnPGGDWQMqk"
        message = "*slaps bass*"
        await self.play(ctx, url=url, message=message)

    @commands.command(name="seinfeldf")
    async def seinfeldf(self, ctx):
        """*slaps bass epicly*"""
        url = "https://www.youtube.com/watch?v=_V2sBURgUBI"
        message = "*slaps bass epicly*"
        await self.play(ctx, url=url, message=message)

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("work?")
        #
        # # get specific guild you want to have the functionality for
        # guild = discord.utils.get(self.bot.guilds, name=GUILD)
        #
        # # get all the voice channels in the guild
        # # the list comprehension returns a generator object, so list() turns it into a list
        # voice_channels = list(c for c in guild.channels if c.type == ChannelType.voice)
        #
        # # sort the list of vc's by size
        # # key is the function to run on each element, that's how it's compared
        # voice_channels.sort(key=lambda x: len(x.members))
        #
        # # if there are any active channels
        # if len(voice_channels[-1].members) > 0:
        #     # take the channel with the most members
        #     vc_choices = [voice_channels.pop()]
        #     # if there are multiple channels with the same number of members
        #     while len(voice_channels[-1].members) == len(vc_choices[0].members):
        #         vc_choices.append(voice_channels.pop())
        #     # picking a random channel if there are multiple channels with the same number of members
        #     if len(vc_choices) > 1:
        #         vc_to_join = random.choice(vc_choices)
        #     else:
        #         vc_to_join = vc_choices[0]
        #     # play friday night
        #     url = "https://www.youtube.com/watch?v=IernJ-2gZ_U"
        #     await self.play(ctx, url=url, chnl=vc_to_join)
        #
        # # if not, it is a sad day
        # else:
        #     tc_to_msg = discord.utils.find(lambda chnl: "bot" in chnl.name, guild.text_channels)
        #     await tc_to_msg.send("Seems like there won't be any celebrating tonight. :pensive:")

    # @tasks.loop(minutes=3.0)
    # async def friday_night(self):
    #     """
    #     Plays Friday Night at a particular time on Friday nights. Automatically joins the most populated voice channel.
    #     """
    #
    #     # get specific guild you want to have the functionality for
    #     guild = discord.utils.get(self.bot.guilds, name=GUILD)
    #
    #     # get all the voice channels in the guild
    #     # the list comprehension returns a generator object, so list() turns it into a list
    #     voice_channels = list(c for c in guild.channels if c.type == ChannelType.voice)
    #
    #     # sort the list of vc's by size
    #     # key is the function to run on each element, that's how it's compared
    #     voice_channels.sort(key=lambda x: len(x.members))
    #
    #     # if there are any active channels
    #     if len(voice_channels[-1].members) > 0:
    #         # take the channel with the most members
    #         vc_choices = [voice_channels.pop()]
    #         # if there are multiple channels with the same number of members
    #         while len(voice_channels[-1].members) == len(vc_choices[0].members):
    #             vc_choices.append(voice_channels.pop())
    #         # picking a random channel if there are multiple channels with the same number of members
    #         if len(vc_choices) > 1:
    #             vc_to_join = random.choice(vc_choices)
    #         else:
    #             vc_to_join = vc_choices[0]
    #         # play friday night
    #         url = "https://www.youtube.com/watch?v=IernJ-2gZ_U"
    #
    #         tc_to_msg = discord.utils.find(lambda chnl: "bot" in chnl.name, guild.text_channels)
    #         await tc_to_msg.send("Ladies and gentlemen, it's time to party.")
    #
    #         # connecting to a channel
    #         if guild.voice_client is not None:
    #             await guild.voice_client.move_to(vc_to_join)
    #         else:
    #             await vc_to_join.connect()
    #
    #         # playing the youtube video
    #         player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #         guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #         # waits to leave the channel
    #         while guild.voice_client.is_playing():
    #             await asyncio.sleep(1)
    #         await guild.voice_client.disconnect()
    #
    #     # if not, it is a sad day
    #     else:
    #         tc_to_msg = discord.utils.find(lambda chnl: "bot" in chnl.name, guild.text_channels)
    #         await tc_to_msg.send("Seems like there won't be any celebrating tonight. :pensive:")

    # @friday_night.before_loop
    # async def before_friday_night(self):
    #     print("Oh yeah baybee")
    #     await self.bot.wait_until_ready()
    #     await asyncio.sleep(5)
    #
    # @commands.command(name="nomorepartying")
    # async def cancel_fn(self, ctx):
    #     self.friday_night.cancel()
    #     await ctx.send("No more dancing I guess. :pensive:")

    # @tasks.loop(seconds=30.0)
    # async def reminder(self):
    #     print("e")
    #     waiting_time = random.randint(0, 15)
    #     print(waiting_time)
    #     await asyncio.sleep(waiting_time)
    #     guild = discord.utils.get(self.bot.guilds, name=GUILD)
    #     tc_to_msg = discord.utils.find(lambda chnl: "bot" in chnl.name, guild.text_channels)
    #     await tc_to_msg.send(str(waiting_time) + " peepeepoopoo")
    #
    # @commands.command(name="cancelr")
    # async def cancel_task(self, ctx):
    #     self.reminder.cancel()
    #     await ctx.send("Cancelled")








