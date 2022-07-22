import time
from telethon import TelegramClient
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from requests import get



api_id="15647704"
api_hash="872ada32b34a2cd7a0f951f31107caa7"
client = TelegramClient('anon', api_id, api_hash)


#client_id = "66776131775c4e4bb9657c25689ccfb9"
#client_secret = "09b711727ecf4584a9ba49c60edec0c0"



def get_song():
    token="BQAq6VCN9X8HwdnSao7dTTxgo10pNbwrgHR5RJsO-p9NFXWQ0yNn4Oiw8fi_D7g1JM4VP713tXtq5EZmab_VySjnEYtvy3S7_SYXupN8wW0CVRe6Q4sezYeg5Tk_uqhCvgp66KkTtPqe4rSgFPT2Izv86Cj5r1LjU0erwMEUx7ckc9JTLfqm2zWZKzn3K1DiKTgaJrugRcYr2S5BgDA83KKgy9fmpGEoI-pPs-i3CWDDMZ637zPTtbvJmo8KfIqyjSu0FSO-tU-047HHHU-yiiefBpIO3R-eVYjdas90zbzl7yctxicYWHPXa3IRJjxLAwYeI4ZEZ3sAlse3dEEiRivN"
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
                about="| Professional Retard |"
            ))

        except errors.FloodWaitError as e:
            print("the flood gates have opened!")
            time.sleep(e.value)

    


with client:
    client.loop.run_until_complete(main())
