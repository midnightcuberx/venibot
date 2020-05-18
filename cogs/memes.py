import discord
from discord.ext import commands
import praw
import random
import os


redid=os.environ.get("redditid")
redsecret=os.environ.get("redditsecret")
reddit = praw.Reddit(client_id=redid, client_secret= redsecret,
user_agent='ok')
class Memes(commands.Cog):
  def __init__(self,bot):
    self.bot=bot
  


  @commands.command()
  async def joke(self,ctx):
      memes_submissions = reddit.subreddit('jokes').hot()
      post_to_pick = random.randint(1, 100)
      for i in range(0, post_to_pick):
          submission = next(x for x in memes_submissions if not x.stickied)
      embed=discord.Embed(title=submission.title,description=submission.selftext, color=0xeee657)
      await ctx.send(embed=embed)

  @commands.command()
  async def meme(self,ctx):
      memes_submissions = reddit.subreddit('memes').hot()
      post_to_pick = random.randint(1, 100)
      for i in range(0, post_to_pick):
          submission = next(x for x in memes_submissions if not x.stickied)
      embed=discord.Embed(title="from r/memes: {}".format(submission.title),description="", color=0xeee657)
      embed.set_image(url=submission.url)
      await ctx.send(embed=embed)

  @commands.command()
  async def dankmeme(self,ctx):
      memes_submissions = reddit.subreddit('dankmemes').hot()
      post_to_pick = random.randint(1, 100)
      for i in range(0, post_to_pick):
          submission = next(x for x in memes_submissions if not x.stickied)
      embed=discord.Embed(title="from r/dankmemes: {}".format(submission.title),description="", color=0xeee657)
      embed.set_image(url=submission.url)
      await ctx.send(embed=embed)

  @commands.command()
  async def shrekmeme(self,ctx):
      memes_submissions = reddit.subreddit('Shrekmemes').hot()
      post_to_pick = random.randint(1, 100)
      for i in range(0, post_to_pick):
          submission = next(x for x in memes_submissions if not x.stickied)
      embed=discord.Embed(title="from r/Shrekmemes: {}".format(submission.title),description="", color=0xeee657)
      embed.set_image(url=submission.url)
      await ctx.send(embed=embed)

  @commands.command()
  async def cubingmeme(self,ctx):
      memes_submissions = reddit.subreddit('cubingmemes').hot()
      post_to_pick = random.randint(1, 100)
      for i in range(0, post_to_pick):
          submission = next(x for x in memes_submissions if not x.stickied)
      embed=discord.Embed(title="from r/cubingmemes: {}".format(submission.title),description="", color=0xeee657)
      embed.set_image(url=submission.url)
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Memes(bot))
