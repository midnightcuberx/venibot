import discord,pymongo,dns,os
from discord.ext import commands


mongosecret=os.environ.get("mongosecret")
client = pymongo.MongoClient(mongosecret)
db = client["comp"]
collection=db["results"]


class Setup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def bansetup(self,ctx):
    for guild in self.bot.guilds:
      db=client["comp"]
      collection=db.bans
      collection.insert_one({"_id":guild.id,"bans":{}})
      await ctx.send("done")

  @commands.command()
  @commands.is_owner()
  async def recordsetup(self,ctx):
    for guild in self.bot.guilds:
      collection=db["records"]
      collection.insert_one({"_id":guild.id,"3x3":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"4x4":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"2x2":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"5x5":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"6x6":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"7x7":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"square-1":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"skewb":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"clock":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"pyraminx":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"oh":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"megaminx":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"3bld":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"4bld":{"single":"Nobody with a single of None","average":"Nobody with an average of None"},"5bld":{"single":"Nobody with a single of None","average":"Nobody with an average of None"}})

  @commands.command()
  @commands.is_owner()
  async def comps123(self,ctx):
    for guild in self.bot.guilds:
      collection.insert_one({"_id":guild.id,"3x3":{},"4x4":{},"2x2":{},"5x5":{},"6x6":{},"7x7":{},"square-1":{},"skewb":{},"clock":{},"pyraminx":{},"oh":{},"megaminx":{},"3bld":{},"4bld":{},"5bld":{}})
  
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def compsetup(self,ctx):
    try:
      collection.insert_one({"_id":ctx.guild.id,"3x3":{},"4x4":{},"2x2":{},"5x5":{},"6x6":{},"7x7":{},"square-1":{},"skewb":{},"clock":{},"pyraminx":{},"oh":{},"megaminx":{},"3bld":{},"4bld":{},"5bld":{}})
    except pymongo.errors.DuplicateKeyError:
      await ctx.send("The comp is already set up in your server!")
  
  @commands.command()
  @commands.is_owner()
  async def config123(self,ctx):
    for guild in self.bot.guilds:
      collection.insert_one({"_id":guild.id,"3x3":{"mode":"on"},"4x4":{"mode":"on"},"2x2":{"mode":"on"},"5x5":{"mode":"on"},"6x6":{"mode":"on"},"7x7":{"mode":"on"},"square-1":{"mode":"on"},"skewb":{"mode":"on"},"clock":{"mode":"on"},"pyraminx":{"mode":"on"},"oh":{"mode":"on"},"megaminx":{"mode":"on"},"3bld":{"mode":"on"},"4bld":{"mode":"on"},"5bld":{"mode":"on"}})


  @commands.command()
  async def resetrecord(self,ctx,event=None,sora=None):
    if not event:
      await ctx.send("You must enter a valid event!")
      return
    if not sora:
      await ctx.send("You must tell me if you want to reset a single or average!")
      return
    sora=sora.lower()
    event=event.lower()
    if event=="pyra":
      event="pyraminx"
    elif event=="skweeb":
      event="skewb"
    elif event=="sq1" or event.lower()=="squan":
      event="square-1"
    elif event=="mega":
      event="megaminx"
    elif event=="cloncc":
      event="clock"

    elif sora!="average" and sora!="single":
      await ctx.send("Please enter single or average!")
      return
    collection=db["records"]
    userlist={}
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      records=result
    try:
      eventresults=records[event]
    except KeyError:
      await ctx.send("Sorry that is not a valid event!")
      return
    for key in records[event]:
      userlist[key]=records[event][key]
    if sora=="single":
      userlist[sora]="Nobody with a single of None"
    else:
      userlist[sora]="Nobody with an average of None"
    collection.update_one({"_id":ctx.guild.id},{"$set":{event:userlist}})

    await ctx.send(f"Successfully reset {event} {sora} to None")
    


def setup(bot):
  bot.add_cog(Setup(bot))
