
#? Chip Bot 
#? This is a discord chat bot that is customizable and supports text and voice channel functionality.
#? This uses py-cord, openai, FFMPEG, and Uberduck.
#? See ReadMe file to get started. 
#? Author: Sean Burns / Buffaloninja#2047

# imports
import discord
import os
import time
import random
import whisper

from discord.ext import commands
from dotenv import load_dotenv
from parse_statement import parse
from tts import play_tts

#cload env file for tokens
load_dotenv("Tokens.env")

# initialize bot
intents = discord.Intents.all()
intents.members=True
client = commands.Bot(command_prefix=['c+','C+'], case_insensitive=True, intents=intents) # allow case insensitivity for better mobile experience (auto capitalize)

# set openai whisper model for stt
model = whisper.load_model("base")

#remove the default help command so that we can write out own
client.remove_command('help')

#!------------------------------------------------------------------------------------------------------------
#? ↓ BOT COMMANDS ↓
#!------------------------------------------------------------------------------------------------------------

# Help Command
@client.command()
async def help(ctx):

    embed = (discord.Embed(title='**Chip Help Menu**',
                               description=
                               '**Commands:** \n' + 
                                    '```   1. help: Bring up this menu \n' +
                                    '   2. helpme: Bring up legacy help menu \n' +
                                    '   3. about: Bring up Chip\'s about me \n' +
                                    '   4. join: Chip joins your current voice channel \n' +
                                    '   5. leave: Chip leaves your current voice channel \n' +
                                    '   6. chip (+ message): Chip responds to you in text chat \n' +
                                    '   7. vc_chip (+ message): Chip responds to you in voice chat \n' +
                                    '   8. tts (+ tts message): Chip speaks a typed tts message \n' +
                                    '   9. listen: Chip starts listening to you speak \n' +
                                    '   10. stop: Chip stops listening and respond to you \n' +
                                    '   11. fart: Chip releases some gas in the voice chat``` \n \n' +

                                '**Examples:** \n' +
                                    '```   1. c+help \n' +
                                    '   2. c+chip How was your day? \n' +
                                    '   3. c+tts You Rock! Cancel that. \n' +
                                    '   4. c+listen -> *you speak* -> c+stop \n' +
                                    '   5. c+fart```',
                               color=discord.Color.yellow())
                 .add_field(name='**Command Prefix**', value='c+')
                 .add_field(name='**Credits**', value='Sean (Buffaloninja#2047)')
                 .add_field(name='**Website**', value='[Click](https://seanburnsportfolio.com/)')
                 .add_field(name='**GitHub**', value='[Click](https://github.com/seanmburns00/Chip)'))
    
    await ctx.send(embed=embed) 


# Legacy Help Command
@client.command()
async def helpme(ctx):

    with open(r"txt_files\help_menu.txt", "r") as file:
        help_menu = file.read()

    await ctx.channel.send(help_menu)


# About Chip Command
@client.command()
async def about(ctx):

    file = discord.File(f"images/chip.jpg", filename=f"image.jpg")

    embed = (discord.Embed(title='**About Chip**',
                               description='```Chip is an imaginary friend bot. Is your discord dying, no one on anymore? Don\'t worry Chip is here. Chip is a discord chat bot with ' +
                                'voice and text functionality. By using openai Chip is able to have a customizable personality in which is used to create a text response ' +
                                'to you. Uberduck allows this response to then be turned into a .wav audio file by using their text-to-speech. This file is then played ' +
                                'in a voice chat. Lastly, by using openai\'s whisper api Chip is able to listen to what you are saying in a voice chat and respond back to you. ```',
                               color=discord.Color.yellow())
                 .add_field(name='**Credits**', value='Sean (Buffaloninja#2047)')
                 .add_field(name='**Website**', value='[Click](https://seanburnsportfolio.com/)')
                 .add_field(name='**GitHub**', value='[Click](https://github.com/seanmburns00/Chip)'))
    
    embed.set_image(url="attachment://image.jpg")
    
    await ctx.send(file=file, embed=embed) 


# join vc
@client.command()
async def join(ctx):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 

    # check if already connected
    if voice == None:
        # set vc to the channel
        vc = ctx.message.author.voice.channel

        # join vc
        await vc.connect()
        await ctx.send(f"Joined **{vc}**")
    else:
        # send return message
        await ctx.send("I'm already connected!")


# leave vc
@client.command()
async def leave(ctx):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return

    voice = ctx.voice_client

    # check if connected to vc
    if voice != None:
        # disconnect
        print("disconnecting")
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send("I am not connected to any voice channel!")


# play a random fart sound in vc
@client.command()
async def fart(ctx):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return
    
    # check if bot is connected to vc
    await bot_in_voice(ctx)

    # get audio file dir and ffmpeg.exe dir
    ffmpeg_exe = r"ffmpeg\bin\ffmpeg.exe"
    fart_dir = r"audio_files\fart_files" 

    # select random gas to leak
    gas_options = ['1', '2', '3', '4']
    gas = random.choice(gas_options)

    # prepare audio to be played
    prepared_audio = discord.FFmpegOpusAudio(f"{fart_dir}" + fr"\fart_{gas}" + ".wav", executable=ffmpeg_exe)
        
    # play audio and send message
    ctx.guild.voice_client.play(prepared_audio, after=None)
    await ctx.message.add_reaction('💩')
    await ctx.send("I farted.")


# play tts audio from command
@client.command()
async def tts(ctx, *, tts_message=""):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return
    
    # check if bot is connected to vc
    await bot_in_voice(ctx)

    if tts_message!="":
        # play tts message
        await play_tts(ctx, tts_message)
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send("You must add a message after the command.")


