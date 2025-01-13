# Dataiku DSS plugin for Steam

This plugin utilizes Steam's RESTful API to gather the recent gaming history of a single Steam user and create a DSS Dataset. It is designed to be called on a recurring schedule (via Scenario time trigger) and appended to an existing dataset. 

Since Steam doesn't expose specific gaming sessions, you can use this plugin to infer how much time a user is spending per day or week for individual games. Steam doesn't expose very much information about an individual's gaming history through their API, so this code relies on the IPlayerService/GetRecentlyPlayedGames API endpoint to gather information.

# Instructions
This plugin was designed and tested on Dataiku DSS v13.2.2. A Steam API key is required.

1) Optional: Locate a Steam User ID using the Steam username and this website: https://www.steamidfinder.com/ . The Steam User ID should be a long number that looks like "76561198842603734".
2) Login to Steam's website and get a Steam API key: https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
3) In Dataiku DSS, install this plugin via link in GitHub: Add Plugin, Fetch from Git Repository: ```git@github.com:THE-MOLECULAR-MAN/dataiku-plugin-steam-user-history.git``` and click Clone. Leave the other options as default.
4) Open an existing Dataiku DSS project create a new one. Edit the Project's local variables and add a new string variable named STEAM_API_KEY. Paste your Steam API key here. Be sure to include the quotes around it. Example:
```
{
  "STEAM_API_KEY": "0000090B0CD8D8DB900000AC00D00000"
}
```
5) Click Test & Get Schema. It should return the recent gaming history for the user ID. You can leave the default one (76561198842603734) to test.
6) Click Create
7) Add a Sync visual recipe to store the recent results into a persistent dataset like CSV or PostgreSQL. Be sure to enable "Append instead of overwrite".
8) Recommended: Create a new Scenario with a Time Trigger set to once per day, add a Step that performs a Build (forced rebuild) on the output dataset.

# Possible future features:
* gather entire steam catalog history by iterating IPlayerService/GetOwnedGames and each game and using IPlayerService/GetSingleGamePlaytime
* gather Steam achievement info to get clues on when a game was played for the first time.

# References
* https://partner.steamgames.com/doc/webapi/IPlayerService#GetRecentlyPlayedGames
* https://partner.steamgames.com/doc/webapi_overview#2
