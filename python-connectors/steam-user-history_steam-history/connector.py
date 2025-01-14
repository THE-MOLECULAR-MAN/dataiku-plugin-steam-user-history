# This file is the actual code for the custom Python dataset steam-user-history_steam-history

# import the base class for the custom dataset
import requests
import time
import pytz
from datetime import datetime
from six.moves import xrange
from dataiku.connector import Connector
import dataiku

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='steam-user-history_steam-history plugin %(levelname)s - %(message)s')

"""
A custom Python dataset is a subclass of Connector.

The parameters it expects and some flags to control its handling by DSS are
specified in the connector.json file.

Note: the name of the class itself is not relevant.
"""
class MyConnector(Connector):

    def __init__(self, config, plugin_config):
        """
        The configuration parameters set up by the user in the settings tab of the
        dataset are passed as a json object 'config' to the constructor.
        The static configuration parameters set up by the developer in the optional
        file settings.json at the root of the plugin directory are passed as a json
        object 'plugin_config' to the constructor
        """
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class

        # perform some more initialization
        logger.info('steam-user-history_steam-history plugin - Fetching steam user ID')
        self.steam_user_ids_list = self.config.get("steam_user_ids_list", "defaultValue")
        self.steam_api_key       = dataiku.get_custom_variables()["STEAM_API_KEY"]


    def get_read_schema(self):
        """
        Returns the schema that this connector generates when returning rows.

        The returned schema may be None if the schema is not known in advance.
        In that case, the dataset schema will be infered from the first rows.

        If you do provide a schema here, all columns defined in the schema
        will always be present in the output (with None value),
        even if you don't provide a value in generate_rows

        The schema must be a dict, with a single key: "columns", containing an array of
        {'name':name, 'type' : type}.

        Example:
            return {"columns" : [ {"name": "col1", "type" : "string"}, {"name" :"col2", "type" : "float"}]}

        Supported types are: string, int, bigint, float, double, date, boolean
        """

        # In this example, we don't specify a schema here, so DSS will infer the schema
        # from the columns actually returned by the generate_rows method
        return {"columns" : [
            {"name": "timestamp",     "type" : "date"}, 
            {"name" :"steam_user_id", "type" : "bigint"},
            {"name" :"app_id",        "type" : "bigint"},
            {"name" :"game_name",     "type" : "string"},
            {"name" :"playtime_2weeks_in_minutes",       "type" : "bigint"},
            {"name" :"playtime_all_time_in_minutes",     "type" : "bigint"},
        ]}
       

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.
        """
        logger.info('steam-user-history_steam-history plugin - Fetching STEAM_API_KEY from local project variables')
        
        if self.steam_api_key is not None:
            logger.info("steam-user-history_steam-history plugin - Successfully got API key")
        else:
            logger.error("steam-user-history_steam-history plugin - FAILED TO GET STEAM API KEY FROM LOCAL PROJECT VARIABLES")
            return None
        
        # https://doc.dataiku.com/dss/latest/variables/index.html
        # "The optional user-generated API key for accessing this user's data. Only required if the user's history is set to private. Ex: 0123445B0CD8D8DB92425FFFFFFFFFFF",
        
        STEAM_FQDN       = 'api.steampowered.com'
        url = f"https://{STEAM_FQDN}/IPlayerService/GetRecentlyPlayedGames/v1/"
        headers = {
            'x-webapi-key': self.steam_api_key
        }
        
        # result = []
        timestamp_request = datetime.now(pytz.timezone('US/Eastern')).isoformat()
        
        for iter_steam_user_id in list(set(self.steam_user_ids_list)):
            logger.info(f"steam-user-history_steam-history plugin - start of loop. iter_steam_user_id={iter_steam_user_id}")
            if iter_steam_user_id is None:
                continue
            
            params_steam = {
                'steamid': iter_steam_user_id,
                'count': 99
            }


            time.sleep(2) # sleep to avoid too many requests
            response = requests.get(url, headers=headers, params=params_steam)

            if response.status_code == 200:
                try:
                    data = response.json()['response']['games']
                    for game in data:
                        yield { "timestamp" :       timestamp_request,
                                "steam_user_id" :   str(iter_steam_user_id),
                                "app_id":           game['appid'],
                                "game_name":        game['name'],
                                "playtime_2weeks_in_minutes":   int(game['playtime_2weeks']),
                                "playtime_all_time_in_minutes": int(game['playtime_forever'])
                              }
                except KeyError:
                    logger.info(f"steam-user-history_steam-history plugin - {iter_steam_user_id} has no recent game history")
                    continue
            else:
                logger.info("steam-user-history_steam-history plugin - API call failed")
                logger.error(f"steam-user-history_steam-history plugin - Error: {response.status_code}, {response.text}")
                continue

    def get_writer(self, dataset_schema=None, dataset_partitioning=None,
                         partition_id=None, write_mode="OVERWRITE"):
        """
        Returns a writer object to write in the dataset (or in a partition).

        The dataset_schema given here will match the the rows given to the writer below.

        write_mode can either be OVERWRITE or APPEND.
        It will not be APPEND unless the plugin explicitly supports append mode. See flag supportAppend in connector.json.
        If applicable, the write_mode should be handled in the plugin code.

        Note: the writer is responsible for clearing the partition, if relevant.
        """
        raise NotImplementedError


    def get_partitioning(self):
        """
        Return the partitioning schema that the connector defines.
        """
        raise NotImplementedError


    def list_partitions(self, partitioning):
        """Return the list of partitions for the partitioning scheme
        passed as parameter"""
        return []


    def partition_exists(self, partitioning, partition_id):
        """Return whether the partition passed as parameter exists

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise NotImplementedError


    def get_records_count(self, partitioning=None, partition_id=None):
        """
        Returns the count of records for the dataset (or a partition).

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise NotImplementedError


class CustomDatasetWriter(object):
    def __init__(self):
        pass

    def write_row(self, row):
        """
        Row is a tuple with N + 1 elements matching the schema passed to get_writer.
        The last element is a dict of columns not found in the schema
        """
        raise NotImplementedError

    def close(self):
        pass
