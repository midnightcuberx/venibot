import discord,random,keep_alive,gspread,corona_api,json,os,time,datetime,pymongo,dns
from discord.ext import commands, tasks
from itertools import cycle


start_time=time.time()

mongosecret=os.environ.get("mongosecret")
client = pymongo.MongoClient(mongosecret)
db = client["bot"]

def get_prefix(bot,message):
  collection=db["prefix"]
  try:
    collection.insert_one({"_id":message.guild.id,"prefix":"+"})
    return "+"
  except pymongo.errors.DuplicateKeyError:
    collection=db["prefix"]
    results=collection.find({"_id":message.guild.id})
    for result in results:
      prefix=result
    return prefix["prefix"]

bot = commands.Bot(command_prefix= get_prefix)
status=cycle(["with Rubiks cubes","+help","ping me for help","with 11DTP","with corona","with myself","with my gf"])
bot.corona = corona_api.Client()

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))


@bot.event
async def on_ready():
    change_status.start()
    #activity = discord.Game(name="with Rubiks cubes | +help", type=3)
    #await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready')
    print('------')


@bot.event
async def on_guild_join(guild):
  collection=db["prefix"]
  collection.insert_one({"_id":guild.id,"prefix":"+"})
  db=client["comp"]
  collection=db["results"]
  collection.insert_one({"_id":guild.id,"3x3":{},"4x4":{},"2x2":{},"5x5":{},"6x6":{},"7x7":{},"square-1":{},"skewb":{},"clock":{},"pyraminx":{},"oh":{},"megaminx":{},"3bld":{},"4bld":{},"5bld":{}})
  db=client["comp"]
  collection=db["config"]
  collection.insert_one({"_id":guild.id,"3x3":{"mode":"on"},"4x4":{"mode":"on"},"2x2":{"mode":"on"},"5x5":{"mode":"on"},"6x6":{"mode":"on"},"7x7":{"mode":"on"},"square-1":{"mode":"on"},"skewb":{"mode":"on"},"clock":{"mode":"on"},"pyraminx":{"mode":"on"},"oh":{"mode":"on"},"megaminx":{"mode":"on"},"3bld":{"mode":"on"},"4bld":{"mode":"on"},"5bld":{"mode":"on"}})
  db=client["comp"]
  collection=db.bans
  collection.insert_one({"_id":guild.id,"bans":{}})
  with open('dadtoggle.json','r') as a:
    dad=json.load(a)
  dad[str(guild.id)]="off"
  with open('dadtoggle.json','w') as a:
    json.dump(dad,a,indent=4)
  with open('invitetoggle.json','r') as a:
    invite=json.load(a)
  invite[str(guild.id)]="off"
  with open('invitetoggle.json','w') as a:
    json.dump(invite,a,indent=4)

@bot.event
async def on_bot_remove(guild):
  collection=db["prefix"]
  collection.delete_one({"_id":guild.id})
  db=client["comp"]
  collection=db["results"]
  collection.delete_one({"_id":guild.id})
  db=client["comp"]
  collection=db["config"]
  collection.delete_one({"_id":guild.id})
  db=client["comp"]
  collection=db.bans
  collection.delete_one({"_id":guild.id})
  with open('dadtoggle.json','r') as a:
    dad=json.load(a)
  dad.pop(str(guild.id))
  with open('dadtoggle.json','w') as a:
    json.dump(dad,a,indent=4)
  with open('invitetoggle.json','r') as a:
    invite=json.load(a)
  invite.pop(str(guild.id))
  with open('invitetoggle.json','w') as a:
    json.dump(invite,a,indent=4)
  
