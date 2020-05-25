import discord
from discord.ext import commands
import pymongo
import dns
import os

mongosecret=os.environ.get("mongosecret")
client = pymongo.MongoClient(mongosecret)
db = client["comp"]
collection=db["results"]

class Comp(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  


  
  @commands.command()
  async def records(self,ctx):
    def convert(seconds):
        minutes =seconds/60
        for i in range(10000):
            if minutes>i and minutes<i+1:
                minutes=i
        secs=round((seconds % 60),2)
        if minutes==0:
            time="{}".format(secs)
        else:
          if secs <10:
            secs="0{}".format(secs)
          time=f"{minutes}:{secs}"
        return time
    collection=db["records"]
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      record=result
    eventlist=["2x2","3x3","4x4","5x5","6x6","7x7","pyraminx","oh","skewb","square-1","clock","megaminx","3bld","4bld","5bld"]
    eventson=[]
    for event in eventlist:
      onoff=db.config
      results=onoff.find({"_id":ctx.guild.id})
      for result in results:
        config=result
      if config[event]["mode"]=="on":
        eventson.append(event)
    embed=discord.Embed(title=f"Records for {ctx.guild}",description="",color=0xffff00)
    for event in eventson:
      user,usersingle=record[event]["single"].split(" with a single of ")
  
      user2,useraverage=record[event]["average"].split(" with an average of ")


      embed.add_field(name=event.capitalize(),value=f"Single: {user} with a single of {usersingle}\nAverage: {user2} with an average of {useraverage}")
    await ctx.send(embed=embed)


  
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def reset(self,ctx,member:discord.Member=None,event=None):
    if not event:
      await ctx.send("Sorry, you must enter a valid event")
      return
    if not member:
      await ctx.send("You must enter a valid member")
      return
    event=event.lower()
    if event=="pyra":
      event="pyraminx"
    elif event=="skweeb":
      event="skewb"
    elif event=="sq1" or event.lower()=="squan":
      event="square-1"
    elif event=="mega":
      event="megaminx"
    elif event=="cloncc":
      event="clock"
    await ctx.send(f"Are you sure you want to reset all {event} results for this user?")
    message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
    while message.content.upper()!="Y" and message.content.upper()!="N":
      message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
      await ctx.send("Please enter Y or N!")
    if message.content.upper()=="N":
      await ctx.send("Ok No reset")
      return
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      comp=result
    userlist={}
    for key in comp[event]:
      userlist[key]=comp[event][key]
    try:
      del userlist[str(member.id)]
    except KeyError:
      await ctx.send(f"That user has no results for {event}")
      return
    
    collection.update_one({"_id":ctx.guild.id},{"$set":{event:userlist}})
    await ctx.send(f"Successfully reset {event} results for {member}")
  
  @reset.error
  async def reset_error(self,ctx,error):
    if isinstance(error,commands.MissingPermissions):
      await ctx.send("Sorry you need manage messages permissions to run this command")
    
    


  @commands.command()
  async def submit(self,ctx,event=None,single=None,average=None):

    collban=db.bans
    results=collban.find({"_id":ctx.guild.id})
    for result in results:
      ban=result
    try:
      userban=ban["bans"][str(ctx.author.id)]
    except KeyError:
      userlist={}
      for key in ban["bans"]:
        userlist[key]=ban["bans"][key]
      userlist[str(ctx.author.id)]="not banned"
      collban.update_one({"_id":ctx.guild.id},{"$set":{"bans":userlist}})
      userban="not banned"
    if userban=="banned":
      await ctx.send("Sorry you are banned from competitions and will not be able to compete.")
      return

    def get_sec(time_str):
      if time_str.upper()=="DNF":
        return "DNF"
      count=time_str.count(":")
      if count==1:
        m, s = time_str.split(':')
        check= float(m) * 60 + float(s)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check
      elif count==2:
        h, m, s = time_str.split(':')
        check=float(h) * 3600 + float(m) * 60 + float(s)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check

      elif count==0:
        check=float(time_str)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check

    def convert(seconds): 
      minutes =seconds/60
      for i in range(10000):
          if minutes>i and minutes<i+1:
              minutes=i
      secs=round((seconds % 60),2)
      if minutes==0:
          time="{}".format(secs)
      else:
        if secs <10:
          secs="0{}".format(secs)
        time=f"{minutes}:{secs}"
      return time

      
    if not event:
      await ctx.send("Please enter a valid event to submit!")

    if not single:
      await ctx.send("You have to specify a single!")
    if not average:
      await ctx.send("You must specify an average to submit!")
    if single.lower()=="nan" or average.lower()=="nan" or single.lower()=="infinity" or average.lower()=="infinity":
      await ctx.send("You must enter a valid single/average!")
      return
    event=event.lower()
    eventson=[]
    
    if event=="pyra":
      event="pyraminx"
    elif event=="skweeb":
      event="skewb"
    elif event=="sq1" or event.lower()=="squan":
      event="square-1"
    elif event=="mega":
      event="megaminx"
    elif event=="cloncc":
      event="clock"
    eventlist=["2x2","3x3","4x4","5x5","6x6","7x7","pyraminx","oh","skewb","square-1","clock","megaminx","3bld","4bld","5bld"]
    eventson=[]
    for item in eventlist:
      onoff=db.config
      results=onoff.find({"_id":ctx.guild.id})
      for result in results:
        config=result
      if config[item]["mode"]=="on":
        eventson.append(item)
    
    if event not in eventson:
      await ctx.send("Sorry that event is not recognised/enabled on this server!")
      return
    
    try:
      testsingle=get_sec(single)
    except ValueError:
      testsingle=single
    except TypeError:
      testsingle=single
    
    try:
      testaverage=get_sec(average)
    except ValueError:
      testaverage=average
    except TypeError:
      testaverage=average
    if testaverage=="You cannot enter a time less than or equal to 0 seconds!":
      await ctx.send(testaverage)
      return
    if testsingle=="You cannot enter a time less than or equal to 0 seconds!":
      await ctx.send(testsingle)
      return
    
    try:
      single=float(single)
    except ValueError:
      single=get_sec(single)
    try:
      average=float(average)
    except ValueError:
      average=get_sec(average)
    if single=="DNF":
      oksingle=100000000000000000000000
    else:
      oksingle=single
    if average=="DNF":
      okaverage=100000000000000000000000
    else:okaverage=average
    if oksingle>okaverage:
      await ctx.send("Your submitted times are invalid because your average is faster than your single! Make sure you have submitted your results in the format +submit <event> <single> <average>!")
      return
    try:
      single=convert(single)
    except ValueError:
      single=single
    except TypeError:
      single=single
    try:
      average=convert(average)
    except ValueError:
      average=average
    except TypeError:
      average=average
    try:
      stime=get_sec(single)
      if stime=="You cannot enter a single less than or equal to 0 seconds!":
        await ctx.send(stime)
        return
    except ValueError:
      if single.upper()=="DNF":
        stime="DNF"
      else:
        await ctx.send("That is not a valid single and/or average!")
        return

    try:
      saverage=get_sec(average)
      if stime=="You cannot enter a single less than or equal to 0 seconds!":
        await ctx.send(saverage)
        return
    except ValueError:
      if average.upper()=="DNF":
        saverage="DNF"
      else:
        await ctx.send("Sorry that is not a valid single and/or average!")
        return
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      comp=result
    userlist={}
    for key in comp[event]:
      userlist[key]=comp[event][key]
    userlist[str(ctx.author.id)]={"average":saverage,"single":stime}
    collection.update_one({"_id":ctx.guild.id},{"$set":{event:userlist}})
    await ctx.send(f"Successfully submitted a single of {single} and an average of {average} for {event}")
  
  @commands.command()
  async def view(self,ctx):

    def convert(seconds): 
        minutes =seconds/60
        for i in range(10000):
            if minutes>i and minutes<i+1:
                minutes=i
        secs=round((seconds % 60),2)
        if minutes==0:
            time="{}".format(secs)
        else:
          if secs <10:
            secs="0{}".format(secs)
          time=f"{minutes}:{secs}"
        return time
    
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      comp=result
    eventlist=["2x2","3x3","4x4","5x5","6x6","7x7","pyraminx","oh","skewb","square-1","clock","megaminx","3bld","4bld","5bld"]
    eventson=[]
    for event in eventlist:
      onoff=db.config
      results=onoff.find({"_id":ctx.guild.id})
      for result in results:
        config=result
      if config[event]["mode"]=="on":
        eventson.append(event)
    embed=discord.Embed(title=f"Submissions for {ctx.author}",description="",color=0xffff00)
    for event in eventson:
      try:
        usersingle=convert(comp[event][str(ctx.author.id)]["single"])
      except TypeError:
        usersingle="DNF"
      except KeyError:
        usersingle="None"
      try:
        useraverage=convert(comp[event][str(ctx.author.id)]["average"])
      except TypeError:
        useraverage="DNF"
      except KeyError:
        useraverage="None"
      

      embed.add_field(name=event.capitalize(),value=f"Single: {usersingle}\nAverage: {useraverage}")
    await ctx.send(embed=embed)
  

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def podiums(self,ctx):
    overall={}
    def get_sec(time_str):
      count=time_str.count(":")
      if count==1:
        m, s = time_str.split(':')
        check= float(m) * 60 + float(s)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check
      elif count==2:
        h, m, s = time_str.split(':')
        check=float(h) * 3600 + float(m) * 60 + float(s)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check

      elif count==0:
        check=float(time_str)
        if check<=0:
          return "You cannot enter a time less than or equal to 0 seconds!"
        else:
          return check
    
    def convert(seconds): 
        minutes =seconds/60
        for i in range(10000):
            if minutes>i and minutes<i+1:
                minutes=i
        secs=round((seconds % 60),2)
        if minutes==0:
            time="{}".format(secs)
        else:
          if secs <10:
            secs="0{}".format(secs)
          time=f"{minutes}:{secs}"
        return time

    await ctx.send("Are you sure you want to reset all results and do podiums Y/N?")
    message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
    while message.content!="Y" and message.content!="N":
      message = await self.bot.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
      await ctx.send("Please enter Y or N!")
    if message.content=="N":
      await ctx.send("Ok No reset")
      return
    results=collection.find({"_id":ctx.guild.id})
    for result in results:
      comp=result
    events=["2x2","3x3","4x4","5x5","6x6","7x7","pyraminx","oh","skewb","square-1","clock","megaminx","3bld","4bld","5bld"]
    for event in events:
      lblist={}
      users=[]
      lb_list=[]
      for key in comp[event]:
        users.append(key)
      for user in users:
        lblist[user]=comp[event][user]["average"]
      print (lblist) 
      for key,value in sorted(lblist.items(), key=lambda item: item[1]):
        try:
          value=convert(value)
        except TypeError:
          value=0
        if value!=0:
          string="<@%s> : %s" % (key,value)
          lb_list.append(string)
      listlen=len(lb_list)
      listlen1=len(lb_list)

      if listlen>3:
        listlen=3
      #extra
      if len(lb_list)!=0:
        bestuser,bestaverage=lb_list[0].split(" : ")

        collrecords=db["records"]
        results=collrecords.find({"_id":ctx.guild.id})
        for result in results:
          records=result

        person,record=records[event]["average"].split(" with an average of ")
        bestaverage=get_sec(bestaverage)
        if record=="None":
          record=100000000000000000000000
        try:
          record=get_sec(record)
        except AttributeError:
          record=record
        if bestaverage<record:
          userlist={}
          bestaverage=convert(bestaverage)
          for key in records[event]:
            userlist[key]=records[event][key]
          userlist["average"]=f"{bestuser} with an average of {bestaverage}"
          collrecords.update_one({"_id":ctx.guild.id},{"$set":{event:userlist}})
      lblist1={}
      users1=[]
      lb_list1=[]
      for key in comp[event]:
        users1.append(key)
      for user in users1:
        lblist1[user]=comp[event][user]["single"]
      for key,value in sorted(lblist1.items(), key=lambda item: item[1]):
        try:
          value=convert(value)
        except TypeError:
          value=0
        if value!=0:
          string="<@%s> : %s" % (key,value)
          lb_list1.append(string)
      listlen11=len(lb_list1)
      listlen111=len(lb_list1)
      if len(lb_list1)!=0:
        bestuser,bestsingle=lb_list1[0].split(" : ")

        collrecords=db["records"]
        results=collrecords.find({"_id":ctx.guild.id})
        for result in results:
          records=result

        person,record=records[event]["single"].split(" with a single of ")
        bestsingle=get_sec(bestsingle)
        if record=="None":
          record=100000000000000000000000
        try:
          record=get_sec(record)
        except AttributeError:
          record=record
        if bestsingle<record:
          userlist={}
          bestsingle=convert(bestsingle)
          for key in records[event]:
            userlist[key]=records[event][key]
          userlist["single"]=f"{bestuser} with a single of {bestsingle}"
          collrecords.update_one({"_id":ctx.guild.id},{"$set":{event:userlist}})  
      #extra end
      onemessage=[]
      if listlen>0:
        onemessage.append(f"{event.capitalize()} podium:")
      for i in range(listlen1-1):
        if len(lb_list)!=0:
          user,average=lb_list[i].split(" : ")
          user2,average2=lb_list[i+1].split(" : ")
          stuff,user1=user.split("@")
          user3,stuf2f=user1.split(">")
          stuff2,user6=user2.split("@")
          user4,studd4=user6.split(">")
          averagelist={}
          averagelist[user]=average
          averagelist[user2]=average2
          if averagelist[user]==averagelist[user2]:
            usersingle=comp[event][user3]["single"]
            user2single=comp[event][user4]["single"]
            useravg=comp[event][user3]["average"]
            user2avg=comp[event][user4]["average"]
            if usersingle>user2single:
              lb_list[i]=f"{user2} : {user2avg}"
              lb_list[i+1]=f"{user} : {useravg}"
      for i in range(listlen):
        user,average=lb_list[i].split(" : ")
        try:
          userinlist=overall[user]
        except KeyError:
          overall[user]=0
        ok,user2=user.split("@")
        user1,test=user2.split(">")
        usersingle=comp[event][user1]["single"]
        usersingle=convert(usersingle)
        if i==0:
          onemessage.append(f"1st place: {user} with an average of {average} and a single of {usersingle}")
          overall[user]+=3
        elif i==1:
          onemessage.append(f"2nd place: {user} with an average of {average} and a single of {usersingle}")
          overall[user]+=2
        elif i==2:
          onemessage.append(f"3rd place: {user} with an average of {average} and a single of {usersingle}")
          overall[user]+=1
      onelen=len(onemessage)
      if onelen>0:
        await ctx.send("\n".join(onemessage))
    winner=[]
    winners=[]
    for key,value in sorted(overall.items(),reverse=True, key=lambda item:item[1]):
      string="%s : %s" % (key,value)
      winner.append(string)
    print(winner)
    winner1,points=winner[0].split(" : ")
    try:
      winner2,points2=winner[1].split(" : ")
    except IndexError:
      points2=0
    try:
      winner3,points3=winner[2].split(" : ")
    except IndexError:
      points3=0
      
    if points==points2:
      times=2
      winners.append(f"{winner1} wins this week with {points} points")
      winners.append(f"{winner2} wins this week with {points2} points")

    if points==points3 and points2==points3 and points==points2:
      times=3
      winners.append(f"{winner3} wins this week with {points} points")
      winners.append(f"{winner1} wins this week with {points} points")
      winners.append(f"{winner2} wins this week with {points} points")
    if points!=points2:
      times=1
      winners.append(f"{winner1} wins this week with {points} points")
    print (winners)   
    for i in range(times):
      await ctx.send(winners[i])
    collection.update_one({"_id":ctx.guild.id},{"$set":{"3x3":{},"4x4":{},"2x2":{},"5x5":{},"6x6":{},"7x7":{},"square-1":{},"skewb":{},"clock":{},"pyraminx":{},"oh":{},"megaminx":{},"3bld":{},"4bld":{},"5bld":{}}})
  
  @podiums.error
  async def podiums_error(self,ctx,error):
    if isinstance(error,commands.MissingPermissions):
      await ctx.send("Sorry you need manage messages permissions to run this command")


def setup(bot):
  bot.add_cog(Comp(bot))
