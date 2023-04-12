import time
from telethon import TelegramClient
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from requests import get



api_id=""
api_hash=""
client = TelegramClient('anon', api_id, api_hash)


def get_song():
    token=	""
    source = get(f"https://api.spotify.com/v1/me/player/currently-playing?access_token={token}").json()
    play = source['is_playing']
    if play:
        source = source['item']
        song = source["name"]
        artist = source['artists'][0]['name']
        return song, artist
    elif play==False:
        return



async def main():
    while True:
        try:
            get_song()
            time.sleep(2)
            song = get_song()[0]
            artist = get_song()[1]
            current_song = ("Playing : " + song + " - " + artist)
            full  = await client(GetFullUserRequest("me"))
            time.sleep(2)
            bio_song = full.about
            if current_song != bio_song:
                if len(current_song) <= 70:
                    await client(UpdateProfileRequest(
                        about=current_song
                    ))
                elif len(current_song) > 70:
                    current_song = song + " - " + artist
                    await client(UpdateProfileRequest(
                        about=current_song
                    ))
        
        except TypeError: 
            await client(UpdateProfileRequest(
                about="| Your current bio |"
            ))

        except errors.FloodWaitError as e:
            print("the flood gates have opened!")
            time.sleep(e.value)

    


with client:
    client.loop.run_until_complete(main())
