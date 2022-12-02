import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button,View,Select


# Charge le fichier .env qui est dans le meme dossier
load_dotenv()

# Recup le token discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# creation d'un nouvel objet bot avec un prefix
bot = commands.Bot(command_prefix="!",case_insensitive=True,intents=discord.Intents.all())
embed = discord.Embed
user = discord.user.User
style = discord.ButtonStyle
option=discord.SelectOption


class MyButton(Button):
  def __init__(self,label,style,id):
    super().__init__(label=label,style=style,custom_id=id)

  async def callback(self,inte):
    if inte.custom_id == "bonjour":
      await inte.response.send_message("Eh bien continuons dans ce cas !")
    elif inte.custom_id == "non":
      await inte.response.send_message("Passe ton chemin alors !")


@bot.command()
async def game(ctx):
  view = View()

  emd = embed(
    title="Voulez vous jouer a un jeu ?",
    color=discord.Color.blurple(),
  )
  emd.set_author(
    name=ctx.author.display_name,
    icon_url=ctx.author.avatar)


  buttonN = MyButton("je peux pas j'ai piscine",style.danger,"non")




  view.add_item(MyButton("boujour",style.primary,"bonjour"))
  view.add_item(buttonN)
  await ctx.send(embed=emd,view=view)


@bot.event
async def on_ready():
  print("The bot is ready")
  


bot.run(DISCORD_TOKEN)