@bot.event
async def on_message(message):
  collection=db["prefix"]
  if message.author.bot:
    return
  elif "<@!679529602028273740>" in message.content or "<@679529602028273740>" in message.content:
    try:
      collection.insert_one({"_id":message.guild.id,"prefix":"+"})
      prefix= "+"
    except pymongo.errors.DuplicateKeyError:
      collection=db["prefix"]
      results=collection.find({"_id":message.guild.id})
      for result in results:
        prefix=result["prefix"]
    await message.channel.send(f"My prefix in {message.guild} is {prefix} Do {prefix}help for more info on my commands")
  elif message.content.startswith(get_prefix(bot,message)):
    with open('economy.json','r') as b:
      economy=json.load(b)
    try:
      userindb=economy[str(message.author.id)]
    except KeyError:
      economy[str(message.author.id)]={}
      economy[str(message.author.id)]["wallet"]=0
      economy[str(message.author.id)]["bank"]=0
      economy[str(message.author.id)]["maxbank"]=0
      economy[str(message.author.id)]["rods"]=0
      economy[str(message.author.id)]["laptops"]=0
      economy[str(message.author.id)]["lifesavers"]=0
      economy[str(message.author.id)]["guns"]=0
      economy[str(message.author.id)]["item"]=0
      economy[str(message.author.id)]["item1"]=0
      economy[str(message.author.id)]["item2"]=0
      economy[str(message.author.id)]["item3"]=0
      economy[str(message.author.id)]["item4"]=0
      economy[str(message.author.id)]["item5"]=0
      economy[str(message.author.id)]["item6"]=0
      economy[str(message.author.id)]["item7"]=0
    economy[str(message.author.id)]["maxbank"]+=random.randint(40,60)
    with open('economy.json','w') as b:
      json.dump(economy,b,indent=4)

  await bot.process_commands(message)

bot.remove_command('help')


@bot.command()
@commands.is_owner()
async def prefixes(ctx):
  for guild in bot.guilds:
    collection=db["prefix"]
    collection.insert_one({"_id":guild.id,"prefix":"+"})
  await ctx.send("DOne")


@bot.command()
async def coronacases(ctx, *, country):
    msg = await bot.corona.get_country_data(country)
    await ctx.send('cases: {0.cases}, deaths: {0.deaths}'.format(msg))
@bot.command()
@commands.is_owner()
async def load(ctx,extension):
  bot.load_extension(f"cogs.{extension}")

@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
  bot.unload_extension(f"cogs.{extension}")


@bot.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    await ctx.send(f"The bot has been up for {text}")

@bot.command()
@commands.is_owner()
async def reload(ctx,*,file=None):
  if not file:
    for filename in os.listdir('./cogs'):
      if filename.endswith(".py"):
        bot.unload_extension(f"cogs.{filename[:-3]}")
        bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send(f"Successfully reloaded {filename}!")
    return
  bot.unload_extension(f"cogs.{file[:-3]}")
  bot.load_extension(f"cogs.{file[:-3]}")
  await ctx.send(f"Successfully reloaded {file}!")


for filename in os.listdir('./cogs'):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
async def guild(ctx):
  for guild in bot.guilds:
    await ctx.send(guild.id)


@bot.command(aliases=["prefix","newprefix"])
@commands.has_permissions(administrator=True)
async def setprefix(ctx,newprefix):
  collection=db["prefix"]
  try:
    collection.insert_one({"_id":ctx.guild.id,"prefix":newprefix})
  except pymongo.errors.DuplicateKeyError:
    collection.update_one({"_id":ctx.guild.id},{"$set":{"prefix":newprefix}})
  await ctx.send(f'prefix is changed to {newprefix}')
@setprefix.error
async def setprefix_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send("You do not have permission to change my prefix! You need admin to do so.")
  elif isinstance(error,commands.MissingRequiredArgument):
    await ctx.send("You did not specify what to change the prefix to!")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down")
    await ctx.bot.logout()

@shutdown.error
async def shutdown_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send("Sorry, Only my owner, Venimental#1289 can use this command")

keep_alive.keep_alive()


token=os.environ.get("botsecret")
bot.run(token)
