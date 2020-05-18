import discord
from discord.ext import commands
import math


class Maths(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.command()
  async def add(self,ctx, a: int, b: int):
      await ctx.send(a+b)

  @commands.command()
  async def multiply(self,ctx, a: int, b: int):
      await ctx.send(a*b)

  @commands.command()
  async def divide(self,ctx, a: int, b: int):
      await ctx.send(a/b)

  @commands.command()
  async def subtract(self,ctx, a: int, b: int):
      await ctx.send(a-b)

  @commands.command(aliases=["solvequadratic","quadsolver"])
  async def solvequad(self,ctx,a:int,b:int,c:int):
    try:
      diff=math.sqrt((b)**2-4*a*c)
    except ValueError:
      await ctx.send("Oops! That quadratic has no real roots!!")
    x1=((-b)+diff)/(2*a)
    x2=((-b)-diff)/(2*a)
    await ctx.send(f"The 2 answers to your quadratic are {x1} and {x2}")

  @commands.command()
  async def factorial(self,ctx,a:int):
    if a<806:
      await ctx.send(f"{a}! = {math.factorial(a)}")
    else:
      await ctx.send("I cannot factorial that number! It is too big!")

  @commands.command()
  async def pi(self,ctx):
    await ctx.send(math.pi)

  @commands.command(aliases=["gcd"])
  async def hcf(self,ctx,a:int,b:int):
    high=math.gcd(a,b)
    await ctx.send(high)

  @commands.command()
  async def degtorad(self,ctx,deg:int):
    rads=math.radians(deg)
    await ctx.send(f"{deg} degrees is {rads} radians!")

  @commands.command()
  async def radtodeg(self,ctx,rads:int):
    deg=math.degrees(rads)
    await ctx.send(f"{rads} radians is {deg} degrees!")
  
  @commands.command()
  async def pythag(self,ctx,a:int,b:int):
    side=math.sqrt((a**2+b**2))
    await ctx.send(f"The length of the hypotenuse is {side}")


def setup(bot):
  bot.add_cog(Maths(bot))
