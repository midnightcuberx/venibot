import discord
import json
from discord.ext import commands, tasks
import asyncio
import random

class Economy(commands.Cog):
  def __init__(self,bot):
    self.bot=bot
  

  @commands.command(aliases=["stonks","stocks"])
  @commands.cooldown(1,43200,commands.BucketType.user)
  async def invest(self,ctx,money:int=None):
    if not money:
      await ctx.send("Please enter a valid amount to invest!")
      self.invest.reset_cooldown(ctx)
      return
    elif money>5000:
      money=5000
      await ctx.send("You cannot invest more than 5k! But since I am nice I will let you invest 5k")
    success=random.randint(1,3)
    with open('economy.json','r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    if money>user_bal:
      await ctx.send("You cannot invest more than you have! But since I am nice, I'll let you invest all your money")
      money=user_bal
    elif money<0:
      await ctx.send("You cannot invest negative money!")
      self.invest.reset_cooldown(ctx)
      return
    if success==1:
      await ctx.send(f"You invested money in the stock market but your investment didn't do well so you lost ${money}!")
      user_bal-=money
    else:
      chance=random.randint(1,15)
      if chance==3:
        multiplier=random.randint(3,5)
      else:
        multiplier=random.randint(1,2)
      money=money*multiplier
      user_bal+=money
      await ctx.send(f"Your investment paid off! You earned ${money}!")
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    
  @invest.error
  async def invest_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))
    

  @commands.command(aliases=["dep"])
  @commands.cooldown(1,10,commands.BucketType.user)
  async def deposit(self,ctx,money):
    with open("economy.json",'r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_bank=economy[str(ctx.message.author.id)]["bank"]
    max_bank=economy[str(ctx.message.author.id)]["maxbank"]
    try:
      money=int(money)
    except ValueError:
      if money=="all" or money=="All":
        if user_bal>=max_bank-user_bank:
          money=max_bank-user_bank
        else:
          money=user_bal
      else:
        await ctx.send("You did not send a valid amount to deposit!")
        return
        
    if money<=0:
      await ctx.send("You cannot deposit $0 negative money!")
      return
    elif money>user_bal:
      await ctx.send("You cannot deposit more than you own!")
      return
    elif money+user_bank>max_bank:
      await ctx.send("You cannot deposit more than you can fit in your bank!")
      return
    else:
      user_bal-=money
      user_bank+=money
      economy[str(ctx.message.author.id)]["wallet"]=user_bal
      economy[str(ctx.message.author.id)]["bank"]=user_bank
      await ctx.send(f"Successfully deposited ${money}!")
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    
    

  @commands.command(aliases=["with"])
  async def withdraw(self,ctx,money):
    with open("economy.json",'r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_bank=economy[str(ctx.message.author.id)]["bank"]
    try:
      money=int(money)
    except ValueError:
      if money=="all" or money=="All":
        money=user_bank
      else:
        await ctx.send("You did not send a valid amount to deposit!")
        return
    if money<0:
      await ctx.send("You cannot withdraw negative money!")
      return
    elif money>user_bank:
      await ctx.send("You cannot withdraw more than what is in your bank!")
    else:
      user_bal+=money
      user_bank-=money
      economy[str(ctx.message.author.id)]["wallet"]=user_bal
      economy[str(ctx.message.author.id)]["bank"]=user_bank
      await ctx.send(f"Successfully withdrew ${money}")
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)

    



  @commands.command(aliases=["steal"])
  @commands.cooldown(1,300,commands.BucketType.user)
  async def rob(self,ctx,member:discord.User=None):
    with open('economy.json','r') as f:
      economy=json.load(f)

    if not member:
      await ctx.send("Please enter a valid member to rob")
      self.rob.reset_cooldown(ctx)
    userid=str(ctx.author.id)
    memberid=str(member.id)
    if member.id==ctx.author.id:
      await ctx.send("You cannot rob yourself, silly")
      self.rob.reset_cooldown(ctx)
      return
    user_bal=economy[userid]["wallet"]
    try:
      member_bal=economy[memberid]["wallet"]
    except KeyError:
      member_bal=0
      self.rob.reset_cooldown(ctx)
    if user_bal >= 500:
      number=random.randint(1,5)
      try:
        userindb=economy[memberid]
      except KeyError:
        member_bal=0
        self.rob.reset_cooldown(ctx)
      if member_bal<500:
        await ctx.send("That user has less than 500 coins, you cannot rob them")
        self.rob.reset_cooldown(ctx)
        return
      elif member_bal>=500:
        if number==1:
          if member_bal<=5000:
            percentage=random.randint(1,75)
          elif member_bal>5000 and member_bal<=10000:
            percentage=random.randint(1,50)
          elif member_bal>10000 and member_bal<=100000:
            percentage=random.randint(1,25)
          elif member_bal>100000:
            percentage=random.randint(1,10)
          max_amount=round(member_bal*percentage/100)
          stolen_amount=random.randint(1,max_amount)
          user_bal+=stolen_amount
          member_bal-=stolen_amount
          await ctx.send(f"💸 | You stole ${stolen_amount} off {member}!")
        else:
          user_bal-=500
          member_bal+=500
          await ctx.send(f"You got caught trying to rob {member} so you paid them $500 to be quiet!")
      economy[userid]["wallet"]=user_bal
      economy[memberid]["wallet"]=member_bal
    
    else:
      await ctx.send("You cannot rob anyone if you dont have 500 coins")
      self.rob.reset_cooldown(ctx)
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
  @rob.error
  async def rob_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, you need time to plan your next roberry so please try again in {:.2f}m!".format(ctx.message.author.mention,error.retry_after/60))
    elif isinstance(error,commands.BadArgument):
      await ctx.send("You need to state a valid user to Rob!")
    elif isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("You need to state a valid user to Rob!")

  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def work(self,ctx):
    with open('economy.json','r') as f:
      economy=json.load(f)

    money=random.randint(1,500)

    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_bal+=money
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    jobs=["nurse","doctor","banker","salesperson","lawyer","zookeeper","movie star","actor","programmer","teacher","musician","truck driver","conductor","bus driver","taxi driver","model","judge","umpire","referee","professional rugby player","professional football player"]
    await ctx.send(f"You worked as a {random.choice(jobs)} and earned ${money}")
  @work.error
  async def work_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}m You can only work every hour!".format(ctx.message.author.mention,error.retry_after/60))

  @commands.command()
  @commands.cooldown(1,10,commands.BucketType.user)
  async def beg(self,ctx):
    money=random.randint(1,20)
    with open('economy.json','r') as f:
      economy=json.load(f)

    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_bal+=money
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send(f"Some took pity on you when they saw you begging and gave you ${money}")

  @beg.error
  async def beg_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}s!".format(ctx.message.author.mention,error.retry_after))

  @commands.command(aliases=["scout"])
  @commands.cooldown(1,30,commands.BucketType.user)
  async def search(self,ctx):
    places=["the dump","a rubbish bin","a trash can", "your parent's dressing room","the school playground","the bus stop","the backseat of a taxi","a dumpster","the dump","your parent's wallet","the coffee shop"]
    number=random.randint(1,20)
    if number==1:
      money=random.randint(125,250)
    elif number>15:
      money=random.randint(50,125)
    else:
      money=random.randint(1,75)

    with open('economy.json','r') as f:
      economy=json.load(f)

    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_bal+=money
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send(f"You scouted {random.choice(places)} and found ${money}!")


  @search.error
  async def search_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}s!".format(ctx.message.author.mention,error.retry_after))


  @commands.command()
  async def bal(self,ctx,user:discord.User=None):
    with open('economy.json','r') as f:
      eco=json.load(f)
    if not user:
      user_bal=eco[str(ctx.author.id)]["wallet"]
      user_bank=eco[str(ctx.author.id)]["bank"]
      max_bank=eco[str(ctx.author.id)]["maxbank"]
      embed=discord.Embed(title=f"{ctx.message.author}'s Balance",description=f"Wallet: ${user_bal}\nBank: {user_bank}/{max_bank}",color=0x000fff)
    else:
      user_bal=eco[str(user.id)]["wallet"]
      user_bank=eco[str(user.id)]["bank"]
      max_bank=eco[str(user.id)]["maxbank"]
      embed=discord.Embed(title=f"{user}'s Balance",description=f"Wallet: ${user_bal}\nBank: {user_bank}/{max_bank}",color=0x000fff)
    await ctx.send(embed=embed)

  @commands.command()
  @commands.cooldown(1,600,commands.BucketType.user)
  async def busk(self,ctx):
    luck=random.randint(1,60)
    if luck >30:
      if luck==50:
        money=random.randint(100,300)
      else:
        money=random.randint(50,100)
    else:
      money=random.randint(1,50)
    with open('economy.json','r') as f:
      eco=json.load(f)
    user_bal=eco[str(ctx.author.id)]["wallet"]
    user_bal+=money
    eco[str(ctx.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(eco,f,indent=4)
    duration=random.randint(1,60)
    money_per_min=money/duration
    instruments=["🎺","🎻","🎸","🎷","🥁","📯","🎹"]
    await ctx.send("{} | {}, You busked for {} minutes and earned ${}! That equates to ${:.2f} per minute!".format(random.choice(instruments),ctx.message.author.mention,duration,money,money_per_min))

  @busk.error
  async def busk_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f} minutes you can only busk once every 10 minutes!".format(ctx.message.author.mention,error.retry_after/60))
    

  @commands.command(aliases=["leaderboard"])
  async def lb(self,ctx):
    with open('economy.json','r') as f:
      economy=json.load(f)
    lblist={}
    users=[]
    lb_list=[]
    for key in economy:
      users.append(key)
    for item in users:
      print(item)
      lblist[item]=economy[item]['wallet']
      
    

    for key, value in sorted(lblist.items(),reverse=True, key=lambda item: item[1]):
      string="<@%s> : %s" % (key,value)
      lb_list.append(string)
    embed = discord.Embed(title="💰Top 5 richest users💰", description=f"🥇{lb_list[0]}\n🥈{lb_list[1]}\n🥉{lb_list[2]}\n4️⃣{lb_list[3]}\n5️⃣{lb_list[4]}",color=0xeee657)
    await ctx.send(embed=embed)
    

  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def hourly(self,ctx):
    with open('economy.json','r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.author.id)]["wallet"]
    user_bal+=100
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send("100 hourly coins collected")
  @hourly.error
  async def hourly_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}m!".format(ctx.message.author.mention,error.retry_after/60))
  
  @commands.command()
  @commands.is_owner()
  async def addbal(self,ctx,member:discord.Member,money:int):
    memberid=str(member.id)
    with open('economy.json','r') as f:
      economy=json.load(f)
    try:
      userindb=economy[memberid]
    except KeyError:
      await ctx.send("This user is not in the database")
    user_bal=int(economy[memberid]["wallet"])
    user_bal+=money
    economy[memberid]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send(f"Successfully added ${money} to {member}'s balance")


  @commands.command()
  @commands.is_owner()
  async def resetuser(self,ctx,member:discord.Member):
    memberid=str(member.id)
    with open('economy.json','r') as f:
      economy=json.load(f)
    try:
      userindb=economy[memberid]
    except KeyError:
      del economy[memberid]
    del economy[memberid]
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send(f"Successfully reset {member}'s balance")  

  @commands.command(aliases=["transfer"])
  async def give(self,ctx,member:discord.User,money:int):
    if money<0:
      await ctx.send("You cannot give someone negative money")
      return
    userid=str(ctx.message.author.id)
    memberid=str(member.id)

    with open("economy.json",'r') as f:
      economy=json.load(f)
    try:
      userindb=economy[str(member.id)]["wallet"]
    except KeyError:
      economy[str(member.id)]={}
      economy[str(member.id)]["wallet"]=0
      economy[str(member.id)]["bank"]=0
      economy[str(member.id)]["maxbank"]=0
      economy[str(member.id)]={}
      economy[str(member.id)]["rods"]=0
      economy[str(member.id)]["laptops"]=0
      economy[str(member.id)]["lifesavers"]=0
      economy[str(member.id)]["guns"]=0
      economy[str(member.id)]["item"]=0
      economy[str(member.id)]["item1"]=0
      economy[str(member.id)]["item2"]=0
      economy[str(member.id)]["item3"]=0
      economy[str(member.id)]["item4"]=0
      economy[str(member.id)]["item5"]=0
      economy[str(member.id)]["item6"]=0
      economy[str(member.id)]["item7"]=0

    member_bal=economy[memberid]["wallet"]
    user_bal=economy[ctx.author.id]["wallet"]
    member_bal+=money
    user_bal-=money
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    economy[memberid]["wallet"]=member_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send(f"Successfully transfered ${money} to {member}")

  @commands.command()
  @commands.cooldown(1,86400,commands.BucketType.user)
  async def daily(self,ctx):
    with open('economy.json','r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.author.id)]["wallet"]
    user_bal+=1000
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send("Daily 1000 coins collected")
  @daily.error
  async def daily_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))
  
  @commands.command()
  @commands.cooldown(1,604800,commands.BucketType.user)
  async def weekly(self,ctx):
    with open('economy.json','r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.author.id)]['wallet']
    user_bal+=5000
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)
    await ctx.send("Weekly 5000 coins collected")

  @weekly.error
  async def weekly_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))

  @commands.command()
  async def gamble(self,ctx,money:int=None):
    success=random.randint(1,3)
    if not money:
      self.gamble.reset_cooldown(ctx)
      await ctx.send("Please specify an amount to gamble!")
    with open('economy.json','r') as f:
      economy=json.load(f)
    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    if user_bal< money:
      await ctx.send("You cannot gamble more than you have!")
      self.gamble.reset_cooldown(ctx)
      return
    if money<0:
      await ctx.send("You cannot gamble negative money")
      self.gamble.reset_cooldown(ctx)
      return
    msg=await ctx.send("🎰 | Spinning......")
    if success==1:
      user_bal+=money
      await asyncio.sleep(2)
      await msg.edit(content=f"The slot machine spins and you win ${money}!")
    else:
      user_bal-=money
      await asyncio.sleep(2)
      await msg.edit(content=f"the slot machine spins and you lose ${money}!")
    economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as f:
      json.dump(economy,f,indent=4)



def setup(bot):
  bot.add_cog(Economy(bot))
