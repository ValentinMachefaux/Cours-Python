import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord_ui import Button

# Charge le fichier .env qui est dans le meme dossier
load_dotenv()

# Recup le token discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# creation d'un nouvel objet bot avec un prefix
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
embed = discord.Embed
user = discord.user

@bot.command()
async def hello(ctx):
  await ctx.channel.send("Greetings")

@bot.event
async def on_message(message):
  #await message.delete()
  await bot.process_commands(message)

  if message.content == "blip":
    await message.channel.send("bloup")

@bot.command()
async def game(ctx):

  emd = embed(
    title=ctx.author,
    description="Voulez vous jouer a un jeu ? ",
    components=[[
      Button( 
          color="blue",
          custom_id="button1",
          label="Blue button",
          emoji="🚀",
      ),
      Button(
          #style=ButtonStyle.red,
          custom_id="button2",
          label="Red button",
          disabled=True,
          emoji="🐺",
      ),
      Button(
          #style=ButtonStyle.green,
          custom_id="button3",
          label="Green button",
          emoji="😄",
      ),
    ]]
  )
  await ctx.send(embed=emd)

@bot.event
async def on_ready():
  print("The bot is ready")





bot.run(DISCORD_TOKEN)