import discord
from discord.ext import commands

import asyncio
import asyncpg
import psycopg2
from psycopg2 import pool
import datetime
import os
import random
from itertools import cycle

bot=commands.Bot(command_prefix="!")
try:
    from bottoken import *
    TOKEN=BOTTOKEN
    NAME=NAME
    USER=USER
    PASSWORD=PASSWORD
    HOST=HOST
except:
    TOKEN=os.environ.get('BOTTOKEN')
    NAME=os.environ.get('NAME')
    USER=os.environ.get('USER')
    PASSWORD=os.environ.get('PASSWORD')
    HOST=os.environ.get('HOST')

async def create_db_pool():
    try:
        bot.pg_con = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                user = USER,
                                                password = PASSWORD,
                                                host = HOST,
                                                port = "5432",
                                                database = NAME)
        #if(bot.pg_con):
        #    print("Connection pool created successfully")
    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while connecting to PostgreSQL", error)


@bot.command(aliases=["site"])
async def website(ctx):
    '''Sends site's website'''
    embed=discord.Embed(title="Pokemon Draft League Online",description="Site for Pokemon Draft Leagues", colour=discord.Colour.red(),url="http://pokemondraftleague.online/")
    embed.set_author(name=bot.user.name,icon_url=bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name,icon_url=ctx.author.avatar_url)
    embed.set_image(url=bot.user.avatar_url)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def reload(ctx,cog):
    try:
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} got reloaded!")
    except Exception as e:
        print(f"{cog} could not be loaded!")
        raise e

async def chnge_pr():
    await bot.wait_until_ready()
    statuslist=["!help","http://pokemondraftleague.online/"]
    statuslist=cycle(statuslist)
    while not bot.is_closed():
        status=next(statuslist)
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(5)

for cog in os.listdir("discordbot/cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog=f"cogs.{cog.replace('.py','')}"
            bot.load_extension(cog)
            print(f"{cog} was loaded!")
        except Exception as e:
            print(f"{cog} could not be loaded!")
            raise e

bot.loop.run_until_complete(create_db_pool())
bot.loop.create_task(chnge_pr())
bot.run(TOKEN)