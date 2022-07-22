import time
from telethon import TelegramClient
from telethon import errors
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from requests import get



api_id="15647704"
api_hash="872ada32b34a2cd7a0f951f31107caa7"
client = TelegramClient('anon', api_id, api_hash)


def get_song():
    token=	"BQBDPTeYcmTPLG_riJ-ydmELSCZjzzX6XNJ-1JF6pTIgAe-4rhKYbtbKMJKEagkCqOHA_JQe98jpvm5cmVKdCVZDJFzHonilidPpvtJUopCpW92hApdVHJzRZfmd5ZXGsGAwoY5LtP7q5Lk_r63veoH6cFvEMWqCnt6TMPzofyYU-09_XCbNznuOfyj1RGMDoKy0MEpgtrPqHBLN3FhEpf-aOASxwmeNj5Y94W-e68ZFjdm8Pp-Ja_p1yCicZ9SNBmDmY3AjJYzmtDU8LVH0Ao25J8t6RimduLKhyz_KzDgXAdxMnDdBajm59d8mCbu3CA064XH8zjvu5L7ZyW03Sw_D"
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
