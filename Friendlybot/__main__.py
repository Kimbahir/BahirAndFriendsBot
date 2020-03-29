import discord
import os
from PyTado.interface import Tado
import time
import asyncio

client = discord.Client()
messages = joined = 0


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(
                    f"Time: {int(time.time())}, Messages: {messages}, Members joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


@client.event
async def on_member_join(member):
    global joined
    joined += 1
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
        global messages
        messages += 1
        msg = message.content.lower()

        if msg == "!help":
            await message.channel.send("My commands are !hello, !bmi, !slayer, !link, !items, !weather and !users")

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

        elif message.content == "!footknight":
            await message.channel.send("Bahir is teh knajt!")

        elif message.content == "!firemage":
            await message.channel.send("Magnus the Red is the Bomb! *KABOOM*")

        elif message.content.startswith('!link'):
            await message.channel.send('https://vermintide2.gamepedia.com/Book_Locations')

        elif message.content.startswith('!items'):
            await message.channel.send('https://vermintide2.gamepedia.com/Items')

        elif message.content == "!users":
            await message.channel.send(f"# of Members are {id.member_count}")

        elif message.content == "!weather":
            await message.channel.send(getWeather())


def getWeather():
    t = Tado(os.environ['TADO_EMAIL'], os.environ['TADO_PASS'])
    w = t.getWeather()
    return f"The temperature is {w['outsideTemperature']['celsius']}C and the sun is shining on Hillerød with {w['solarIntensity']['percentage']}% intensity"


client.loop.create_task(update_stats())
client.run(os.environ['DISCORD_TOKEN'])
