import time
import discord
from discord.ext import commands
import json, operator
import os
import random
import numpy as np
import datetime
import asyncio
import settings
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads
try:
    mongo = MongoClient(os.environ['mongo'])
    db = mongo["accounts"]
    col = db["counts"]
    cursor = col.find()
    with open('jsonFileCounts.json', 'w') as file:
            
        for document in cursor:
            file.write(dumps(document))
                
    with open('jsonFileCounts.json') as json_file:
        countJson = json.load(json_file)
        del countJson["_id"]
except:
    mongo = MongoClient(os.environ['mongo'])
    db = mongo["accounts_backup"]
    col = db["counts"]
    cursor = col.find()
    with open('jsonFileCounts.json', 'w') as file:
            
        for document in cursor:
            file.write(dumps(document))
                
    with open('jsonFileCounts.json') as json_file:
        countJson = json.load(json_file)
        del countJson["_id"]


os.remove('jsonFileCounts.json')

class count(commands.Cog, description="Yes"):
    def __init__(self, client):
        self.client = client
        
    @commands.command(brief="Start a counter in your channel!", description="See how high your members can count!")
    async def startCount(self, ctx):
        if str(ctx.guild.id) in countJson:
            await ctx.reply("You already have a counter in this server!")
            return 
        else:
            await ctx.reply("Count started!")
            await ctx.send("0")
            countJson[str(ctx.guild.id)] = {}
            countJson[str(ctx.guild.id)]["channel"] = ctx.channel.id
            countJson[str(ctx.guild.id)]["count"] = 1
            countJson[str(ctx.guild.id)]["lastUser"] = "3798753498743598"
            countJson[str(ctx.guild.id)]["servername"] = ctx.guild.name

        print(countJson)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot: return
        if message.content.isdecimal() and message.channel.id == countJson[str(message.guild.id)]["channel"]:
            

            if str(countJson[str(message.guild.id)]["count"]) == str(message.content) and str(countJson[str(message.guild.id)]["lastUser"]) != str(message.author.id):
                await message.add_reaction("🍎")
                countJson[str(message.guild.id)]["count"] +=1
                countJson[str(message.guild.id)]["lastUser"] = str(message.author.id)
                
            else:
                channel = await self.client.fetch_channel(countJson[str(message.guild.id)]["channel"])
                await channel.send("COUNT FAILED HAHAHAHA! GO BACK AND START AT 1!!")
                print(message.author.name + " failed count at "+str(countJson[str(message.guild.id)]["count"]))
                countJson[str(message.guild.id)]["count"] = 1
                countJson[str(message.guild.id)]["lastUser"] = "0"



def setup(client):
    client.add_cog(count(client))