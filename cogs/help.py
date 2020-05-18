import discord
from discord.ext import commands



class Help(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.command()
  async def help(self,ctx,a=None):
    if not a:
      embed = discord.Embed(title="Veni Scrambler Bot", description="do +help <category> to get more info on that category", color=0xeee657)

      embed.add_field(name="__**Utility**__", value="info, reminder, timer, whatdayis, suggest, suggestbot, send, avatar, userinfo", inline=False)
      embed.add_field(name="__**Cubing**__", value="s, zbll, memescram, avg, bigcube", inline=False)
      embed.add_field(name="__**Fun**__", value="say, rps, rate, howgay, pedo, love, 8ball, guess, cf, kill, ping, boomerscan or bscan, zoomerscan or zscan, ncscan, cuberscan, noobscan, meme, joke, hack, encrypt,dadtoggle,quickdraw, quicklb", inline=False)
      embed.add_field(name="__**Moderation**__", value="kick, ban, purge, mute, unmute, invitetoggle", inline=False)
      embed.add_field(name="__**Economy**__", value="bal, work, daily, weekly, search, beg, give, lb, rob, gamble, busk, shop, inv, buy, hunt, fish, pm", inline=False)
      embed.add_field(name="__**Maths**__", value="pythag, pi, solvequad, hcf, add, subtract, multiply, divide, degtorad, radtodeg, factorial", inline=False)
      embed.add_field(name="__**COVID-19**__", value="corona, coronatop, cvhistory", inline=False)
      await ctx.author.send(embed=embed)

    elif a.lower()=="utility":
      embed = discord.Embed(title="__**Utility commands**__", description="helpful commands", color=0xeee657)
      embed.add_field(name="+info", value="Gives this message", inline=False)
      embed.add_field(name="+whatdayis <day> <month> <year>", value="Tells you what weekday a date is", inline=False)
      embed.add_field(name="+timer <seconds>", value="sets a timer for however many seconds", inline=False)
      embed.add_field(name="+reminder <time> <reminder notice> ", value="sets a reminder for later", inline=False)
      embed.add_field(name="+suggest <suggestion>", value="sends a suggestion for the server", inline=False)
      embed.add_field(name="+suggestbot <suggestion>", value="sends a suggestion for the bot to the owner of the bot", inline=False)
      embed.add_field(name="+send <message>", value="sends a message to my owner", inline=False)
      embed.add_field(name="+avatar ", value="shows your avatar", inline=False)
      embed.add_field(name="+userinfo <user> ", value="shows the info on a user", inline=False)
      await ctx.author.send(embed=embed)

    elif a.lower()=="cubing":
      embed = discord.Embed(title="__**Cubing commands**__", description="stuff about rubiks cubes", color=0xeee657)
      embed.add_field(name="+s <event> <num>", value="Generates <num> of <event> scrambles (Hopefully you get a wr :D)",inline=False)
      embed.add_field(name="Events:", value="1x1, 2x2, 3x3, 4x4, 5x5, 6x6, 7x7, OH, skewb,megaminx, pyraminx",inline=False)
      embed.add_field(name="zbll", value="Generates Juliette Sebastian's zbll sheet in the working",inline=False)
      embed.add_field(name="+memescram", value="Generates a very easy meme 3x3 scramble",inline=False)
      embed.add_field(name="+<event> <num>", value="Generates <num> of <event> wca legal scrambles (Only works if im hosting on pc)",inline=False)
      embed.add_field(name="+cubingmeme", value="generates a meme from r/cubingmemes", inline=False)
      embed.add_field(name="+avg <time1> <time2> <time3> <time4> <time5>", value="calculates your average", inline=False)
      embed.add_field(name="+bigcube <size> <number of scrambles>", value="generates a big cube scramble max 27x27 ish because of discord character limits", inline=False)
      await ctx.author.send(embed=embed)

    elif a.lower()=="fun":
      embed = discord.Embed(title="__**Fun commands**__", description="fun stuff", color=0xeee657)
      embed.add_field(name="+ping", value="Shows the ping", inline=False)
      embed.add_field(name="+say", value="repeats what is said", inline=False)    
      embed.add_field(name="+rps <choice>", value="Feel free to play rock paper scissors against the bot", inline=False)
      embed.add_field(name="+rate", value="gives you a rating out of 10", inline=False)
      embed.add_field(name="+howgay", value="tells you how gay you are", inline=False)
      embed.add_field(name="+pedo", value="tells you how pedo you are", inline=False)
      embed.add_field(name="+foxometer", value="Try your luck! ARe you a fox or not?", inline=False)
      embed.add_field(name="+love <name> <name2>", value="tells you how much in love 2 individuals are", inline=False)
      embed.add_field(name="+8ball", value="pretty much an 8ball but veni style", inline=False)
      embed.add_field(name="+guess", value="try to guess the number I'm thinking of between 1 and 1000. You have 10 guesses", inline=False)
      embed.add_field(name="+cf <heads or tails>", value="flips a coin", inline=False)       
      embed.add_field(name="+kill <thing you want to kill>", value="kills someone", inline=False)
      embed.add_field(name="+bscan or +boomerscan", value="scans the server for boomers", inline=False)
      embed.add_field(name="+zscan or +zoomerscan", value="scans the server for zoomers", inline=False)
      embed.add_field(name="+ncscan", value="scans the server for Non cubers", inline=False)
      embed.add_field(name="+cuberscan", value="scans the server for cubers", inline=False)
      embed.add_field(name="+noobscan", value="scans the server for noobs", inline=False)
      embed.add_field(name="+smollppscan or +spscan", value="scans the server for people with smoll pps", inline=False)
      embed.add_field(name="+dankmeme", value="generates a meme from r/dankmemes", inline=False)
      embed.add_field(name="+meme", value="generates a meme from r/memes", inline=False)
      embed.add_field(name="+joke", value="generates a joke from r/jokes", inline=False)
      embed.add_field(name="+hack", value="Hacks a user", inline=False)
      embed.add_field(name="+rick", value="Sends rickroll", inline=False)
      embed.add_field(name="+encrypt <shift up the alphabet> <message>", value="encrypt your message! shift has to be between -25 and 25", inline=False)
      embed.add_field(name="+dadtoggle <on/off>", value="turn on or off I'm dad messages", inline=False)
      embed.add_field(name="+quickdraw", value="Test your reaction speed", inline=False)
      embed.add_field(name="+quicklb", value="Check the leaderboard for best reaction times", inline=False)
      await ctx.author.send(embed=embed)

    elif a.lower()=="moderation":
      embed = discord.Embed(title="__**Moderation commands**__", description="Moderation stuff", color=0xeee657)
      embed.add_field(name="+ban <member> <reason>", value="Bans a member", inline=False)
      embed.add_field(name="+kick <member> <reason>", value="kills someone", inline=False)
      embed.add_field(name="+purge <amount>", value="deletes a certain amount of messages", inline=False)
      embed.add_field(name="+mute <member> <reason>", value="mutes a member for some reason", inline=False)
      embed.add_field(name="+unmute <member>", value="unmutes a member", inline=False)
      embed.add_field(name="+invitetoggle <on/off>", value="toggles invite police on or off", inline=False)
      await ctx.author.send(embed=embed)
    elif a.lower()=="economy":
      embed = discord.Embed(title="__**Economy commands**__", description="Money", color=0xeee657)
      embed.add_field(name="+search", value="get money from searching a random place", inline=False)
      embed.add_field(name="+beg", value="beg for money", inline=False)
      embed.add_field(name="+work", value="work your ass off for money", inline=False)
      embed.add_field(name="+daily", value="Get your daily 1000 coins", inline=False)
      embed.add_field(name="+weekly", value="Gets your weekly 5000 coins", inline=False)
      embed.add_field(name="+bal", value="check your balance", inline=False)
      embed.add_field(name="+give <user> <amount>", value="gives a user your money", inline=False)
      embed.add_field(name="+rob", value="robs a user", inline=False)
      embed.add_field(name="+gamble <amount>", value="gambles money", inline=False) 
      embed.add_field(name="+busk", value="try your luck by busking?", inline=False) 
      embed.add_field(name="+hourly", value="collect hourly coins", inline=False) 
      embed.add_field(name="+shop", value="Shows the shop", inline=False) 
      embed.add_field(name="+buy <item>", value="Buy something from the shop", inline=False) 
      embed.add_field(name="+hunt", value="Try your luck hunting! There is a chance you'll be shot though", inline=False)
      embed.add_field(name="+pm", value="post a meme", inline=False) 
      embed.add_field(name="+fish", value="Try fish for something. Maybe you'll get lucky", inline=False) 
      await ctx.author.send(embed=embed)
    
    elif a.lower()=="maths":
      embed = discord.Embed(title="__**Maths commands**__", description="", color=0xeee657)
      embed.add_field(name="+add", value="adds 2 numbers together", inline=False)
      embed.add_field(name="+subtract", value="subtracts the 2nd number from the first",inline=False)
      embed.add_field(name="+divide", value="divides the first number by the 2nd number",inline=False)
      embed.add_field(name="+multiply", value="Multiplies 2 numbers together", inline=False)
      embed.add_field(name="+hcf <num1> <num2>", value="Finds highest common factor of 2 numbers", inline=False)
      embed.add_field(name="+solvequad <a> <b> <c>", value="Solves a quadratic but only if its solveable", inline=False)
      embed.add_field(name="+degtorad <degrees>", value="converts degrees to radians", inline=False)
      embed.add_field(name="+radtodeg <radians>", value="converts radians to degrees", inline=False)
      embed.add_field(name="+pythag <a value> <b value>", value="solves for the hypnotuse", inline=False)
      embed.add_field(name="+factorial", value="Finds the factorial of any number up to 805", inline=False)
      await ctx.author.send(embed=embed)


    elif a.lower()=="covid-19" or a.lower()=="corona" or a.lower()=="coronavirus":
      embed = discord.Embed(title="__**COVID-19 commands**__", description="", color=0xeee657)
      embed.add_field(name="+corona", value="Gives corona stats for a country or the whole world", inline=False)
      embed.add_field(name="+coronatop", value="Shows top 15 corona countries", inline=False)
      embed.add_field(name="+cvhistory", value="Shows history for a country", inline=False)
      await ctx.author.send(embed=embed)

    else:
      await ctx.send("You did not enter a valid help command!")
      return
    emoji = '👍'
    await ctx.message.add_reaction(emoji)
    await ctx.send("Please check your dms!")

  @help.error
  async def help_error(self,ctx,error):
      await ctx.send("Please turn on your dms!")

def setup(bot):
    bot.add_cog(Help(bot))
