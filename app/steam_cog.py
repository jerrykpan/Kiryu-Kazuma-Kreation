import discord
from discord.ext import commands
import steam


class SteamGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getSteamID", help="Returns your Steam # ID given your username")
    async def getSteamID(self, ctx, username=None):
        # if the user forgets to include their username
        if username is not None:
            user_id_msg = steam.getSteamUserID(username)
            if user_id_msg.isdigit():
                await ctx.send("Steam ID: " + steam.getSteamUserID(username))
            else:
                await ctx.send(user_id_msg)
        else:
            await ctx.send("You need to include your username with this command.")
