# Dataiku DSS plugin for Steam

This plugin utilizes Steam's RESTful API to gather the recent gaming history of a single Steam user. It is designed to be called on a recurring schedule (via Scenario time trigger) and appended to an existing dataset. 

Since Steam doesn't expose specific gaming sessions, you can use this plugin to infer how much time a user is spending per day or week for individual games.

Steam doesn't expose very much information about an individual's gaming history through their API, so this script relies on the IPlayerService/GetRecentlyPlayedGames endpoint to gather information about 

https://partner.steamgames.com/doc/webapi/IPlayerService#GetRecentlyPlayedGames

Possible future features:
* gather entire steam catalog history by iterating IPlayerService/GetOwnedGames and each game and using IPlayerService/GetSingleGamePlaytime
* gather Steam achievement info to get clues on when a game was played for the first time.

More info about Steam's RESTful API: https://partner.steamgames.com/doc/webapi_overview#2

# Instructions
This plugin was designed and tested on Dataiku DSS v13.2.2. Steam API keys are required to access your own Steam account if it is set to private.

1) Install the plugin in DSS via link in GitHub: Add Plugin, Fetch from Git Repository: git@github.com:THE-MOLECULAR-MAN/dataiku-plugin-steam-user-history.git
2) Click Clone
3) Get your Steam API key here. A steam account is required: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
4) In Dataiku DSS, create a new project or open an existing project. Edit the Porject's local variables and add a new one with the format:
{
  "STEAM_API_KEY": "0000090B0CD8D8DB900000AC00D00000"
}
5) Create a Project and add a Dataset: Steam User History
6) Locate your own Steam User ID using https://www.steamidfinder.com/ You can also leave the default ID for a popular public Steam user
7) Click Test & Get Schema. It should return the recent gaming history
9) Click create
