import discord
from discord.ext import commands

import asyncio
import asyncpg
import datetime
import os
import random

client=commands.Bot(command_prefix="!")
try:
    from bottoken import *
    TOKEN=BOTTOKEN
except:
    TOKEN=os.environ.get('BOTTOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    return
    
@client.command()
async def website(ctx):
    await ctx.send("http://pokemondraftleague.online/")

client.run(TOKEN)