# text to chip and get response in text chat
@client.command()
async def chip(ctx, *, statement=""):

    if statement!="":
        # create openai prompt and get the reply
        reply = await get_response(ctx, statement)

        # send response message
        await ctx.channel.send(reply)
    else: 
        await ctx.send("You must add a message after the command.")


# text to chip and get response through text and voice chat
@client.command()
async def vc_chip(ctx, *, statement=""):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return

    # check if bot is connected to vc
    await bot_in_voice(ctx)

    if statement!="":
        # create openai prompt and get the reply
        reply = await get_response(ctx, statement)

        # play tts and send message
        await play_tts(ctx, reply)
        await ctx.send(reply)
    else: 
        await ctx.send("You must add a message after the command.")


# starts recording authors voice
@client.command()
async def listen(ctx):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return
    
    # check if bot is connected to vc
    await bot_in_voice(ctx)

    # record users audio and start callback when recording stops
    ctx.voice_client.start_recording(discord.sinks.WaveSink(), callback, ctx)
    await ctx.send("listening...")
    

# stops recording
@client.command()
async def stop(ctx):

    # check if user is in voice channel 
    voice_check = await user_in_voice(ctx)
    if voice_check == False:
        return
    
    # check if bot is connected to vc
    await bot_in_voice(ctx)
    
    ctx.voice_client.stop_recording()


#!------------------------------------------------------------------------------------------------------------
#? ↓ Helper Funtions ↓
#!------------------------------------------------------------------------------------------------------------

# Function to remove last N characters from string
def removeLastN(S, N):
    
    # Stores the resultant string
    res = ''
      
    # Traverse the string
    for i in range(len(S)-N):
        
          # Insert current character
        res += S[i]
  
    # Return the string
    return res


# Check if user is in voice channel
async def user_in_voice(ctx):

    vc = ctx.message.author.voice
    if vc == None:
        # send return message
        await ctx.send("You need to be in a voice channel to use this command")
        return False #return boolean to break out of command
    

# check if bot is connected to voice channel
#not used in join/leave due to needing slightly different functionality
async def bot_in_voice(ctx):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    # check if bot not in vc
    if voice == None:
        # connect
        vc = ctx.message.author.voice.channel
        vc = await vc.connect()


# create openai prompt and get response
async def get_response(ctx, statement):
        
    # show bot is typing while response generates
    async with ctx.typing():
        # get custom openai repsonse params
        with open(r"txt_files\openai_moods.txt", "r") as file:
            random_tones=file.read().splitlines()
            tone=random.choice(random_tones)

        with open("txt_files\openai_background.txt", "r") as file:
            background=file.read()

        length_list = ["short", "medium-length", "long", "very long"]
        length=random.choice(length_list)
        user = str(ctx.message.author)
        user = removeLastN(user, 5) #remove discord tag from user

        # get reply message from openai / print user statement and openai response
        reply = parse(background, user, length, tone, statement)
        print("\nCreate a " + f"{length}" + ", " + f"{tone}" + " and " + "informal response to " + f"{user}" + ":  Chip, " + f"{statement} \n" + f"\nReply: {reply}\n")
            
        #return response
        return reply


#if random user  set user id and author id to random
# call back, reads .wav file created from user speaking and responds in voice chat
async def callback(sink: discord.sinks, ctx):

    for user_id, audio in sink.audio_data.items():
        if user_id == ctx.author.id:

            # show bot is typing while response generates
            async with ctx.typing():
                # get audio recording data
                audio: discord.sinks.core.AudioData = audio
                #print(user_id) # debug print

                # create audio file and write data to it
                filename = "audio.wav"
                with open(filename, "wb") as file:
                    file.write(audio.file.getvalue())

                # load audio and trim to 30 seconds (openai_whisper allows max 30 seconds)
                audio = whisper.load_audio("audio.wav")
                audio = whisper.pad_or_trim(audio)
                #print("loaded.") # debug print

                # craete log-Mel spectrogram and transfer to model device
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                # detect the language user spoke
                _, probs = model.detect_language(mel)
                #print(f"Detected language: {max(probs, key=probs.get)}") #debug print

                # decode audio
                options = whisper.DecodingOptions(fp16=False)
                result = whisper.decode(model, mel, options).text
                
                # get custom openai repsonse params
                with open(r"txt_files\openai_moods.txt", "r") as file:
                    random_tones=file.read().splitlines()
                    tone=random.choice(random_tones)

                with open("txt_files\openai_background.txt", "r") as file:
                    background=file.read()

                length_list = ["short", "medium-length", "long", "very long"]
                length=random.choice(length_list)
            
                user = str(ctx.message.author)
                user = removeLastN(user, 5) #remove discord tag from user

                # get reply message from openai / print user statement and openai response
                reply = parse(background, user, length, tone, result)
                print("\nCreate a " + f"{length}" + ", " + f"{tone}" + " and " + "informal response to " + f"{user}" + ": " + f"{result} \n" + f"\nReply: {reply}\n")

            # play tts
            await play_tts(ctx, reply)


#!------------------------------------------------------------------------------------------------------------
#? ↓ Bot Events ↓
#!------------------------------------------------------------------------------------------------------------

# Base Events
@client.event
async def on_ready():

    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):

    await client.process_commands(message)
    if message.author == client.user:
        return

    # ping
    if message.content.startswith("ping"):
        await message.channel.send(f"Pong! Latency is {client.latency}")


#!------------------------------------------------------------------------------------------------------------
#? ↓ Start the Bot ↓
#!------------------------------------------------------------------------------------------------------------

# start the Bot
client.run(os.environ['DISCORD'])
