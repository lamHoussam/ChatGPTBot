import discord
import openai
import json
import asyncio
from gtts import gTTS
import tempfile

with open('config.json') as f:
    config = json.load(f)

TOKEN = config['TOKEN']
APIKEY= config['API-KEY']
PREFIX = "$"

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

def answer_usage():
    return "$answer [question]","Answers question with ChatGPT's text-davinci-002 model."

def help_usage():
    return "$help","Sends this help message"

commands = {
    "help" : help_usage,
    "answer" : answer_usage,
}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]

    if args[0] == "help":
        mbd = discord.Embed(title='Help')

        for cmd, usg in commands.items():
            c, txt = usg()
            final_text = c + "\n" + txt
            mbd.add_field(name=cmd, value=final_text)

        mbd.color = discord.Color.orange()

        await message.channel.send(embed=mbd)
    
    
    elif(args[0] == "answer"):
        question = " ".join(args[1::])
        print(question)
        answer = answer_question(question)
        mbd = discord.Embed(title='Question', description=question)

        mbd.add_field(name='Answer', value=answer)

        mbd.color = discord.Color.green()

        await message.channel.send(embed=mbd)
    elif(args[0] == "audio"):

        vc_channel = message.author.voice.channel
        if vc_channel is None:
            message.reply("Not connected to a voice channel")
            return            

        question = " ".join(args[1::])
        print(question)
        answer = answer_question(question)

        text = 'Hello, this is a text-to-speech message'

        vc = await vc_channel.connect()
        await asyncio.sleep(5)

        with tempfile.NamedTemporaryFile() as fp:
            tts = gTTS(text=text)
            tts.write_to_fp(fp)
            fp.flush()
            vc.play(discord.FFmpegPCMAudio(fp.name))

            print("Duration : " + str(tts))

            # await asyncio.sleep(tts.duration)

            # await vc.disconnect()


    else:
        await message.reply("Unknown command")

client.run(TOKEN)
