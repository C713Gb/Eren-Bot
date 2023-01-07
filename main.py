import discord
import os
import requests
import json

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


@client.event
async def on_ready():
  guild = discord.utils.get(client.guilds, name=GUILD)

  print(
      f'{client.user} is connected to the following guild:\n'
      f'{guild.name}(id: {guild.id})'
  )
  
  members = '\n - '.join([member.name for member in guild.members])
  print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
  print("Message Author -> {0}".format(message.author))
  if message.author == client.user:
    return

  quote = get_quote()
  await message.channel.send(quote)


client.run(TOKEN)

