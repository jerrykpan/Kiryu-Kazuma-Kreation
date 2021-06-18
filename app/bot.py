import os
import random
from dotenv import load_dotenv
import discord
import youtube_dl
from music_cog import MusicSFX
players = {}

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="hello", help="Responds with a random greeting")
async def hello(ctx):
    sayings = [
        'Hello!!!!!!!!!!!!!',
        "Wuz poppin\'?",
        "What's up?",
        "gaming",
        "YOOOO"
    ]
    response = random.choice(sayings)
    await ctx.send(response)


@bot.command(name="roll_dice", help="Simulates rolling N number of dice with S sides")
async def roll(ctx, dice_num: int, side_num: int):
    dice = [
        str(random.choice(range(1, side_num + 1)))
        for i in range(dice_num)
    ]
    await ctx.send(', '.join(dice))


# @bot.command(name="create_channel")
# @commands.has_role("Knight")
# async def create_channel(ctx, channel_name="castle-courtroom"):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)
#         await ctx.send(f"{channel_name} successfully created.")
#     else:
#         await ctx.send("There is already a channel with that name. Try again.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


# @bot.command(name="join")
# async def join(ctx):
#     channel = ctx.author.voice.channel
#
#     await channel.connect()
#
#
# @bot.command(name="leave")
# async def leave(ctx):
#     await ctx.voice_client.disconnect()
#
#
# # user does not have to be in channel to use this command?, sends the bot to a specific channel
# @bot.command(name="play")
# async def play(ctx, url : str, channel):
#     guild = ctx.guild
#     voice_channel = discord.utils.get(guild.voice_channels, name=channel)
#     voice = discord.utils.get(bot.voice_clients, guild=guild)
#
#     # if the proposed channel exists
#     if voice_channel:
#         # print(voice)
#         await voice_channel.connect()
#         # print(voice)
#     else:
#         await ctx.send("This channel does not exist.")
#
#
# @bot.command(name="btr")
# async def btr(ctx):
#     sfx_url = "https://www.youtube.com/watch?v=GUf7pPiZSNY"
#     guild = ctx.guild
#     voice_client = bot.voice_client_in(guild)
#     player = await voice_client.create_ytdl_player(sfx_url)
#     print("After await")
#     players[guild.id] = player
#     player.start()

@commands.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Commands List", description="Commands and what they do")
    embed.add_field(name="!hello", value="bruh")

bot.add_cog(MusicSFX(bot))

bot.run(TOKEN)
