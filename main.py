import discord
from discord.ext import commands
from discord.utils import get
import urllib.request
from datetime import datetime
import os
import random

# When running on a virtual machine online, some modules go back to previous versions and must be updated.
os.system("pip install pytube --upgrade")
os.environ['MPLCONFIGDIR'] = "MPLCONFIGDIR"
client = commands.Bot(command_prefix = "?")

# Add cogs for every .py file in the cogs directory.
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

# a function for Rock Paper Scissors to determine winning scores
def get_score(user, computer, mention):
  user_rock = {"paper": "I", "scissors": "You"}
  user_paper = {"rock": "You", "scissors": "I"}
  user_scissors = {"rock": "I", "paper": "You"}

  if user == computer:
    return f"{mention} It's a tie! I also chose {user}"
  
  if user == "rock":
    win = user_rock.get(computer)
  elif user == "paper":
    win = user_paper.get(computer)
  elif user == "scissors":
    win = user_scissors.get(computer)
  return f"{mention} {win} win! I chose {computer} and you chose {user}"

@client.event
async def on_ready():
  print("===Caroline activated===")
  channel = client.get_channel(841948085855715371) # general
  await client.change_presence(activity=discord.Game('Portal (?help)'))
  await channel.send("Online!")

# Welcome new users
@client.event
async def on_member_join(member):
  channel = client.get_channel(841948085855715371)
  await channel.send(f"Welcome, {member.mention}!")

# RPS reaction check
bot_messages = []
@client.listen()
async def on_raw_reaction_add(react):
  global bot_messages
  msg_id = react.message_id
  channel = client.get_channel(react.channel_id)
  reacts = ["💎", "📰", "✂"]
  words = ["rock", "paper", "scissors"]
  computer = random.choice(words)
  if not react.member.bot and react.emoji.name in reacts and msg_id in bot_messages:
    i = reacts.index(react.emoji.name)
    user = words[i]
    score = get_score(user, computer, react.member.mention)
    await channel.send(score)
    bot_messages.remove(msg_id)

# Begin RPS Game
@client.command(brief="Rock, Paper, Scissors!")
async def rps(ctx):
  global bot_messages
  embed = discord.Embed(title="**Rock Paper Scissors**")
  msg = await ctx.send(embed=embed)
  reacts = ["💎", "📰", "✂"]
  for i in reacts:
    await msg.add_reaction(i)
  bot_messages.append(msg.id)

  # Check for DMs and report to Loud_Cat
@client.event
async def on_message(message):
  cat = await client.fetch_user(771066520726011904)
  user = message.author
  pfp = user.avatar_url_as()
  if str(message.channel) == str(user.dm_channel) and user != cat:
    embed = discord.Embed(timestamp=datetime.now())
    embed.add_field(name=str(user.dm_channel), value=message.content)
    embed.set_footer(text=f"User id: {user.id}", icon_url = pfp)
    await cat.send(embed=embed)
  await client.process_commands(message)

client.run(os.environ['TOKEN'])
