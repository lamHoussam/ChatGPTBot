import discord
import openai
import json

with open('config.json') as f:
    config = json.load(f)

TOKEN = config['TOKEN']
APIKEY= config['API-KEY']
PREFIX = "!"

def answer_question(question):
    openai.api_key = APIKEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        temperature=0.7,
        max_tokens=709,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].text)
    return response.choices[0].text


intents = discord.Intents.all()

intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]

    if(args[0] == "answer"):
        question = " ".join(args[1::])
        print(question)
        answer = answer_question(question)
        await message.channel.send(answer)
    else:
        await message.reply("Unknown command")

client.run(TOKEN)
