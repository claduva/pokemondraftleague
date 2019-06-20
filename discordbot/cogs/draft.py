import discord
from discord.ext import commands

import asyncio
import asyncpg
import json

class Draft(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.draft_check())

    async def draft_check(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open('discordbot/cogs/draft.json','r') as f:
                self.draft= json.load(f)
            print(self.draft)
            for i, item in enumerate(self.draft):
                if self.draft[i]['announced']=='No':
                    league=item['league']
                    text=item['text']
                    print(text)
                    leagueserver=None
                    botservers=self.bot.guilds
                    for item in botservers:
                        if item.name == league:
                            leagueserver=item
                    leaguechannels=leagueserver.channels
                    draftchannel=None
                    for item in leaguechannels:
                        if item.name=='draft':
                            draftchannel=item
                    self.draft[i]['announced']='Yes'
                    embed=discord.Embed(description=f"{text}\n__________ is now on the clock. Please go to __________ to input your next pick.",colour=discord.Colour.blue())
                    embed.set_author(name=f"PDL",icon_url=self.bot.user.avatar_url)
                    await draftchannel.send(embed=embed)  
            with open('discordbot/cogs/draft.json','w') as f:
                json.dump(self.draft,f,indent=4)
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(Draft(bot))