import discord
import os
from dotenv import load_dotenv
import json
import random
from discord.ext import commands
from discord.ui import Button,View,Select
from discord.reaction import Reaction


# Charge le fichier .env qui est dans le meme dossier
load_dotenv()

# Recup le token discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# creation d'un nouvel objet bot avec un prefix
bot = commands.Bot(command_prefix="!",case_insensitive=True,intents=discord.Intents.all())

embed = discord.Embed
style = discord.ButtonStyle
option = discord.SelectOption

@bot.event
async def on_ready():
  print("The bot is ready")

class MyButton(Button):
  def __init__(self,label,style,id):
    super().__init__(label=label,style=style,custom_id=id)

  async def callback(self,inte):
    if inte.custom_id == "oui":
      await inte.response.send_message("Bravo !")
    elif inte.custom_id == "non":
      await inte.response.send_message("Raté !")

@bot.command()
async def coucou(ctx):
  print("coucou")

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


  buttonY = MyButton("Yes",style.green,"yes")
  buttonN = MyButton("No",style.grey,"no")
  respButton = discord.Interaction.response

  view.add_item(buttonY)
  view.add_item(buttonN)

  await ctx.send(embed=emd,view=view)
  
  if discord.Interaction.custom_id == "yes":
    print("bravo")
    await respButton.send_message("bravo")



@bot.command()
async def quiz(ctx,message):
  with open('Bot_discord/questions.json','r',encoding="utf8") as f:
    data = json.loads(f.read())
    data_dic = data["quizz"]

  class Qcm(Select):
      async def callback(self,interaction):
        if self.values[0] == random_reponse:
          print(random_anec)
          await interaction.response.send_message(embed=embed(title="Bravo mais saviez-vous que :", description=random_anec))
        else:
          print(random_anec)
          await interaction.response.send_message("Raté, essaye encore") #TO DO moins X point



  ran = random.randint(0,len(data_dic))
  
  random_question = data_dic[0]["question"]
  random_reponse =data_dic[ran]["reponse"]
  random_prop =data_dic[ran]["propositions"]
  random_anec =data_dic[ran]["anecdote"]
  random_indice =data_dic[ran]["indice"]

  view =View()

  qcm1 = Qcm(
    options=[
      option(label=random_prop[0]),
      option(label=random_prop[1]),
      option(label=random_prop[2]),
      option(label=random_prop[3]),
    ],row=4
  )

  if message.content == "indice":
    await ctx.send(embed=embed(description=random_indice))

  view.add_item(qcm1)
  await ctx.send(embed=embed(description=random_question),view=view)

#@bot.command()
#async def hello(ctx,message):
    #print(ctx.content)
    #if ctx.author==bot.user:
    #  return 
    
#    if message.content=="hello":
#      channel = bot.get_channel(1044897838674497559)
#      await ctx.send("Bienvenue dans l'antre du Riddler ")
#  
#      def check(message):
#        return   ctx.channel == ctx.channel 
#
#      await bot.wait_for("message", check=check)
#      message=await ctx.channel.send("Preparez-vous au top .Une fois pret validez avec 👍 sinon 👎")
#      await ctx.add_reaction("👍")
#      await ctx.add_reaction("👎")
      
#      def checkEmoji(reaction,user):
#        return  ctx.id == reaction.ctx.id and (str(reaction.emoji) == "👍" or str(reaction.emoji) == "👎")
  
  #reaction, user = await bot.await_for("reaction_add",timeout = 10, check = checkEmoji)
#      reaction ,user = await bot.wait_for("reaction_add" ,check = checkEmoji)
#      if reaction.emoji == "👍": 
#        await ctx.channel.send("Très bien nous passons a la première question")
#      else:
 #       await ctx.channel.send("je savais que tu n'etais pas prêt ")

#Passage a la deuxieme question        
#      message_2=await ctx.channel.send("Dans une course si je depasse le deuxième je deviens ?")
#      await message_2.add_reaction("1️⃣")
#      await message_2.add_reaction("2️⃣")
      
#      def checkEmojis(reaction,user):
#        return  message_2.id == reaction.ctx.id and (str(reaction.emoji) == "1️⃣" or str(reaction.emoji) == "2️⃣")
  
  #reaction, user = await bot.await_for("reaction_add",timeout = 10, check = checkEmoji)
#      reaction ,user = await bot.wait_for("reaction_add" ,check = checkEmojis)
#      if reaction.emoji == "2️⃣": 
#        await ctx.channel.send("Très bien nous passons a la deuxieme question")
#      else:
#        await ctx.channel.send("mauvaise réponse ")




bot.run(DISCORD_TOKEN)