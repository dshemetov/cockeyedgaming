# cfg.py

#Twitch Params
TWITCH_HOST = "irc.twitch.tv"               # the Twitch IRC server
TWITCH_PORT = 6667                          # always use port 6667!
TWITCH_NICK = "CrunkyBot"                   # your Twitch username, lowercase
TWITCH_PASS = "oauth:18evm5hvhgm32ojq1adwotj1ydqod2"  # your Twitch OAuth token
TWITCH_SUB_PASS = "oauth:5ajrivss516kladd3yz6ssf30ov50b"
TWITCH_CHAN = "cockeyedgaming"                    # the channel you want to join
TWITCH_RATE = (20/30) # Rate in msgs per sec.
TWITCH_FOLLOWS_URL = 'https://api.twitch.tv/kraken/channels/161192102/follows'
TWITCH_SUB_URL = 'https://api.twitch.tv/kraken/channels/161192102/subscriptions'
TWITCH_HEADERS = {'Accept': 'application/vnd.twitchtv.v5+json',
                  'Client-ID': 'i202c5n9be1v8cppav0fic5gfqe7jm',
                  'Authorization':TWITCH_PASS.split(":")[1]}
TWITCH_SUB_HEADERS = {'Accept': 'application/vnd.twitchtv.v5+json',
                      'Client-ID': 'i202c5n9be1v8cppav0fic5gfqe7jm',
                      'Authorization': 'OAuth ' + TWITCH_SUB_PASS.split(":")[1]}
TWITCH_V2_STREAMS_URL = 'https://api.twitch.tv/helix/streams'
TWITCH_V2_HEADERS = {'Client-ID': 'i202c5n9be1v8cppav0fic5gfqe7jm',
                     'Authorization': 'Bearer ' + TWITCH_PASS.split(":")[1]}

# Youtube params
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
KEY = "AIzaSyAW_7OHh5qAy1jrAIVMkXWfgdqJCuL0-0M"
DEVELOPER_KEY = KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#File locations
MUSIC_DOWNLOAD_DIR = r"C:\Users\Andrew\Music"
MUSIC_DB = r"C:\Users\Andrew\music.db"
DB_PATH = "dbs/crunky.db"
MUSIC_PLAYLIST = "/home/andrew/music/playlist.txt"
INSULTS = "insults.txt"

OPLIST = {}
FOLLOWERLIST = []
SUBLIST = []
