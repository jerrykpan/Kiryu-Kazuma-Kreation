import requests
import os
from dotenv import load_dotenv
wl_payload = {'p': 0}

wl_url = 'https://store.steampowered.com/wishlist/profiles//wishlistdata/'

# load_dotenv()
# Steam API Token
# STEAM_TOKEN = os.getenv('STEAM_TOKEN')
STEAM_TOKEN = os.environ.get('STEAM_TOKEN')



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
    try:
        if wl["success"] == 2:
            return "You must change your \'Game details\' on your profile to Public in order for this bot to access your wishlist."\
                   " You can do this by going to your profile, clicking \'Edit Profile\' and changing your \'Game details\' to Public "\
                   "in the \'Privacy settings\' tab."
    except KeyError:
        return wl


def get_games(wl, upper_price=None):
    full_wl_games = [wl[item] for item in wl.keys()]
    games_list = []
    for item in full_wl_games:
        # if the game has a price
        if len(item["subs"]) > 0 and "discount_block" in item["subs"][0]:
            game = find_price(item)
            # if there is a price limit
            if upper_price is not None:
                # if the game is on discount
                if game["discount_price"] is not None:
                    # if the game is below the price limit
                    if float(game["discount_price"]) < upper_price:
                        games_list.append(game)
                # if the game is not on discount
                else:
                    if float(game["og_price"]) < upper_price:
                        games_list.append(game)
            # if there is no price limit
            else:
                games_list.append(find_price(item))

    games_list.sort(key=lowest_price_of_game)

    return games_list


def find_price(game):
    game_info = {"title": game["name"]}
    discount_block = game["subs"][0]["discount_block"]
    # if there is a discount
    try:
        og_price = discount_block[discount_block.index("original_price") + 21 : discount_block.index('</div><div class=\"discount_final')]
        discount_price = discount_block[discount_block.index("discount_final_price") + 27:].strip("</div>")
    # if there isn't a discount
    except ValueError:
        og_price = discount_block[discount_block.index("discount_final_price") + 27:].strip("</div>")
        discount_price = None
    game_info["og_price"] = og_price
    game_info["discount_price"] = discount_price
    return game_info


def lowest_price_of_game(game):
    if game["discount_price"] is not None:
        return float(game["discount_price"])
    else:
        return float(game["og_price"])

# Running shit
def runshit(upper_price=None):
    mps_url = 'https://store.steampowered.com/wishlist/profiles/76561198139212976/wishlistdata/'

    mps_wl = get_wl(mps_url)
    wl_games = get_games(mps_wl, upper_price)

    for game in wl_games:
        if game["discount_price"] is not None:
            print(game["title"] + ": " + game["discount_price"])
        else:
            print(game["title"] + ": " + game["og_price"])


# runshit(10)  # testing

#
# print(getSteamUserID(""))

# print(wl_titles)
# print(r)
# print(r.url)
# print(dir(r))