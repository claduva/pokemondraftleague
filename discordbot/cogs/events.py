import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author==self.bot.user:
            return
        user=message.author.name
        msg=message.content
        #print(f'{user} said {msg}')
        #if msg.lower().replace("-","").replace(" ","").replace(".","").find("lombre")>-1 or msg.lower().replace("-","").replace(" ","").replace(".","").find("mbre")>-1:
        #    await message.delete()
        #    await message.channel.send("For the love of Arceus shut up about Lombre!")

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You don't have permission to do that!")
        if isinstance(error,commands.CommandNotFound):
            await ctx.send("That is not a command!")
        raise error

def setup(bot):
    bot.add_cog(Events(bot))