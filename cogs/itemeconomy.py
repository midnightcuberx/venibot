import discord
from discord.ext import commands
import json
import random


class Itemeconomy(commands.Cog):
  def __init__(self,bot):
    self.bot=bot


  @commands.command()
  async def shop(self,ctx):
    embed=discord.Embed(title="Shop",description="A place where you can buy things",color=0xeee657)
    embed.add_field(name="Laptop-$1500",value="You can post memes with this laptop.")
    embed.add_field(name="Rod-$200",value="You can fish with this!")
    embed.add_field(name="Lifesaver-$15000",value="You may die from hunting so why not have one of these handy?")
    embed.add_field(name="Gun-$5000",value="You can hunt with this. But beware as there is a chance you will be shot by someone else!")
    await ctx.send(embed=embed)
  
  @commands.command()
  async def buy(self, ctx, item=None, amount=1):
    with open('economy.json','r') as f:
      eco=json.load(f)

    item = item.lower()
    if not item:
      await ctx.send("Please enter a valid item!")
    elif eco[str(ctx.author.id)]['wallet'] >= (eco['shop'][item]*amount):
      eco[str(ctx.author.id)]['wallet'] -= (eco['shop'][item]*amount)
      eco[str(ctx.author.id)][item] += amount

      with open("economy.json", "w") as f:
        json.dump(eco, f, indent=4)
      await ctx.send(f'You successfully bought {amount} {item}(s)!')
    else:
      await ctx.send("You Do Not Have Enough Money.")
  
  @commands.command(aliases=["inventory"])
  async def inv(self,ctx):
    with open('economy.json','r') as a:
      eco=json.load(a)
    userid=str(ctx.author.id)
    
    embed=discord.Embed(title=f"{ctx.message.author}'s inventory",description=f"Fishing rods:{eco[userid]['rod']}\nLaptops:{eco[userid]['laptop']}\nGuns:{eco[userid]['gun']}\nLifesavers:{eco[userid]['lifesaver']}",color=0xeee657)
    await ctx.send(embed=embed)


  @commands.command()
  @commands.cooldown(1,3600,commands.BucketType.user)
  async def hunt(self,ctx):
    with open('economy.json','r') as a:
      economy=json.load(a)
    user_bal=economy[str(ctx.message.author.id)]["wallet"]
    user_guns=economy[str(ctx.message.author.id)]["gun"]
    user_life=economy[str(ctx.author.id)]["lifesaver"]

    if user_guns<1:
      await ctx.send("You cannot hunt without a gun! use the buy command to buy yourself a gun first")
      self.hunt.reset_cooldown(ctx)
      return
    success=random.randint(1,10)
    if success==4:
      if user_life<1:
        await ctx.send("You were shot while hunting and you didnt have a lifesaver so you died!")
        economy[str(ctx.message.author.id)]["wallet"]=0
      else:
        user_life-=1
        economy[ctx.author.id]["lifesaver"]=user_life
        await ctx.send("You were shot by a fellow hunter but you had a lifesaver and survived after being taken to hospital")
    else:
      money=random.randint(1000,5000)
      user_bal+=money
      await ctx.send(f"You went hunting and caught ${money} worth of game!")
      economy[str(ctx.message.author.id)]["wallet"]=user_bal
    with open('economy.json','w') as a:
      json.dump(economy,a,indent=4)
  
  @hunt.error
  async def hunt_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("{} Woah there, slow down, please try again in {:.2f} minutes!".format(ctx.message.author.mention,error.retry_after/60))


  @commands.command(aliases=["postmeme"])
  @commands.cooldown(1,600,commands.BucketType.user)
  async def pm(self,ctx):
    userid=str(ctx.message.author.id)
    with open('economy.json','r') as a:
      economy=json.load(a)
    if economy[userid]["laptop"]<1:
      await ctx.send("You cannot post memes withut a laptop! Go buy one at the shop")
      self.pm.reset_cooldown(ctx)
      return
    memes=["edgy","funky","dank","repost","cubing","corona"]
    money=random.randint(10,250)
    economy[userid]["wallet"]+=money
    await ctx.send(f"You posted a {random.choice(memes)} meme and earned ${money}!")
    with open('economy.json','w') as a:
      json.dump(economy,a,indent=4)

  @pm.error
  async def pm_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("Woah there, slow down. Try again in {:.2f} minutes".format(error.retry_after/60))


  @commands.command()
  @commands.cooldown(1,120,commands.BucketType.user)
  async def fish(self,ctx):
    userid=str(ctx.message.author.id)
    with open('economy.json','r') as a:
      economy=json.load(a)
    if economy[userid]["rod"]<1:
      await ctx.send("You cannot fish without a fishing rod! Go buy one at the shop")
      self.fish.reset_cooldown(ctx)
      return
    fish=["snapper","kingfish","pufferfish","shrimp","catfish","salmon","prawn","tuna"]
    money=random.randint(50,100)
    economy[userid]["wallet"]+=money
    fishes=random.randint(1,5)
    await ctx.send(f"You caught {fishes} {random.choice(fish)} and earned ${money}!")
    with open('economy.json','w') as a:
      json.dump(economy,a,indent=4)

  @fish.error
  async def fish_error(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("Woah there, slow down. Try again in {:.2f}s".format(error.retry_after))
  



def setup(bot):
    bot.add_cog(Itemeconomy(bot))
