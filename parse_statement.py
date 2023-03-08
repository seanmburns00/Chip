
#? This script sends a response request to open ai and returns the response

#imports
import os
import openai

from dotenv import load_dotenv

# load env file for tokens
load_dotenv("Tokens.env")

#changed temp from .8 to 1 (repetitiveness)
def parse(background, user, length, tone, input, temp=1.0, max_tokens=200, voice="informal"):

    # Load your API key from env file
    openai.api_key = os.environ['OPENAI']

    # Send request to openai and get response json
    responseJSON = openai.Completion.create(
        model="text-davinci-003",
        prompt=background + "Create a " + length + ", " + tone + " and " + voice + " response to " + user + ": Chip, " + input + "\n \n Chip: ",
        temperature=temp,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )

    # get text form json and return
    responseText = responseJSON.get("choices")[0].get("text")
    return responseText