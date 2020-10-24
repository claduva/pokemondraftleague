import discord
from discord.ext import commands

import asyncio
import asyncpg
import json, requests

class Matchreplays(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.replay_check())

    async def replay_check(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            response=requests.get(f'http://127.0.0.1:8000/api/schedule/')
            replay_records=response.json()
            for record in replay_records:
                #get server
                for item in self.bot.guilds:
                    if item.name=='claduva Test Server':
                        for channel in item.channels:
                            if channel.name=='replays':
                                try:
                                    embed=discord.Embed(
                                        title=f"Week {record['week']}: {record['team1name']} vs {record['team2name']}",
                                        #url=record['replay'],
                                        colour=discord.Colour.blue(),
                                        description=f"Replay: {record['replay']}\nWinner: ||{record['winnername']}||"
                                        )
                                except:
                                    try:
                                        embed=discord.Embed(
                                            title=f"Week {record['week']}: {record['team1name']} vs {record['team2name']}",
                                            colour=discord.Colour.blue(),
                                            description=f"Replay: {record['replay']}\nWinner: ||{record['winnername']}||"
                                            )
                                    except:
                                        embed=discord.Embed(
                                            title=f"Week {record['week']}: {record['team1name']} vs {record['team2name']}",
                                            colour=discord.Colour.blue(),
                                            description=f"Replay: {record['replay']}"
                                            )
                                embed.set_author(name=f"PDL",icon_url=self.bot.user.avatar_url)
                                await channel.send(embed=embed)
                                url = f'http://127.0.0.1:8000/api/schedule/{record["id"]}/'
                                myobj = {'week':record['week'],'replay':record['replay'],'announced': True}
                                x = requests.put(url, data = myobj)
                                print(x.content)
            await asyncio.sleep(30)

def setup(bot):
    bot.add_cog(Matchreplays(bot))
