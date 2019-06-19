import discord
from discord.ext import commands

import asyncio
import asyncpg
import datetime
import os
import random
from itertools import cycle

bot=commands.Bot(command_prefix="!")
try:
    from bottoken import *
    TOKEN=BOTTOKEN
except:
    TOKEN=os.environ.get('BOTTOKEN')

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

#bot.loop.run_until_complete(create_db_pool())
bot.loop.create_task(chnge_pr())
bot.run(TOKEN)