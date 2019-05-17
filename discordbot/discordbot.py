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

    if message.content.startswith('Kick Sleepy') and (message.author.id==270800855677140994 or message.author.id==396785635991486466):
        sleepy=message.guild.get_member(248633879529783296)
        await sleepy.kick(reason="LOL Kicked by a bot")
        await message.channel.send('Finally. I thought you would never ask.')

client.run(bottoken)