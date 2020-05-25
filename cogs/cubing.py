import discord,random,asyncio,gspread,os,pymongo,dns
from discord.ext import commands, tasks
from oauth2client.service_account import ServiceAccountCredentials
from pycubescrambler import nxn,side,bld



mongosecret=os.environ.get("mongosecret")
client = pymongo.MongoClient(mongosecret)
db = client["scrambles"]
collection=db["4x4"]

scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('venibot-cce23e8af80f.json', scope)
gc = gspread.authorize(credentials)
gc.login()
@tasks.loop(seconds=10)
async def refresh(gc):
  gc.login()

class Cubing(commands.Cog):
  def __init__(self,bot):
    self.bot=bot
  
  


  @commands.command(aliases=["avg"])
  async def avgcalculator(self,ctx,time1,time2,time3,time4,time5):
    def get_sec(time_str):
      count=time_str.count(":")
      if count==1:
        m, s = time_str.split(':')
        secs= float(m) * 60 + float(s)
        return round(secs,2)
      elif count==2:
        h, m, s = time_str.split(':')
        secs= float(h) * 3600 + float(m) * 60 + float(s)
        return round(secs,2)
      elif count==0:
        s=float(time_str)
        return round(s,2)

    def convert(seconds): 
      minutes =seconds/60
      for i in range(60):
        if minutes>i and minutes<i+1:
          minutes=i
      secs=round((seconds % 60),2)
      if minutes==0:
        time="{}".format(round(secs,2))
      else:
        if secs <10:
          secs="0{}".format(round(secs,2))
        time=f"{minutes}:{secs}"
      return time

    times=[time1,time2,time3,time4,time5]
    timelist=[]
    for item in times:
      try:
        stime=get_sec(item)
        timelist.append(stime)
      except ValueError:
        await ctx.send(f"{item} is not a valid time!")
        return
    
    timelist.sort()
    avg=timelist[1]+timelist[2]+timelist[3]
    avg5=avg/3
    avg5=convert(avg5)
    await ctx.send(f"Your average is {avg5}!")

  @commands.command()
  async def memescram(self,ctx):
    await ctx.send("D L2 R2 U L2 U2 R2 U L2 U' B2 U2 F' L' R2 D U2 B' R' D' R2 D2")
  
  @commands.command()
  async def zbll(self,ctx):
    await ctx.send("https://docs.google.com/spreadsheets/d/1-uwmZHf4vwJxFgeB3-TiF8MQ0RFSS30d5CUK96PoIwk/edit#gid=34031343")
  @commands.command()
  async def pbs(self,ctx):
    wks = gc.open("Test").sheet1
    wks1=gc.open("averages").sheet1
    userid=str(ctx.author.id)
    try:
      user=wks.find(str(ctx.author.id))
    except gspread.exceptions.CellNotFound:
      wks.append_row([userid,"2x2","None","3x3","None","4x4","None","5x5","None","6x6","None","7x7","None","pyraminx","None","skewb","None","square-1","None","oh","None","clock","None","megaminx","None","3bld","None","4bld","None","5bld","None","mbld","None","fmc","None"])
      user=wks.find(str(ctx.author.id))
    try:
      user1=wks1.find(str(ctx.author.id))
    except gspread.exceptions.CellNotFound:
      wks1.append_row([userid,"2x2","None","3x3","None","4x4","None","5x5","None","6x6","None","7x7","None","pyraminx","None","skewb","None","square-1","None","oh","None","clock","None","megaminx","None","3bld","None","4bld","None","5bld","None","mbld","None","fmc","None"])
      user1=wks1.find(str(ctx.author.id))

    user_row=user.row
    user_row1=user1.row
    pb_singles=wks.row_values(user_row)
    pb_averages=wks1.row_values(user_row1)
    send=[]
    send1=[]
    for i in range(1,35,2):
      string=f"{pb_singles[i]} : {pb_singles[i+1]}"
      send.append(string)
    ms=", ".join(send)
    for i in range(1,35,2):
      string=f"{pb_averages[i]} : {pb_averages[i+1]}"
      send1.append(string)
    msg=", ".join(send1)
    await ctx.send(f"PB singles for <@{ctx.author.id}>:\n{ms}\nPB averages for <@{ctx.author.id}>:\n {msg}")

  @commands.command()
  async def update(self,ctx,event,sora,time):
    wks = gc.open("Test").sheet1
    wks1=gc.open("averages").sheet1
    userid=str(ctx.author.id)
    event=event.lower()
    
    if sora=="single":
      try:
        user=wks.find(str(ctx.author.id))
      except gspread.exceptions.CellNotFound:
        wks.append_row([userid,"2x2","None","3x3","None","4x4","None","5x5","None","6x6","None","7x7","None","pyraminx","None","skewb","None","square-1","None","oh","None","clock","None","megaminx","None","3bld","None","4bld","None","5bld","None","mbld","None","fmc","None"])
        user=wks.find(str(ctx.author.id))
      user_row=wks.find(str(ctx.author.id)).row
      update_pb=(wks.find(event).col)+1
      wks.update_cell(user_row,update_pb,time)
    elif sora=="average" or sora=="avg":
      try:
        user=wks.find(str(ctx.author.id))
      except gspread.exceptions.CellNotFound:
        wks1.append_row([userid,"2x2","None","3x3","None","4x4","None","5x5","None","6x6","None","7x7","None","pyraminx","None","skewb","None","square-1","None","oh","None","clock","None","megaminx","None","3bld","None","4bld","None","5bld","None","mbld","None","fmc","None"])
        user=wks1.find(str(ctx.author.id))
      user_row=user.row
      user_row=wks1.find(str(ctx.author.id)).row
      update_pb=(wks1.find(event).col)+1
      wks1.update_cell(user_row,update_pb,time)


      
    await ctx.send(f"Successfully updated your {event} pb {sora} to {time}!")
  @commands.command()
  async def s(self,ctx,a, b:int = 1):
    if b>5:
      b=5
    a=a.lower()
    if a == "1x1":
      for x in range(b):
        a=nxn.get1()
        await ctx.send(a)

    elif a == "megaminx" or a == "mega":
      for x in range(b):
        a=side.get_mega()
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="4x4":
      for i in range(b):
        list1=[]
        results=collection.find({})
        
        scramble=results[0]["scramble"]
        embed=discord.Embed(title="",description=scramble,color=0xffff00)
        await ctx.send(embed=embed)
        scram=collection.find({"scramble":scramble})
        list2=[]
        for result in scram:
          list2.append(result["_id"])
        collection.delete_one({"_id":list2[-1],"scramble":scramble})
        
    elif a=="8x8":
      for i in range(b):
        a=nxn.get8()
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="9x9":
      for i in range(b):
        a=nxn.get9()
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="10x10":
      for i in range(b):
        a=nxn.get10()
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="11x11":
      for i in range(b):
        a=nxn.get11()
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="12x12":
      for i in range(b):
        a=nxn.get_big_cube(12)
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
    elif a=="13x13":
      for i in range(b):
        a=nxn.get_big_cube(13)
        embed=discord.Embed(title="",description=a,color=0xffff00)
        await ctx.send(embed=embed)
  @commands.command()
  async def bigcube(self,ctx,size:int=8,num:int=1):
    if size<8:
      await ctx.send("The smallest cube size is 8")
      return
    for i in range(num):
      scram=nxn.get_big_cube(size)
      embed=discord.Embed(title="",description=scram,color=0xffff00)
      try:
        await ctx.send(embed=embed)
      except discord.errors.HTTPException:
        await ctx.send("Sorry I cannot send that scramble because it is too long")
        return
    


def setup(bot):
  bot.add_cog(Cubing(bot))
