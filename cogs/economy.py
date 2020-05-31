import discord,pymongo,dns,json,os,random,asyncio
from discord.ext import commands
#By2【你並不懂我 You Don't Know Me】官方完整版 

mongosecret=os.environ.get("mongosecret2")
client = pymongo.MongoClient(mongosecret)
db = client["economy"]
collection=db["economy"]

class Ecotest(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=["postmeme"])
  @commands.cooldown(1,600,commands.BucketType.user)
  async def pm(self,ctx):
    userid=ctx.message.author.id
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]
    if economy["laptop"]<1:
      await ctx.send("You cannot post memes withut a laptop! Go buy one at the shop")
      self.pm.reset_cooldown(ctx)
      return
    memes=["edgy","funky","dank","repost","cubing","corona"]
    money=random.randint(10,250)
    user_bal+=money
    userlist={}
    for key in economy:
      if key != "_id":
        userlist[key]=economy[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    await ctx.send(f"You posted a {random.choice(memes)} meme and earned ${money}!")

  @pm.error
  async def pm_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("Woah there, slow down. Try again in {:.2f} minutes".format(error.retry_after/60))

  @commands.command()
  @commands.cooldown(1,120,commands.BucketType.user)
  async def fish(self,ctx):

    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]
    if economy["rod"]<1:
      await ctx.send("You cannot fish without a fishing rod! Go buy one at the shop")
      self.fish.reset_cooldown(ctx)
      return
    fish=["snapper","kingfish","pufferfish","shrimp","catfish","salmon","prawn","tuna"]
    money=random.randint(50,100)
    user_bal+=money
    fishes=random.randint(1,5)
    userlist={}
    for key in economy:
      if key != "_id":
        userlist[key]=economy[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    await ctx.send(f"You caught {fishes} {random.choice(fish)} and earned ${money}!")


  @fish.error
  async def fish_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("Woah there, slow down. Try again in {:.2f}s".format(error.retry_after))

  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def hunt(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]
    user_guns=economy["gun"]
    user_life=economy["lifesaver"]

    if user_guns<1:
      await ctx.send("You cannot hunt without a gun! use the buy command to buy yourself a gun first")
      self.hunt.reset_cooldown(ctx)
      return
    success=random.randint(1,10)
    if success==4:
      if user_life<1:
        await ctx.send("You were shot while hunting and you didnt have a lifesaver so you died!")
        user_bal=0
        userlist={}
        for key in economy:
          if key != "_id":
            userlist[key]=economy[key]
        
        userlist["wallet"]=user_bal
      else:
        user_life-=1
        userlist={}
        for key in economy:
          if key != "_id":
            userlist[key]=economy[key]
        
        userlist["lifesaver"]=user_life
        await ctx.send("You were shot by a fellow hunter but you had a lifesaver and survived after being taken to hospital")
    else:
      money=random.randint(500,2000)
      user_bal+=money
      await ctx.send(f"You went hunting and caught ${money} worth of game!")
      userlist={}
      for key in economy:
        if key != "_id":
          userlist[key]=economy[key]
      
      userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})

  
  @hunt.error
  async def hunt_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f} minutes!".format(ctx.message.author.mention,error.retry_after/60))

  @commands.command()
  async def buy(self,ctx,item=None,amount=1):
    item=item.lower()
    shopitems=["laptop","rod","instrument","gun","lifesaver"]
    itemvalue={"laptop":1500,"rod":200,"instrument":500,"gun":2000,"lifesaver":5000}
    if not item:
      await ctx.send("Please enter a valid item!")
    if item not in shopitems:
      await ctx.send("That is not a valid item! use +shop to check what items are on sale")
      return
    
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    item_amount=eco[item]

    if user_bal >= itemvalue[item]*amount:
      user_bal -= itemvalue[item]*amount
      item_amount+=amount
      await ctx.send(f'You successfully bought {amount} {item}(s)!')
      userlist={}
      for key in eco:
        if key != "_id":
          userlist[key]=eco[key]
      
      userlist["wallet"]=user_bal
      userlist[item]=item_amount
      collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    else:
      await ctx.send("Sorry, You Do Not Have Enough Money.")
  
  @commands.command(aliases=["inventory"])
  async def inv(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    gun=eco["gun"]
    rod=eco["rod"]
    instrument=eco["instrument"]
    laptop=eco["laptop"]
    lifesaver=eco["lifesaver"]
    embed=discord.Embed(title=f"{ctx.author}'s inventory",description=f"Guns: {gun}\nRods: {rod}\nInstruments: {instrument}\nLaptops: {laptop}\nLifesavers: {lifesaver}",color=0xffff00)
    await ctx.send(embed=embed)
    

  @commands.command(aliases=["leaderboard"])
  async def lb(self,ctx):
    lblist={}
    users=[]
    lb_list=[]
    users=[]
    results=collection.find()
    for result in results:
      users.append(result["_id"])
    for item in users:
      results=collection.find({"_id":item})
      for result in results:
        eco=result
      lblist[item]=eco["wallet"]
    length=len(lblist)
    if length>5:
      length=5
    for i in range(5-length):
      list1=["Nobody","None","No-one","Noone","No person"]
      test=random.choice(list1)
      list1.remove(test)
      lblist[test]=1
    for key, value in sorted(lblist.items(),reverse=True, key=lambda item: item[1]):
      string=f"<@!{key}> : {value}"
      lb_list.append(string)
    embed = discord.Embed(title="💰Top 5 richest users💰", description=f"🥇{lb_list[0]}\n🥈{lb_list[1]}\n🥉{lb_list[2]}\n4️⃣{lb_list[3]}\n5️⃣{lb_list[4]}",color=0xeee657)
    await ctx.send(embed=embed)

  @commands.command(aliases=["steal"])
  @commands.cooldown(1,300,commands.BucketType.user)
  async def rob(self,ctx,member:discord.User=None):
    memberid=member.id
    userid=ctx.author.id
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]

    if not member:
      await ctx.send("Please enter a valid member to rob")
      self.rob.reset_cooldown(ctx)

    if member.id==ctx.author.id:
      await ctx.send("You cannot rob yourself, silly")
      self.rob.reset_cooldown(ctx)
      return
    try:
      collection.insert_one({"_id":member.id,"wallet":0,"bank":0,"maxbank":0,"gun":0,"rod":0,"laptop":0,"lifesaver":0})
    except pymongo.errors.DuplicateKeyError:
      pass
    results=collection.find({"_id":member.id})
    for result in results:
      eco=result
    member_bal=eco["wallet"]
    if user_bal >= 500:
      number=random.randint(1,5)
      if member_bal<500:
        await ctx.send("That user has less than 500 coins, you cannot rob them")
        self.testrob.reset_cooldown(ctx)
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
      userlist={}
      for key in economy:
        if key != "_id":
          userlist[key]=economy[key]
      
      userlist["wallet"]=user_bal
      collection.update_one({"_id":ctx.author.id},{"$set":userlist})
      userlist1={}
      for key in eco:
        if key != "_id":
          userlist1[key]=eco[key]
      
      userlist1["wallet"]=member_bal
      collection.update_one({"_id":member.id},{"$set":userlist1})
    
    else:
      await ctx.send("You cannot rob anyone if you dont have 500 coins")
      self.rob.reset_cooldown(ctx)

  @rob.error
  async def rob_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, you need time to plan your next roberry so please try again in {:.2f}m!".format(ctx.message.author.mention,error.retry_after/60))
    elif isinstance(error,commands.BadArgument):
      await ctx.send("You need to state a valid user to Rob!")
    elif isinstance(error,commands.MissingRequiredArgument):
      await ctx.send("You need to state a valid user to Rob!")


  @commands.command(aliases=["transfer"])
  async def give(self,ctx,member:discord.User,money:int):
    if money<=0:
      await ctx.send("You cannot give someone $0 or negative money!")
      return
    userid=ctx.message.author.id
    memberid=member.id


    try:
      collection.insert_one({"_id":member.id,"wallet":0,"bank":0,"maxbank":0,"gun":0,"rod":0,"laptop":0,"lifesaver":0})
    except pymongo.errors.DuplicateKeyError:
      pass
    


    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]

    results=collection.find({"_id":member.id})
    for result in results:
      eco=result
    member_bal=eco["wallet"]

    member_bal+=money
    user_bal-=money

    userlist={}
    for key in economy:
      if key != "_id":
        userlist[key]=economy[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    userlist1={}
    for key in eco:
      if key != "_id":
        userlist1[key]=eco[key]
    
    userlist1["wallet"]=user_bal
    collection.update_one({"_id":member.id},{"$set":userlist1})

    await ctx.send(f"Successfully transfered ${money} to {member}")



  @commands.command(aliases=["slots"])
  async def gamble(self,ctx,money:int=None):
    success=random.randint(1,4)
    if not money:
      self.gamble.reset_cooldown(ctx)
      await ctx.send("Please specify an amount to gamble!")

    results=collection.find({"_id":ctx.author.id})
    for result in results:
      economy=result
    user_bal=economy["wallet"]

    if user_bal< money:
      await ctx.send("You cannot gamble more than you have!")
      return
    if money<=0:
      await ctx.send("You cannot gamble $0 or negative money!")
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
    userlist={}
    for key in economy:
      if key != "_id":
        userlist[key]=economy[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    userlist1={}


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

    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    user_bal+=money

    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})

    duration=random.randint(1,60)
    money_per_min=money/duration
    instruments=["🎺","🎻","🎸","🎷","🥁","📯","🎹"]
    await ctx.send("{} | {}, You busked for {} minutes and earned ${}! That equates to ${:.2f} per minute!".format(random.choice(instruments),ctx.message.author.name,duration,money,money_per_min))
  @busk.error
  async def busk_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}m!".format(ctx.message.author.mention,error.retry_after/60))

  @commands.command(aliases=["stonks","stocks"])
  @commands.cooldown(1,43200,commands.BucketType.user)
  async def invest(self,ctx,money:int=None):
    if not money:
      await ctx.send("Please enter a valid amount to invest!")
      self.invest.reset_cooldown(ctx)
      return
    elif money>1000:
      money=1000
      await ctx.send("You cannot invest more than 1000! But since I am nice I will let you invest 1000")
    success=random.randint(1,3)

    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    if money>user_bal:
      await ctx.send("You cannot invest more than you have! But since I am nice, I'll let you invest all your money")
      money=user_bal
    elif money<=0:
      await ctx.send("You cannot invest negative or 0 money!")
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
    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})

  @invest.error
  async def invest_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))

  @commands.command(aliases=["dep"])
  async def deposit(self,ctx,money):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    user_bank=eco["bank"]
    max_bank=eco["maxbank"]
    try:
      money=int(money)
    except ValueError:
      if money.lower()=="all":
        if user_bal>=max_bank-user_bank:
          money=max_bank-user_bank
        else:
          money=user_bal
      else:
        await ctx.send("You did not send a valid amount to deposit!")
        return
        
    if money<=0:
      await ctx.send("You cannot deposit $0 or negative money!")
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
      userlist={}
      for key in eco:
        if key != "_id":
          userlist[key]=eco[key]
      
      userlist["wallet"]=user_bal
      userlist["bank"]=user_bank
      collection.update_one({"_id":ctx.author.id},{"$set":userlist})
      await ctx.send(f"Successfully deposited ${money}!")


  @commands.command(aliases=["with"])
  async def withdraw(self,ctx,money):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    user_bank=eco["bank"]

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
      userlist={}
      for key in eco:
        if key != "_id":
          userlist[key]=eco[key]
      
      userlist["wallet"]=user_bal
      userlist["bank"]=user_bank
      collection.update_one({"_id":ctx.author.id},{"$set":userlist})
      await ctx.send(f"Successfully withdrew ${money}")

  @commands.command()
  @commands.cooldown(1,10,commands.BucketType.user)
  async def beg(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    money=random.randint(1,20)
    user_bal+=money
    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    await ctx.send(f"You begged and earned ${money}")

  @beg.error
  async def beg_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}s!".format(ctx.message.author.mention,error.retry_after))
  
  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def work(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result

    money=random.randint(1,250)

    user_bal=eco["wallet"]+money

    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})

    jobs=["nurse","doctor","banker","salesperson","lawyer","zookeeper","movie star","actor","programmer","teacher","musician","truck driver","conductor","bus driver","taxi driver","model","judge","umpire","referee","professional rugby player","professional football player"]
    await ctx.send(f"You worked as a {random.choice(jobs)} and earned ${money}")

  @work.error
  async def work_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))
  



  @commands.command()
  async def bal(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    user_bank=eco["bank"]
    user_max=eco["maxbank"]
    embed=discord.Embed(title=f"{ctx.author}'s balance",description=f"Wallet: ${user_bal}\nBank: {user_bank}/{user_max}",color=0xffff00)
    await ctx.send(embed=embed)
  
  @commands.command(aliases=["scout"])
  @commands.cooldown(1,60,commands.BucketType.user)
  async def search(self,ctx):
    places=["the dump","a rubbish bin","a trash can", "your parent's dressing room","the school playground","the bus stop","the backseat of a taxi","a dumpster","the dump","your parent's wallet","the coffee shop"]
    number=random.randint(1,20)
    if number==1:
      money=random.randint(125,250)
    elif number>15:
      money=random.randint(50,125)
    else:
      money=random.randint(1,75)

    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result

    user_bal=eco["wallet"]+money

    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})

    await ctx.send(f"You scouted {random.choice(places)} and found ${money}!")

  @search.error
  async def search_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}s!".format(ctx.message.author.mention,error.retry_after))

  @commands.command()
  @commands.cooldown(1,43200,commands.BucketType.user)
  async def daily(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    money=1000
    user_bal+=money
    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    await ctx.send("You successfully collected your 1000 daily coins!")

  @daily.error
  async def daily_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}h!".format(ctx.message.author.mention,error.retry_after/3600))

  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def hourly(self,ctx):
    results=collection.find({"_id":ctx.author.id})
    for result in results:
      eco=result
    user_bal=eco["wallet"]
    money=100
    user_bal+=money
    userlist={}
    for key in eco:
      if key != "_id":
        userlist[key]=eco[key]
    
    userlist["wallet"]=user_bal
    collection.update_one({"_id":ctx.author.id},{"$set":userlist})
    await ctx.send("You successfully collected your 100 hourly coins!")
  @hourly.error
  async def hourly_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f}m!".format(ctx.message.author.mention,error.retry_after/60))
  
  
#discord.ext.commands.errors.CommandInvokeError: Command raised an exception: InvalidDocument: cannot encode object: <Member id=646597016205656064 name='Venimental' discriminator='1289' bot=False nick=None guild=<Guild id=696453389625720873 name='Veni Bot & pycubescrambler python module support' shard_id=None chunked=True member_count=20>>, of type: <class 'discord.member.Member'>

    

    





def setup(bot):
  bot.add_cog(Ecotest(bot))
