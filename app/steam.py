import requests
import os
from dotenv import load_dotenv
wl_payload = {'p': 0}

wl_url = 'https://store.steampowered.com/wishlist/profiles//wishlistdata/'

load_dotenv()
# Steam API Token
STEAM_TOKEN = os.getenv('STEAM_TOKEN')


def getSteamUserID(username):
    id_payload = {"key": STEAM_TOKEN, "vanityurl": username}
    r = requests.get("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/", params=id_payload)
    r_json = r.json()

    # if the user exists/has spent $5
    if r_json["response"]["success"] == 1:
        # returns id as a string
        return r_json["response"]["steamid"]
    # if the user doesn't exist
    else:
        return "This user does not exist or has not spent $5 on Steam."


def form_url(id_):
    return "https://store.steampowered.com/wishlist/profiles/" + id_ + "/wishlistdata/"


def get_wl(url):
    r = requests.get(url, params=wl_payload)
    wl = r.json()
    return wl


def get_games(wl, upper_price=None):
    full_wl_games = [wl[item] for item in wl.keys()]
    games_list = []
    if not upper_price:
        for item in full_wl_games:
            # if the game has a price
            if len(item["subs"]) > 0 and "discount_block" in item["subs"][0]:
                games_list.append(find_price(item, upper_price))

    return games_list


def find_price(game, upper_price):
    game_info = {"title": game["name"]}
    discount_block = game["subs"][0]["discount_block"]
    # if there is a discount
    try:
        og_price = discount_block[discount_block.index("original_price") + 16 : discount_block.index('</div><div class=\"discount_final')]
        discount_price = discount_block[discount_block.index("discount_final_price") + 22:].strip("</div>")
    # if there isn't a discount
    except ValueError:
        og_price = discount_block[discount_block.index("discount_final_price") + 22:].strip("</div>")
        discount_price = None
    game_info["og_price"] = og_price
    game_info["discount_price"] = discount_price
    return game_info


# Running shit
# mps_url = 'https://store.steampowered.com/wishlist/profiles/76561198139212976/wishlistdata/'
#
# mps_wl = get_wl(mps_url)
# wl_games = get_games(mps_wl)

# for game in wl_games:
#     if game["discount_price"] is not None:
#         print(game["title"] + ": " + game["discount_price"])
#     else:
#         print(game["title"] + ": " + game["og_price"])

# print(getSteamUserID(""))

# print(wl_titles)
# print(r)
# print(r.url)
# print(dir(r))