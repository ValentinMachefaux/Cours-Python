import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# Charge le fichier .env qui est dans le meme dossier
load_dotenv()

# Recup le token discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# recup l'objet client de l'api discord.py
bot = discord.Client()

#@bot.command()
@bot.event
async def on_message(message):

  if message.content == "hello":
    await message.channel.send("Greetings !")






bot.run(DISCORD_TOKEN)