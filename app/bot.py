import os
import random
# from dotenv import load_dotenv
import discord
import youtube_dl
import asyncio
from music_cog import MusicSFX
from steam_cog import SteamGames
players = {}

# 1
from discord.ext import commands, tasks

# load_dotenv()
# Local env token
# TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = os.environ.get('DISCORD_TOKEN')

# 2

# Declaring intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await bot.change_presence(activity=discord.Game('Use $help for command list'))


@bot.command(name="snooze")
async def snooze(ctx):
    # testing asyncio.sleep()
    for i in range(1, 6):
        message = "Z" * i + "." * i
        await ctx.send(message)
        await asyncio.sleep(i)
    await ctx.send("*W O K E*")


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


@bot.command(name="sample", help="Sample embed message")
async def sampleEmbed(ctx):
    colour = discord.Colour.from_rgb(14, 59, 106)
    embed = discord.Embed(title="Sample Embed",
                          url="https://en.wikipedia.org/wiki/Cock_and_ball_torture",
                          description="This is an example of an embed message with different components huehue",
                          colour=colour.value
                          )
    embed.description = "bruh"
    embed.set_footer(text="bruh moment")
    # await ctx.send(embed=embed)
    embed1 = discord.Embed(title="Embed 1", description="This is the first embed.", colour=discord.Colour.red())
    embed2 = discord.Embed(title="Embed 2", description="This is the second embed.", colour=discord.Colour.green())
    embed3 = discord.Embed(title="Embed 3", description="This is the third embed.", colour=discord.Colour.blue())
    embeds = [embed1, embed2, embed3]
    buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
    current = 0
    # gets the object of the message so that we can edit it upon reaction
    msg = await ctx.send(embed=embeds[current])

    # having the bot add these reactions (buttons) for users to press
    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            embed = embeds[current]
            embed.set_footer(text="Timed out.")
            await msg.clear_reactions()

        else:
            past_page = current
            # if the user reacts with a rewind emoji
            if reaction.emoji == u"\u23EA":
                current = 0     # move them to the first page
            # if the user reacts with the backwards arrow emoji
            elif reaction.emoji == u"\u25C0":
                if current > 0:     # if there are pages to go backwards to
                    current -= 1    # moves the page backwards one
            # if the user reacts with the forwards arrow emoji
            elif reaction.emoji == u"\u25B6":
                if current < len(embeds) - 1:   # if there are pages to go forwards to
                    current += 1                # moves the page forwards one
            # if the user reacts with the fast forward emoji
            elif reaction.emoji == u"\u23E9":
                current = len(embeds) - 1       # moves the page to the last page
            # removes each reaction upon user reaction
            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            # if we are on a new page
            if current != past_page:
                await msg.edit(embed=embeds[current])



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
bot.add_cog(SteamGames(bot))

bot.run(TOKEN)
