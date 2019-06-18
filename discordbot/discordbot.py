#worker: python discordbot/discordbot.py
import discord
import os
import random 

try:
    from bottoken import *
    bottoken=BOTTOKEN
except:
    bottoken=os.environ.get('BOTTOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!website'):
        await message.channel.send('http://pokemondraftleague.online/')
    
    if message.content.startswith('!help'):
        await message.channel.send('Help documentation is under development.')

client.run(bottoken)