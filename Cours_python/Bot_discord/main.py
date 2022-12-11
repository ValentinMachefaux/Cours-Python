import discord
import asyncio
import youtube_dl
import os
from dotenv import load_dotenv
import json
import random
from discord.ext import commands
from discord.ui import View,Button
from discord.reaction import Reaction


# Charge le fichier .env qui est dans le meme dossier
load_dotenv()

# Recup le token discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# creation d'un nouvel objet bot avec un prefix
bot = commands.Bot(case_insensitive=True,intents=discord.Intents.all())

embed = discord.Embed
voice_clients = {}
yt_opt={'format':'bestaudio/best'}
yt=youtube_dl.YoutubeDL(yt_opt)
ffmpeg_opts= {'options':'-vn'}

class Qcm():
  def __init__(self,id_question,question):
    super().__init__()
    self.id_question = id_question
    self.question=question
    self.embed = discord.Embed(title=f"Question numéro : {id_question}",color=0x763374)
    self.embed.add_field(name=f"\u200b",value=f"{question}",inline=True)
  def to_dict(self):
    return self.embed.to_dict()


@bot.event
async def on_ready():
  print("The bot is ready")


@bot.event
async def on_message(message):
  if message.content.startswith("!play"):
    #on cree un tru catch pour verif si la personne a mis un espace ou non durant la commande
    try:
      url = message.content.split()[1]
      #recup le canal connecté
      voice_client = await message.author.voice.channel.connect()
      voice_clients[voice_client.guild.id] = voice_client

      loop = asyncio.get_event_loop()
      data = await loop.run_in_executor(None,lambda:yt.extract_info(url,download=False))
      #met l'url dans la list data
      music = data['url']
      player = discord.FFmpegPCMAudio(music,**ffmpeg_opts)
      voice_client.play(player)
    except Exception as err:
      print(err)

    
  if message.content.startswith("!quizz"):
    with open('Bot_discord/questions.json','r',encoding="utf8") as f:
      data = json.loads(f.read())
      data_dic = data["quizz"]
    score = 0
    for i in range(5):

      ran = random.randint(0,29)
      embed= Qcm(data_dic[i]["id"],data_dic[ran]["question"])
      view= View()

      for o in data_dic[ran]["propositions"]:

        btn = Button(label=o,style=discord.ButtonStyle.primary,custom_id=o)
        view.add_item(btn)

        async def btn_callback(interaction):
          await interaction.response.defer()
        btn.callback = btn_callback

      await message.channel.send(embed=embed)
      await message.channel.send(view=view)


      reaction = await bot.wait_for("interaction",timeout=8000)
      if reaction.custom_id == data_dic[ran]["reponse"]:
        score= score+1
        await message.channel.send("Bravo mais saviez-vous que ?\n")
        await message.channel.send(data_dic[ran]["anecdote"])
      else:
        score = score-0.5
        await message.channel.send("Raté, vous perdez 0.5 point")

      if message.content=="indice":
        print(data_dic[ran]["indice"])
    await message.channel.send(embed=discord.Embed(title="Fin du quizz",description="Votre score est de :{score}"))











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