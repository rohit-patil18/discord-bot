import discord
import os
import csv
import random
import requests
import json
from keep_alive import keep_alive

# iniitializing discord client
client = discord.Client()

# For messages from imported csv file
phrases = []
with open("phrases.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    for row in csv_reader:
        phrases.append(row[1])

# For messages via APIs
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote

@client.event
async def on_ready():
    print("{0.user} has logged in now!".format(client))

@client.event
async def on_message(message):
    # When message is sent by bot itself
    if message.author == client.user:
        return

    msg = message.content

    # Greeting
    if msg.startswith('$hello'):
        await message.channel.send(f"Hello! How are you {message.author}?")
    
    # Response via csv file
    if "$thought" in msg:
        reply = phrases[random.randint(0, len(phrases) - 1)]
        await message.channel.send(reply)

    # Response via API
    if msg.startswith("$quote"):
        reply = get_quote()
        await message.channel.send(reply)

keep_alive()
my_secret = os.environ['TOKEN'] # TOKEN = Your discord channel token
client.run(my_secret)