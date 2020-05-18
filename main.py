import discord
import random
from discord.ext import commands, tasks
import keep_alive
import gspread
import corona_api
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from itertools import cycle
import time
import datetime


start_time=time.time()



def get_prefix(bot,message):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
  try:
    hi=prefixes[str(message.guild.id)]
  except KeyError:
    return "+"
  return hi

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
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
  prefixes[str(guild.id)]="+"  
  with open('prefixes.json','w') as f:
    json.dump(prefixes,f,indent=4)
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
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
  prefixes.pop(str(guild.id))  
  with open('prefixes.json','w') as f:
    json.dump(prefixes,f,indent=4)
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
  if message.author.bot:
    return
  elif "<@!679529602028273740>" in message.content or "<@679529602028273740>" in message.content:
    with open('prefixes.json','r') as f:
      prefix=json.load(f)
      serverprefix=prefix[str(message.guild.id)]
    await message.channel.send(f"My prefix in {message.guild} is {serverprefix} Do {serverprefix}help for more info on my commands")
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
  if message.guild.id!=696453389625720873:
    await bot.process_commands(message)
    return
  with open('number.json','r') as f:
    num=json.load(f)
  try:
    trynum=int(message.content)
  except ValueError:
    await bot.process_commands(message)
    return

  if trynum==num["number"]:
    await message.channel.send(f"{message.author.mention}, You guessed the number I was thinking of! It was {trynum}!")
    num["number"]=random.randint(1,100)
  else:
    if trynum==num["previous"]:
      await message.channel.send(f"{trynum} is nor closer or further than {trynum} to the number I am thinking of")
    else:
      diff1=num["number"]-trynum
      diff2=num["number"]-num["previous"]
      if diff1<0:
        diff1=diff1/(-1)
      if diff2<0:
        diff2=diff2/(-1)
      if diff1<diff2:
        await message.channel.send(f"{trynum} is closer to my number than {num['previous']}")
      elif diff1==diff2:
        await message.channel.send(f"{trynum} and {num['previous']} are equally as close as each other to my number")
      else:
        await message.channel.send(f"{num['previous']} is closer to my number than {trynum}")

  num["previous"]=trynum
  with open('number.json','w') as f:
    json.dump(num,f,indent=4)

  await bot.process_commands(message)

bot.remove_command('help')




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
async def test(ctx):
  if ctx.channel.is_nsfw():
    await ctx.send("This channel is nsfw")
  else:
    await ctx.send("This channel is not NSFw")
@bot.command()
async def guild(ctx):
  for guild in bot.guilds:
    await ctx.send(guild.id)


@bot.command(aliases=["prefix","newprefix"])
@commands.has_permissions(administrator=True)
async def setprefix(ctx,newprefix):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
  prefixes[str(ctx.guild.id)]=newprefix
  with open('prefixes.json','w') as f:
    json.dump(prefixes,f,indent=4)
  await ctx.send(f'prefix is changed to {newprefix}')
@setprefix.error
async def setprefix_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send("You do not have permission to change my prefix! You need admin to do so.")
  elif isinstance(error,commands.MissingArgument):
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
