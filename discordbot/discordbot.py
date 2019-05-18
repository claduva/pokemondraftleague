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

    if message.content.startswith('Kick Sleepy') and (message.author.id==270800855677140994 or message.author.id==396785635991486466 or message.author.id==291710529981120524):
        sleepy=message.guild.get_member(248633879529783296)
        await sleepy.kick(reason="LOL Kicked by a bot")
        await message.channel.send('Finally. I thought you would never ask.')
    
    if message.content.startswith('blob me times'):
        number=message.content.split(" ")[3]
        if int(number) < 31:
            blobs=[client.get_emoji(496772116897857537),client.get_emoji(475876685422657557),client.get_emoji(473988298860134400),client.get_emoji(473985986452520960),client.get_emoji(469644183523557387)]
            blobs.append(client.get_emoji(579159386648477717))
            blobs.append(client.get_emoji(579158599687995392))
            blobs.append(client.get_emoji(579158101647949835))
            bloblist=""
            for i in range(int(number)):
                blob=random.choice(blobs)
                bloblist=bloblist+str(blob)
            await message.channel.send(bloblist)

    if message.content.startswith('emoji'):
        emojis=message.guild.emojis
        print(emojis)
client.run(bottoken)