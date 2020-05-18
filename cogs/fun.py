import discord
from discord.ext import commands
import random
import asyncio
import time
import json


class Fun(commands.Cog):
  def __init__(self,bot):
    self.bot=bot
  @commands.command()
  async def say(self,ctx, *, arg):
    if "@everyone" in arg or "@here" in arg:
      await ctx.send("Stop trying to ping everyone!")
    else:
      await ctx.message.delete()
      await ctx.send(arg)
  @say.error
  async def say_error(self,ctx,error):
    if isinstance(error,commands.BotMissingPermissions):
      await ctx.send("I do not have permission to delete messages!")
  
  @commands.command()
  async def quickdraw(self,ctx):
    await ctx.send("When I say !DRAW send !DRAW")
    start_time=time.time()
    sleep=random.randint(5,10)
    await asyncio.sleep(sleep)
    await ctx.send(f"{ctx.author.mention}, !DRAW")
    message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
    while message.content!="!DRAW":
      message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
    #ctx.channel.id != whatever force only retrive emessages from there
    end_time=time.time()
    reaction=end_time-start_time-sleep
    reaction1=round(reaction*1000)
    await ctx.send(f"{ctx.author.mention}, Your reaction time was {reaction1}ms")
    with open('reactiontime.json','r') as f:
      react=json.load(f)
    try:
      userindb=react[str(ctx.author.id)]
    except ValueError:
      react[str(ctx.author.id)]=reaction1
    if react[str(ctx.author.id)]>reaction1:
      react[str(ctx.author.id)]=reaction1
    
    with open('reactiontime.json','w') as f:
      json.dump(react,f,indent=4)
    
  @commands.command()
  async def quicklb(self,ctx):
    with open('reactiontime.json','r') as f:
      economy=json.load(f)
    lblist=[]
    for key, value in sorted(economy.items(),reverse=False, key=lambda item: item[1]):
      string="<@%s> : %s" % (key,value)
      lblist.append(string)
    embed = discord.Embed(title="Top 5 fastest users!", description=f"🥇{lblist[0]}ms\n🥈{lblist[1]}ms\n🥉{lblist[2]}ms\n4️⃣{lblist[3]}ms\n5️⃣{lblist[4]}ms",color=0xeee657)
    await ctx.send(embed=embed)
    



  @commands.command()
  async def guess(self,ctx,a:int=None):
    number=random.randint(1,1000)
    guesses=0
    if not a:
      await ctx.send("You must tell me what number between 1 and 1000 you are trying to guess!")
    elif a>1000 or a<1:
      await ctx.send("The number must be between 1 and 1000 inclusive!")
    else:
      while number!=a:
        guesses-=1
        if 10-guesses<1:
          await ctx.send(f"You ran out of guesses! My number was {number}")
          return
        if a>1000 or a<1:
          await ctx.send("The number must be between 1 and 1000 inclusive!")
        elif a>number:
          await ctx.send(f"Your number was too high You have {10-guesses} guesses left")
        else:
          await ctx.send(f"Your number was too low. You have {10-guesses} guesses left")
        a = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        try:
          a=int(a.content)
        except ValueError:
          await ctx.send("You did not enter a vaid number!")
      if a==number:
        await ctx.send("Your guess is correct!")

  @commands.command()
  async def rps(self,ctx,a):
    rps=["rock","paper","scissors"]
    item=random.choice(rps)
    if item.lower()==a:
      await ctx.send("Tie! You and your opponent both played {}!".format(item))
    elif item=="rock" and a=="scissors":
      await ctx.send("Your opponent played rock and you played scissors. Rock smashes scisors you lose. GG")
    elif item.lower()=="rock" and a=="paper":
      await ctx.send("Your opponent played rock and you played paper. Paper wraps rock. You win. GG")
    elif item.lower()=="scissors" and a=="paper":
      await ctx.send("Your opponent played scissors and you played paper. SCISSORS CUT PAPER You lose. GG")

    elif item.lower()=="scissors" and a=="rock":
      await ctx.send("Your opponent played scissors and you played rock. Rock smashes scissors so you win GG.")

    elif item.lower()=="paper" and a=="rock":
      await ctx.send("Your opponent played paper and you played rock. Paper beats rock so you lose. GG.")

    elif item.lower()=="paper" and a=="scissors":
      await ctx.send("Your opponent played paper and you played scissors. Scissors beat paper so you win. GG")

  @commands.command()
  async def cf(self,ctx,a=None):
    choices=["heads","tails"]
    ranchoice=random.choice(choices)
    if not a:
      await ctx.send("The coin flips.... and it lands on {}!".format(ranchoice))
    elif a != "heads" and a != "tails":
      await ctx.send("Smh you didn't enter heads or tails. Did you invent your own type of coin or something?")
    else:
      if a==ranchoice:
        await ctx.send("The coin flips.... and it lands on {}. Congratulations! Have a free pie.".format(ranchoice))
      else:
        await ctx.send("The coin flips.... and it lands on {}. No free pie for you. Better luck next time!".format(ranchoice))
    

  @commands.command(aliases=["8ball"])
  async def _8ball(self,ctx,a=None):
    if not a:
      await ctx.send("Please ask me something?")
    else:
      answers=["Yes","No","Maybe","Definately","Perhaps","Definately not","Yes, I think so","I think not","Never","Certainly","Certainly not"]
      await ctx.send(random.choice(answers))

  @commands.command()
  async def rate(self,ctx,*,arg=None):
      a=random.randint(0,10)
      if not arg:
          arg="You"
          embed = discord.Embed(title="Rate Machine", description="You are a {} out of 10".format(a), color=0xeee657)
      else:
        embed = discord.Embed(title="Rate Machine", description="{} is a {} out of 10".format(arg,a), color=0xeee657)
      await ctx.send(embed=embed)

  @commands.command()
  async def howgay(self,ctx,*,arg=None):
      a=random.randint(0,100)
      if not arg:
          arg="You"
          embed = discord.Embed(title="Gay Rate Machine", description="You are {}% gay".format(a), color=0xeee657)
      else:
        embed = discord.Embed(title="Gay Rate Machine", description="{} is {}% gay".format(arg,a), color=0xeee657)
      await ctx.send(embed=embed)

  @commands.command()
  async def foxometer(self,ctx,*,arg=None):
      a=random.randint(0,100)
      if not arg:
          arg="You"
          embed = discord.Embed(title="Fox-O-Meter", description="You are {}% a fox".format(a), color=0xeee657)
      else:
        embed = discord.Embed(title="Fox-O-Meter", description="{} is {}% a fox".format(arg,a), color=0xeee657)
      await ctx.send(embed=embed)

  @commands.command()
  async def love(self,ctx,a,b):
    c=random.randint(0,100)
    embed = discord.Embed(title="Love Calculator", description="Love between {} and {} is at {}%".format(a,b,c), color=0xFFC0CB)
    await ctx.send(embed=embed)

  @commands.command()
  async def pedo(self,ctx,*,arg=None):
      a=random.randint(0,100)
      if not arg:
          arg="You"
          embed = discord.Embed(title="Pedo Rate Machine", description="You are {}% pedo".format(a), color=0xeee657)
      else:
        embed = discord.Embed(title="Rate Machine", description="{} is {}% pedo".format(arg,a), color=0xeee657)
      await ctx.send(embed=embed)


  @commands.command(aliases=["bscan"])
  async def boomerscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for boomers...")
      await asyncio.sleep(2)
      await msg.edit(content="I found a boomer! They are {}".format(random.choice(guild.members)))

  @commands.command(aliases=["zscan"])
  async def zoomerscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for zoomers...")
      await asyncio.sleep(2)
      await msg.edit(content="I found a zoomer! They are {}".format(random.choice(guild.members)))

  @commands.command()
  async def ncscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for Non cubers...")
      await asyncio.sleep(2)
      await msg.edit(content="I found a Non Cuber! They are {}".format(random.choice(guild.members)))

  @commands.command()
  async def cuberscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for cubers...")
      await asyncio.sleep(2)
      await msg.edit(content="I found a cuber! They are {}".format(random.choice(guild.members)))

  @commands.command()
  async def noobscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for noobs...")
      await asyncio.sleep(2)
      await msg.edit(content="I found a noob! They are {}".format(random.choice(guild.members)))

  @commands.command(aliases=["spscan","smallppscan"])
  async def smollppscan(self,ctx):
      guild=ctx.guild
      msg=await ctx.send("Scanning the server for people with a smoll pp...")
      await asyncio.sleep(2)
      await msg.edit(content="I found someone with a smoll pp! They are {}".format(random.choice(guild.members)))

  @commands.command(aliases=["rick"])
  async def rickroll(self,ctx):
      await ctx.message.delete()
      await ctx.send("https://bit.ly/3eiDmyi")

  @commands.command()
  async def encrypt(self,ctx,shift:int=None,*,msg=None):
    if not msg:
      await ctx.send("You have to enter a message for me to encrypt!")
    if not shift:
      await ctx.send("You have to enter a valid integer to shift!")
    if not msg or not shift:
      return
    if shift > 25 or shift < -25:
      await ctx.send("Smh you can only encrypt messages by 25 and -25 at most!")
      return
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    msg=msg.upper()
    encrypted_str=[]
    for cur_letter in msg:
      position=alphabet.find(cur_letter)
      newpos=position+shift
      if cur_letter in alphabet:
        encrypted_str.append(alphabet[newpos])
      else:
        encrypted_str.append(cur_letter)

    await ctx.send("".join(encrypted_str))
  @encrypt.error
  async def encrypt_error(self,ctx,error):
    if isinstance(error,commands.BadArgument):
      await ctx.send("smh you have to enter a valid integer to shift!")

  @commands.command()
  async def hack(self,ctx,member:discord.Member=None):
    if not member:
      await ctx.send("You have to specify a member to hack!")
      return

    letters=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"]
    letters1=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    a=[]
    c=[]
    numbers=["0","1","2","3","4","5","6","7","8","9"]
    b=random.randint(8,16)
    d=random.randint(4,10)
    e=random.randint(1,5)
    for i in range(b):
      a.append(random.choice(letters))
    for i in range(d):
      c.append(random.choice(letters1))
    for i in range(e):
      c.append(random.choice(numbers))
    f="".join(a)
    g="".join(c)
    emails=["gmail.com","programmer.net","hotmail.com","outlook.com","protonmail.com","hackermail.com","yahoo.com.tw","mail.com"]
    msg=await ctx.send("Hacking {}'s computer...".format(member))
    await asyncio.sleep(1)
    await msg.edit(content="Retrieving {}'s credidentials and important files...".format(member))
    await asyncio.sleep(1)
    await msg.edit(content="Overriding {}'s computer".format(member))
    await asyncio.sleep(1)
    await msg.edit(content="Hack complete.")
    await ctx.send("{}'s email: {}@{} \n{}'s password: {}".format(member,g,random.choice(emails),member,f))
  @hack.error
  async def hack_error(self,ctx,error):
   if isinstance(error,commands.BadArgument):
      await ctx.send("You didn't enter a valid user!")

def setup(bot):
  bot.add_cog(Fun(bot))
