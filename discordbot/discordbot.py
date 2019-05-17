import discord
import os

debug=False
if debug==True:
    from bottoken import *
    bottoken=BOTTOKEN
else:
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

    await message.channel.send(message.guild)

client.run(bottoken)