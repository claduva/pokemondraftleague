import discord
from discord.ext import commands

import asyncio
import asyncpg
import json,requests

class Draft(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.draft_check())

    async def draft_check(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            response=requests.get(f'http://127.0.0.1:8000/api/draftannouncement/')
            replay_records=response.json()
            for record in replay_records:
                #get server
                for item in self.bot.guilds:
                    if item.name==record['discordserver']:
                        for channel in item.channels:
                            if channel.name==record['discordchannel']:
                                if record['picknumber']==1:
                                    pick="1st"
                                elif record['picknumber']==2:
                                    pick="2nd"
                                elif record['picknumber']==3:
                                    pick="3rd"
                                else:
                                    pick=f"{record['picknumber']}th"
                                if record['upnext']!="The draft has concluded.":
                                    desc=f"{record['upnext']} is now on the clock. Please go to http://pokemondraftleague.online/leagues/{record['league'].replace(' ','_')}/{record['subleague'].replace(' ','_')}/draft/ to input your next pick."
                                else:
                                    desc=f"{record['upnext']} Please go to http://pokemondraftleague.online/leagues/{record['league'].replace(' ','_')}/{record['subleague'].replace(' ','_')}/draft/ to view the full draft."
                                embed=discord.Embed(
                                    title=f"With the {pick} pick of the draft, the {record['teamname']} have selected {record['pokemonname']}.",
                                    colour=discord.Colour.blue(),
                                    description=desc
                                    )
                                embed.set_thumbnail(url=record['logo'])
                                embed.set_image(url=record['pokemonsprite'])
                                embed.set_author(name=f"PDL",icon_url=self.bot.user.avatar_url)
                                await channel.send(embed=embed)
                                if record["upnextid"] and record["upnextid"]>99999999:
                                    await channel.send(f'<@{record["upnextid"]}>')
                                url = f'http://127.0.0.1:8000/api/draftannouncement/{record["id"]}/'
                                myobj = {'picknumber':record['picknumber'],'skipped':record['skipped'],'announced': True}
                                x = requests.put(url, data = myobj)
            await asyncio.sleep(30)

def setup(bot):
    bot.add_cog(Draft(bot))