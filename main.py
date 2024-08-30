import discord
from discord.ext import commands
import os
import keep_alive
import json
import pymongo
import settings
from pymongo import MongoClient

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=settings.Prefix, intents=intents)


@client.event
async def on_ready():

    print("Bot is ready!")
    
    await client.change_presence(status=discord.Status.online, activity=discord.Game(settings.BotStatus))
    

for filename in os.listdir("./cogsFiles"):
    if filename.endswith(".py"):
        client.load_extension(f'cogsFiles.{filename[:-3]}')

keep_alive.keep_alive()

client.run(settings.TOKEN)