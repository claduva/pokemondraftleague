import discord
from discord.ext import commands

import asyncio
import asyncpg
import json

class Matchreplays(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.loop.create_task(self.draft_check())

    async def draft_check(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            # Use getconn() to Get Connection from connection pool
            ps_connection  = self.bot.pg_con.getconn()
            if(ps_connection):
                #print("successfully recived connection from connection pool ")
                ps_cursor = ps_connection.cursor()
                ps_cursor.execute("select * from individualleague_replay_announcements")
                replay_records = ps_cursor.fetchall()
                for record in replay_records:
                    #get server
                    for item in self.bot.guilds:
                        if item.name==record[1]:
                            for channel in item.channels:
                                if channel.name==record[4]:
                                    try:
                                        embed=discord.Embed(title=record[3],url=f"{record[3].split(': ')[2].split('.')[0]}",colour=discord.Colour.blue())
                                    except:
                                        embed=discord.Embed(title=record[3],colour=discord.Colour.blue())
                                    embed.set_author(name=f"PDL",icon_url=self.bot.user.avatar_url)
                                    await channel.send(embed=embed)
                                    ps_cursor.execute("DELETE from individualleague_replay_announcements WHERE id = %s",(record[0],))
                                    ps_connection.commit()
                ps_cursor.close()
                #Use this method to release the connection object and send back to connection pool
                self.bot.pg_con.putconn(ps_connection)
                #print("Put away a PostgreSQL connection")
            await asyncio.sleep(30)

def setup(bot):
    bot.add_cog(Matchreplays(bot))

"""
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
            """