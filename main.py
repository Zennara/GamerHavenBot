#imports
import discord
import os
import asyncio
import keep_alive
from mcstatus import MinecraftServer

#declare client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#declare server 
server = MinecraftServer.lookup("gamerhaven.apexmc.co")
serverTest = MinecraftServer.lookup("gamerhaven.secure.pebble.host")

@client.event
async def on_ready():
  print('\n\nBOT ONLINE\n\n')

async def checkStatus():
  await client.wait_until_ready()
  while True:
    #query = server.query()
    #print("The server has the following players online: {0}".format(", ".join(query.players.names)))

    await asyncio.sleep(1)

    channel = await client.fetch_channel(int(859141243983364136))

    try:
      status = server.status()
      online = True
    except:
      online = False

    if not online:
      for messages in await channel.history(limit=None, oldest_first=True).flatten():
        await messages.delete()

      embed = discord.Embed(color=0x593695, description="Server is currently down.")
      embed.set_author(name="❌ | @" + client.user.name)
      await channel.send(embed=embed, content="@!274245369389645827>")

      while not online:
        try:
          status = server.status()
        except:
          online = False
    
    if online:
      for messages in await channel.history(limit=None, oldest_first=True).flatten():
        await messages.delete()

      embed = discord.Embed(color=0x593695, description="Server is currently up with **" + str(status.players.online) + "** players online.")
      embed.set_author(name="✔️ | @" + client.user.name)
      await channel.send(embed=embed, content="@!274245369389645827>")

      while online:
        print("sayy")
        try:
          status = server.status()
        except:
          online = False

done = False
async def checkPlayers():
  await client.wait_until_ready()
  channel = await client.fetch_channel(int(859141243983364136))
  while True:
    await asyncio.sleep(1)
    print("test")

    try:
      status = server.status()
      online = True
    except:
      online = False
    print("test")

    #try:
    print("test")
    for messages in await channel.history(limit=None, oldest_first=True).flatten():
      embedt = messages.embeds[0]
    print("test2")
    if str(status.players.online) not in embedt.description and online:
      print("test3")
      embed = discord.Embed(color=0x593695, description="Server is currently up with **" + str(status.players.online) + "** players online.")
      embed.set_author(name="✔️ | @" + client.user.name)
      await messages.edit(embed=embed)
    print("test4")
    #except Exception as x:
      #print(str(x))
  print("test5")

client.loop.create_task(checkPlayers())
client.loop.create_task(checkStatus())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by data
client.run(os.environ.get("TOKEN"))