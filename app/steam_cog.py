import discord
from discord.ext import commands
import steam
import asyncio

steam_rgb = (14, 59, 106)


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

    @commands.command(name="wl", help="Returns all the games on your Steam wishlist under $X (optional price limit) sorted by ascending price.")
    async def get_wl_prices(self, ctx, username=None, price_limit: float = None):
        # if they provide a username and price limit
        if username is not None:
            user_id_msg = steam.getSteamUserID(username)
            # if we really got the user's ID
            if user_id_msg.isdigit():
                user_url = steam.form_url(user_id_msg)
                user_wl = steam.get_wl(user_url)
                # if the user's wishlist is public
                if not isinstance(user_wl, str):
                    user_games = steam.get_games(user_wl, price_limit)
                    await self.set_wl_embed(ctx, user_games)
                # if the user's wishlist is not public
                else:
                    await ctx.send(user_wl)
            else:
                await ctx.send(user_id_msg)
        else:
            await ctx.send("You need to include your username.")

    async def set_wl_embed(self, ctx, wl_games):
        current_pg = 0
        interval = 10
        last_pg = len(wl_games) // interval
        desc = await self.set_wl_desc(wl_games, current_pg, last_pg, interval)
        wl_embed_colour = discord.Colour.from_rgb(14, 59, 106)
        wl_embed = discord.Embed(title="Your Steam Wishlist", colour=wl_embed_colour)
        current_pg = 0
        wl_embed.set_footer(text="Pg " + str(current_pg+1) + " of " + str(last_pg+1))
        # reaction buttons for user to push
        buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
        wl_embed.description = desc
        msg = await ctx.send(embed=wl_embed)

        # adding the reaction buttons to the msg
        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                wl_embed.set_footer(text="Timed out.")
                await msg.edit(embed=wl_embed)
                await msg.clear_reactions()

            else:
                past_pg = current_pg
                # if the user reacts with a rewind emoji
                if reaction.emoji == u"\u23EA":
                    current_pg = 0     # move them to the first page
                # if the user reacts with the backwards arrow emoji
                elif reaction.emoji == u"\u25C0":
                    if current_pg > 0:          # if there ar pages to go back to
                        current_pg -= 1         # moves the page backwards one
                # if reacted with forwards arrow emoji
                elif reaction.emoji == u"\u25B6":
                    if current_pg < last_pg:    # if there are pages to go forward to
                        current_pg += 1         # moves the page fowards one
                # if reacted with the fast forward button
                elif reaction.emoji == u"\u23E9":
                    current_pg = last_pg        # moves the page to the last page
                # removes all button reactions upon reaction
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                # if we are on a new page
                if current_pg != past_pg:
                    desc = await self.set_wl_desc(wl_games, current_pg, last_pg, interval)
                    wl_embed.description = desc
                    wl_embed.set_footer(text="Pg " + str(current_pg+1) + " of " + str(last_pg+1))
                    await msg.edit(embed=wl_embed)


    async def set_wl_desc(self, wl_games, current_pg, last_pg, interval):
        lines = []
        if current_pg != last_pg:
            for game in wl_games[current_pg*interval:current_pg*interval+interval]:
                line = game["title"] + ": " + "$"
                if game["discount_price"] is not None:
                    line += game["discount_price"] + "  ~~$" + game["og_price"] + "~~"
                else:
                    line += game["og_price"]
                lines.append(line)
        else:
            for game in wl_games[current_pg*interval:]:
                line = game["title"] + ": " + "$"
                if game["discount_price"] is not None:
                    line += game["discount_price"] + "  ~~$" + game["og_price"] + "~~"
                else:
                    line += game["og_price"]
                lines.append(line)
        desc = "\n".join(lines)
        return desc


# import steam
