import discord
from discord.ext import commands
import calendar
import asyncio

class Utility(commands.Cog):
  def __init__(self,bot):
    self.bot=bot





  @commands.command()
  async def userinfo(self,ctx,user:discord.Member=None):
    if not user:
      user=ctx.message.author
    embed = discord.Embed(title=f"User info for {user}",description="", color=0xeee657)
    embed.add_field(name='User ID', value=user.id, inline=False)
    embed.add_field(name='Nick', value=user.nick, inline=False)
    embed.add_field(name='Status', value=user.status, inline=False)
    embed.add_field(name='Game', value=user.activity, inline=False)
    embed.add_field(name='Roles', value=user.roles, inline=False)
    embed.add_field(name='Account Created', value=user.created_at,inline=False)
    embed.add_field(name='Join Date', value=user.joined_at,inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)
  """@userinfo.error
  async def userinfo_error(self,ctx,error):
    if isinstance(error,commands.BadArgument):
      await ctx.send("You did not specify a valid member!")"""


  @commands.command()
  async def avatar(self,ctx,member : discord.Member=None):
    if not member:
      member=ctx.message.author
    embed=discord.Embed(title=f"{member}'s avatar",description="", color=0xeee657)
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)



  @commands.command()
  async def info(self,ctx):
      embed = discord.Embed(title="veni scrambler bot", description="A veni nice bot :D", color=0xeee657)

      embed.add_field(name="Dev", value="Venimental#1289",inline = False)
      embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}",inline=False)
      embed.add_field(name="Invite", value="https://tinyurl.com/venibotinvite",inline=False)
      embed.add_field(name="Support Server",value="https://tinyurl.com/venisupport",inline=False)
      await ctx.send(embed=embed)

  @commands.command()
  async def oldsuggest(self,ctx,*,arg=None):
      if ctx.message.channel.name=="suggestions":
          if not arg:
            await ctx.send("Please enter a suggestion")
          else:
            await ctx.message.delete()
            embed = discord.Embed(title="Suggestion by {}".format(ctx.message.author), description="{}".format(arg), color=0xeee657)
          msg=await ctx.send(embed=embed)
          emoji1='👍'
          emoji2='👎'
          await msg.add_reaction(emoji1)
          await msg.add_reaction(emoji2)
      else:
          await ctx.send("You can only post suggestions in the suggestions channel!")

  @commands.command()
  async def kill(self,ctx,*,arg=None):
      if not arg:
        await ctx.send("Who are you trying to kill?")
      else:
        await ctx.send("{} killed {}! The cops are on your tail, you'd better run quick!".format(ctx.message.author.mention,arg))

  @commands.command()
  async def reminder(self,ctx,a:int=None,*,arg):
    if not a:
      await ctx.send("Please specify a time in seconds!")
    else:
      await ctx.send("You have set a reminder of {} for {} seconds!".format(arg,a))
      await asyncio.sleep(a)
      await ctx.send("{}, {}".format(arg,ctx.message.author.mention))

  @commands.command()
  async def timer(self,ctx,a:int=None):
    if not a:
      await ctx.send("Please enter a time in seconds")
    else:
      await ctx.send("You have set a timer for {} seconds".format(a))
      await asyncio.sleep(a)
      await ctx.send("{}, Your timer of {} seconds has now expired".format(ctx.message.author.mention,a))

  @commands.command()
  async def whatdayis(self,ctx,a:int=None,b:int=None,c:int=None):
    if not a or not b or not c:
      await ctx.send("Enter a real date in the format <date> <month> <year>!")
    cal=calendar.weekday(c,b,a)
    if cal==0:
      day="Monday"
    elif cal==1:
      day="Tuesday"
    elif cal==2:
      day="Wednesday"
    elif cal==3:
      day="Thursday"
    elif cal==4:
      day="Friday"
    elif cal==5:
      day="Saturday"
    elif cal==6:
      day="Sunday"
    await ctx.send("{}/{}/{} is a {}".format(a,b,c,day))



  @commands.command()
  async def ping(self,ctx):
      await ctx.send('Pong! {0}ms'.format(round(self.bot.latency*1000)))

  @commands.command()
  async def suggest(self,ctx,*,arg):
    guild=ctx.guild
    suggestion = discord.utils.get(ctx.guild.text_channels, name="suggestions")
    if not suggestion:
      await ctx.send("You can only post suggestions if there is a suggestions channel!")
    else:
      if not arg:
        await ctx.send("Please enter a suggestion")
      else:
        await ctx.message.delete()
        embed = discord.Embed(title="Suggestion by {}".format(ctx.message.author), description="{}".format(arg), color=0xeee657)
        msg=await suggestion.send(embed=embed)
        emoji1='👍'
        emoji2='👎'
        await msg.add_reaction(emoji1)
        await msg.add_reaction(emoji2)
  
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lock(self,ctx):
    channel=ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("Successfully locked this channel")

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unlock(self,ctx):
    channel=ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("successfuly unlocked this channel")
    
  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def suggestsetup(self,ctx):
    guild=ctx.guild
    suggestion = discord.utils.get(ctx.guild.text_channels, name="suggestions")
    if not suggestion:
      suggestion=await guild.create_text_channel('suggestions')
      await suggestion.set_permissions(ctx.guild.default_role, send_messages=False)
    else:
      await ctx.send("There is already a suggestion channel!")
  @suggestsetup.error
  async def suggestsetup_error(self,ctx,error):
    if isinstance(error,commands.MissingPermissions):
      await ctx.send("Smh, You don't have the manage channel permissions!")



def setup(bot):
  bot.add_cog(Utility(bot))
