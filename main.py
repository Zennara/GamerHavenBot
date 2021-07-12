#imports
import discord
import os
import asyncio
import keep_alive
from mcstatus import MinecraftServer

#declare client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

print('\n\nBOT ONLINE\n\n')

#declare server 
server = MinecraftServer.lookup("gamerhaven.apexmc.co")
serverTest = MinecraftServer.lookup("gamerhaven.secure.pebble.host")

async def checkStatus():
  while True:
    status = server.status()
    #query = server.query()
    #print("The server has the following players online: {0}".format(", ".join(query.players.names)))

    await asyncio.sleep(1)

    channel = await client.fetch_channel(int(859141243983364136))

    try:
      status = server.status()
      test = status.latency
      online = True
    except:
      online = False

    print("-----")
    print(str(online))

    if not online:
      for messages in await channel.history(limit=None, oldest_first=True).flatten():
        await messages.delete()

      embed = discord.Embed(color=0x593695, description="Server is currently down.")
      embed.set_author(name="❌ | @" + client.user.name)
      await channel.send(embed=embed, content="<@!274245369389645827>")

      while not online:
        try:
          status = server.status()
          test = status.latency
          online = True
        except:
          online = False
    
    if online:
      for messages in await channel.history(limit=None, oldest_first=True).flatten():
        await messages.delete()

      embed = discord.Embed(color=0x593695, description="Server is currently up with **" + str(status.players.online) + "** players online.")
      embed.set_author(name="✔️ | @" + client.user.name)
      await channel.send(embed=embed, content="<@!274245369389645827>")

      while online:
        try:
          status = server.status()
          test = status.latency
          online = True
        except:
          online = False


async def checkPlayers():
  while True:
    await asyncio.sleep(600)

    status = server.status()

    print("The server has {0} players and repli ed in {1} ms".format(status.players.online, status.latency))

    for guild in client.guilds:
      for channel in guild.voice_channels:
        if "Players:" in channel.name:
          if channel.name != "「👥」Players: " + str(status.players.online):
            await channel.edit(name="「👥」Players: "+ str(status.players.online))

client.loop.create_task(checkPlayers())
client.loop.create_task(checkStatus())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by data
client.run(os.environ.get("TOKEN"))