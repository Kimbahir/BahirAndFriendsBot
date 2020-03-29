import discord
import os
from PyTado.interface import Tado

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"Welcome to the server {member.mention} - you can write !help in the commands channel for a list of commands")


@client.event
async def on_message(message):
    id = client.get_guild(693111289261588551)
    channels = ["commands"]

    if message.author == client.user:
        return

    if str(message.channel) in channels:
        #print(f"Rejected because the channel was {message.channel}")
        msg = message.content.lower()

        if msg == "!help":
            await message.channel.send("My commands are !hello, !bmi, !slayer, !link, !weather and !users")

        elif message.content.startswith('!hello'):
            await message.channel.send('Hello!')

        elif message.content.startswith('!bmi'):
            if "help" in msg:
                await message.channel.send('To use BMI calculator, write: $bmi <height in meters> <weight in kgs>')
                await message.channel.send('Note: use "." as decimal seperator')
            else:
                cmd = msg.split(" ")
                height = float(cmd[1])
                weight = float(cmd[2])
                await message.channel.send(f"Your BMI is {(weight)/(height**2)}")

        elif message.content.startswith('!slayer'):
            await message.channel.send('Groesmeyer is the best slayer!!!')

        elif message.content.startswith('!link'):
            await message.channel.send('https://www.reddit.com/r/Vermintide/comments/831d6r/tome_and_grimoire_locations_with_screenshots/')

        elif message.content == "!users":
            await message.channel.send(f"# of Members are {id.member_count}")

        elif message.content == "!weather":
            await message.channel.send(getWeather())


def getWeather():
    t = Tado(os.environ['TADO_EMAIL'], os.environ['TADO_PASS'])
    w = t.getWeather()
    return f"It is now {w['outsideTemperature']['celsius']}C and the sun is shining on Hillerød with {w['solarIntensity']['percentage']}% intensity"


client.run(os.environ['DISCORD_TOKEN'])
