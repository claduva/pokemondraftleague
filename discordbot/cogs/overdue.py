import discord
from discord.ext import commands

import asyncio
import asyncpg
import json, requests

class Overdue(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.overdue_check())

    async def overdue_check(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            response=requests.get(f'https://pokemondraftleague.online/api/overdue/')
            #response=requests.get(f'http://127.0.0.1:8000/api/overdue/')
            records=response.json()
            for record in records:
                #get server
                for item in self.bot.guilds:
                    if item.name==record['discordserver']:#'claduva Test Server':
                        for channel in item.channels:
                            if channel.name==record['discordchannel']:#'announcements':
                                embed=discord.Embed(
                                    title=f"Week {record['week']}: {record['team1name']} vs {record['team2name']} is overdue and is subject to forfeits. Please discuss with your league admins to get this match updated as soon as possible.",
                                    #url=record['replay'],
                                    colour=discord.Colour.blue(),
                                    #description=f"|"
                                    )
                                if record["coach1id"]==None or  int(record["coach1id"])<999999999999:
                                    embed.add_field(name="Coach 1", value= f'{record["coach1"]}', inline=True)
                                else:
                                    embed.add_field(name="Coach 1", value= f'<@{record["coach1id"]}>', inline=True)
                                if record["coach2id"]==None or  int(record["coach2id"])<999999999999:
                                    embed.add_field(name="Coach 2", value= f'{record["coach2"]}', inline=True)
                                else:
                                    embed.add_field(name="Coach 2", value= f'<@{record["coach2id"]}>', inline=True)
                                embed.set_author(name=f"PDL",icon_url=self.bot.user.avatar_url)
                                await channel.send(embed=embed)
            await asyncio.sleep(60*60*24)

def setup(bot):
    bot.add_cog(Overdue(bot))
