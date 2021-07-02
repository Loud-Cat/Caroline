import discord
from discord.utils import get
from subprocess import *
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

client = commands.Bot(command_prefix = "?")
class Admin(commands.Cog):
  """Admin only commands"""
  def __init__ (self, client):
    self.client = client

  @client.command(brief="Remove {num} messages (including ?purge)")
  async def purge(self, ctx, num=2):
    num = int(num)
    await ctx.channel.purge(limit=num)
    msg = await ctx.send(f"Channel cleared by {ctx.author.mention}")
    await asyncio.sleep(4)
    await msg.delete()
  
  @client.command()
  async def image(self, ctx, *, search="ice-cream"):
    await ctx.send("Searching... may take a while.")
    search = search.replace(" ", "-")
    url = 'https://unsplash.com/s/photos/' + search
    session = requests.Session()
    my_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36".strip()}
    resp = session.get(url, headers=my_headers)
    all_images = BeautifulSoup(resp.content, 'html.parser').find_all('img')

    image_links = set()
    for link in all_images:
      try:
        src = link['src']
        if "profile" not in src and 'crop' not in src:
          image_links.add(urljoin(url, src))
      except Exception as e:
        print(e)
        continue
    image_links = [*image_links]
    print("\n\n".join(image_links))
    print("\n\n\n")

    choice = ""
    if not image_links:
      await ctx.send("Sorry! Couldn't find anything.")
      return
    
    while len(choice) < 10 or 'gif' in choice or 'unsplash' not in choice:
      choice = __import__("random").choice(image_links)
    await ctx.send(choice)

def setup(client):
  client.add_cog(Admin(client))
