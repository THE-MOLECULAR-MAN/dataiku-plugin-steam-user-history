# Dataiku DSS plugin for Steam

This plugin utilizes Steam's RESTful API to gather the recent gaming history of a single Steam user. It is designed to be called on a recurring schedule (via Scenario time trigger) and appended to an existing dataset. 

Since Steam doesn't expose specific gaming sessions, you can use this plugin to infer how much time a user is spending per day or week for individual games.

Steam doesn't expose very much information about an individual's gaming history through their API, so this script relies on the IPlayerService/GetRecentlyPlayedGames endpoint to gather information about 

https://partner.steamgames.com/doc/webapi/IPlayerService#GetRecentlyPlayedGames

Possible future features:
* gather entire steam catalog history by iterating IPlayerService/GetOwnedGames and each game and using IPlayerService/GetSingleGamePlaytime
* gather Steam achievement info to get clues on when a game was played for the first time.

More info about Steam's RESTful API: https://partner.steamgames.com/doc/webapi_overview#2
