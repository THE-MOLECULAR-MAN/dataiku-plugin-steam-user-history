# Dataiku DSS plugin for Steam

This plugin utilizes Steam's RESTful API to gather the recent gaming history of a single Steam user and create a DSS Dataset. It is designed to be called on a recurring schedule (via Scenario time trigger) and appended to an existing dataset. 

Since Steam doesn't expose specific gaming sessions, you can use this plugin to infer how much time a user is spending per day or week for individual games. Steam doesn't expose very much information about an individual's gaming history through their API, so this code relies on the IPlayerService/GetRecentlyPlayedGames API endpoint to gather information.

# Instructions
This plugin was designed and tested on Dataiku DSS v13.2.2. A Steam API key is required.

1) Locate your own Steam User ID using https://www.steamidfinder.com/ or leave the default ID for a popular public Steam user
2) Get your Steam API key from Steam's site: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
3) In Dataiku DSS, install the plugin in DSS via link in GitHub: Add Plugin, Fetch from Git Repository: ```git@github.com:THE-MOLECULAR-MAN/dataiku-plugin-steam-user-history.git``` and click Clone
4) Open an existing Dataiku DSS project create a new one. Edit the Project's local variables and add a new string variable named STEAM_API_KEY. Paste your Steam API key here. Be sure to include the quotes around it. Example:
```
{
  "STEAM_API_KEY": "0000090B0CD8D8DB900000AC00D00000"
}
```
5) Click Test & Get Schema. It should return the recent gaming history for the user ID.
6) Click create
7) Add a Sync visual recipe to store the recent results into a persistent dataset like CSV or PostgreSQL. Be sure to enable "Append instead of overwrite".

# Possible future features:
* gather entire steam catalog history by iterating IPlayerService/GetOwnedGames and each game and using IPlayerService/GetSingleGamePlaytime
* gather Steam achievement info to get clues on when a game was played for the first time.

# References
* https://partner.steamgames.com/doc/webapi/IPlayerService#GetRecentlyPlayedGames
* https://partner.steamgames.com/doc/webapi_overview#2
