import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} was kicked by {ctx.author.mention}. [{reason}]')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} was banned by {ctx.author.mention}. [{reason}]')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} messages got deleted')
    
    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            print('here')
            await ctx.send("You need to specify an amount!")
        if isinstance(error,commands.BadArgument):
            await ctx.send("Give an integer!")
        raise error

def setup(bot):
    bot.add_cog(Mod(bot))