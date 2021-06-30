import discord
from discord.ext import commands
import steam


class SteamGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getSteamID")
    async def getSteamID(self, ctx, username):
        await ctx.send(steam.getSteamUserID(username))
