# The Fool DBot

A basic Discord bot that can play music and sound effects in a Discord voice channel by user commands.

It can also retrieve data from the Steam API about a Steam user's video game wishlist. If given a Steam UserID, it can display a multi-page menu of all the games and their prices on that Steam user's wishlist.

Issue: Currently facing an issue where the Steam feature displays prices in CAD if run locally (since my PC is located in Canada). However, since it's hosted on Heroku that's based in USA, it ends up displaying the prices in USD. Note that I cannot simply just convert the price from USD to CAD because Steam does not price many of their games that way. Take Guilty Gear -Strive- for example. In the American Steam store, it is priced at $59.99 USD, which roughly converts to $75.50 CAD at the time of writing this. Now in the Canadian Steam store, it is overpriced at $79.99 CAD. Given that the Steam API does not have much detail in their documentation, I will have to find another way on finding the proper prices.
