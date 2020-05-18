import discord
from discord.ext import commands
import random
import json

class Im(commands.Cog):
  def __init__(self,bot):
    self.bot=bot  
  
  
  
  @commands.Cog.listener()
  async def on_message(self,message):
    send=[]
    if message.author.bot:
      return
    elif message.content.lower().startswith("im") or message.content.lower().startswith("i'm"):
      with open('dadtoggle.json','r') as f:
        dad=json.load(f)
      guildid=dad[str(message.guild.id)]
      if guildid=="off":
        return
      x=message.content.split()
      for i in range(1,len(x)):
        send.append(x[i])
      string=" ".join(send)
      await message.channel.send(f"Hi {string}, I'm Dad")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def dadtoggle(self,ctx,onoff=None):
    with open('dadtoggle.json','r') as a:
      dad=json.load(a)
    guildid=dad[str(ctx.guild.id)]
    if not onoff:
      if guildid=="on":
        guildid="off"
      else:
        guildid="on"
      await ctx.send(f"Successfully toggled I'm dad to {guildid}")
      dad[str(ctx.guild.id)]=guildid
      with open('dadtoggle.json','w') as a:
        json.dump(dad,a,indent=4)
      return
    elif onoff.lower() != "on" and onoff.lower() != "off":
      await ctx.send("You must tell me to toggle it on or off!")
      return
    onoff=onoff.lower()
    guildid=onoff
    await ctx.send(f"Successfully toggled I'm Dad to {guildid}")
    dad[str(ctx.guild.id)]=guildid
    with open('dadtoggle.json','w') as a:
      json.dump(dad,a,indent=4)
  @dadtoggle.error
  async def dadtoggle_error(self,ctx,error):
    if isinstance(error,commands.MissingPermissions):
      await ctx.send("You can only use this command if you have the manage messages permission!")

def setup(bot):
  bot.add_cog(Im(bot))
