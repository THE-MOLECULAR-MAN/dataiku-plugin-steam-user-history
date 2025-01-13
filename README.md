# Dataiku DSS plugin for Steam

This plugin utilizes Steam's RESTful API to gather the recent gaming history of a single Steam user and create a DSS Dataset. It is designed to be called on a recurring schedule (via Scenario time trigger) and appended to an existing dataset. 

Since Steam doesn't expose specific gaming sessions, you can use this plugin to infer how much time a user is spending per day or week for individual games. Steam doesn't expose very much information about an individual's gaming history through their API, so this code relies on the IPlayerService/GetRecentlyPlayedGames API endpoint to gather information.

# Instructions
This plugin was designed and tested on Dataiku DSS v13.2.2. Steam API keys are required to access your own Steam account if it is set to private.

1) Install the plugin in DSS via link in GitHub: Add Plugin, Fetch from Git Repository: ```git@github.com:THE-MOLECULAR-MAN/dataiku-plugin-steam-user-history.git```
2) Click Clone
3) Recommended: Get your Steam API key from Steam's site: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
4) In Dataiku DSS, create a new project or open an existing project. Edit the Porject's local variables and add a new one with the format:
```
{
  "STEAM_API_KEY": "0000090B0CD8D8DB900000AC00D00000"
}
```
5) Create a Project and add a Dataset: Steam User History
6) Locate your own Steam User ID using https://www.steamidfinder.com/ You can also leave the default ID for a popular public Steam user
7) Click Test & Get Schema. It should return the recent gaming history for the user ID.
8) Click create
9) Add a Sync visual recipe to store the recent results into a persistent dataset like CSV or PostgreSQL. Be sure to enable "Append instead of overwrite".

# Possible future features:
* gather entire steam catalog history by iterating IPlayerService/GetOwnedGames and each game and using IPlayerService/GetSingleGamePlaytime
* gather Steam achievement info to get clues on when a game was played for the first time.

# References
* https://partner.steamgames.com/doc/webapi/IPlayerService#GetRecentlyPlayedGames
* https://partner.steamgames.com/doc/webapi_overview#2
