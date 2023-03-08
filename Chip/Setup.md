# Setup Overview
In this file you will find the step by step instructions on how to set up your own discord chatbot.

# Step 1: Python and package installing
First you will need to Python. 
    Python version: 3.8.2
    https://www.python.org/downloads/release/python-382/ 

Once Python is installed open a Comand Prompt (win + r, type 'cmd', click 'ok')
    you will need to run the following commands:
        py -3 -m pip install -U py-cord
        py -3 -m pip install -U py-cord[voice]
        py -3 -m pip install -U python-dotenv
        py -3 -m pip install -U openai
        py -3 -m pip install -U openai-whisper
        py -3 -m pip install ffmpeg

# Step 2: adding FFMPEG to your PATH
a ffmpeg cloned repository is included in this project. However, you will still need to add ffmpeg.exe to your PATH. 
To do this open file explorer, right click on 'This PC' -> properties -> advanced system settings -> environment variables
Once in the envieonment variables settings, under user variables scroll and click on PATH, then click edit.
Now click new and copy paste the directory to ffmpeg.exe (C:\path\to\bot\CHIP BOT\ffmpeg\bin)

# Step 3: Required Keys/Tokens
Now we need to setup the API keys needed. If you do not have keys for the following APIs search how to get them: 
    - openai (API key)
    - Uberduck (API key, API secret, and Basic AUTH code)

You will also need to create a private discord bot (so people can't add bot to other servers).
To do this go to https://discord.com/developers/applications and find a tutorial, plenty on YouTube.
Make sure to grab your bot token by following the tutorial.

When making the discord application, if you are interested in using the same picture, name, and bio as chip see the Discord Bot
Assets Folder. 

Now go into the 'Tokens.env' file and replace the example tokens with all yours you've acquired. (need ' ' around them)

You know have the functionality setup, only thing left to do is to give chip your own custom personality. 

# Step 4: setting up chatbot personality
First go to 'openai_moods.txt' in the txt_files folder. Use the current moods txt file as a template replacing the moods with 
your own. The more a mood is repeated the more likely for that mood to occur. 

Then go to 'openai_background.txt' in the txt_files folder. Read through and follow instructions on creating a background for 
your bot. Essentially you can add any information you want your bot to hold here as all this text is placed before the prompt 
to openai. Give it likes, dislikes, relationships with people, and anything else you want! This is the most fun and creative 
part of the process so enjoy it. 

# Step 5: Running the bot 
And there you go! Chip is all set up, to run chip start up a Command Prompt and run the following commands: 
    - cd C:\path\to\bot\CHIP BOT
    - python bot.py

In discord type c+help to see commands and have fun talking with your new friend!