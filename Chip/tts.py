
#? This script sends TTS request to Uberduck and plays TTS to discord voice channel

# imports
import requests
import discord
import tempfile
import nacl
import os
import aiohttp

from discord import FFmpegOpusAudio
from dotenv import load_dotenv

# load env file for tokens
load_dotenv("Tokens.env")

# Your Uberduck API key and API secret.
# Create one at https://app.uberduck.ai/account/manage (currently need paid tier :/ )
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
API_ROOT = "https://api.uberduck.ai"

ffmpeg_exe = r"ffmpeg\bin\ffmpeg.exe"

async def play_tts(ctx, text, pace=1):

    # show bot is typing while tts generates
    async with ctx.typing():

        url = f"{API_ROOT}/speak-synchronous"
        auth=aiohttp.BasicAuth(API_KEY, API_SECRET) #! currently not working get basic AUTH from Uberduck api documentation

        # set uberduck args
        payload = {"voice": "claptrap", "pace": pace, "speech": text} #todo make pace changeable
        headers = {
            "accept": "application/json",
            "uberduck-id": "anonymous",
            "content-type": "application/json",
            #"authorizaton": f"{auth}", #! (not working, found basic auth on uberduck api documentation and used below.)
            "authorization": os.environ['UBERDUCK'],
        }

        # get TTS 
        response = requests.post(url, json=payload, headers=headers)

    # create temp .wav file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio:
        # show bot is typing while tts generates
        async with ctx.typing():
            # write data to file
            audio.write(response.content)
            audio.flush()
            audio.seek(0)

            # if you get an error saying ffmpeg isn't defined, please go back to startup and install ffmpeg
            prepared_audio = discord.FFmpegOpusAudio(audio.name, executable=ffmpeg_exe)

        # play audio file in discord voice channel
        ctx.guild.voice_client.play(prepared_audio, after=None)

        #close temp file
        audio.close