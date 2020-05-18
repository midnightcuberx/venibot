import discord
from discord.ext import commands

class Uptime(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.command()
  async def send(self,ctx,*,arg):
    target = discord.utils.get(ctx.guild.members, id=646597016205656064)
    await ctx.send("Your message has successfully been sent to my owner by dm")
    await target.send(f"From {ctx.message.author} : {arg}")

  @commands.command()
  async def suggestbot(self,ctx,*,arg):
    target = discord.utils.get(ctx.guild.members, id=646597016205656064)
    await target.send(f"Suggestion by {ctx.message.author} : {arg}")
    await ctx.send("Your suggestion has been recieved!")


def setup(bot):
    bot.add_cog(Uptime(bot))
