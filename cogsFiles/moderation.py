import time
import discord
from discord.ext import commands, tasks
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



class moderation(commands.Cog, description="Stuff"):
    def __init__(self, client):
        self.client = client
        self.printer.start()

    @tasks.loop(seconds=20.0)
    async def printer(self):

        mongo = MongoClient(os.environ['mongo'])
        db = mongo["accounts"]
        col = db["data"]
        col2 = db["counts"]
        import cogsFiles.currency as currency
        import cogsFiles.count as count
        print("Updating main database. DO NOT TERMINATE")
        col.drop()
        col2.drop()
        col.insert_one(currency.userJson)
        col2.insert_one(count.countJson)
        print("Update complete.")
        await asyncio.sleep(10)
        import cogsFiles.currency as currency
        import cogsFiles.count as count
        db = mongo["accounts_backup"]
        col = db["data"]
        col2 = db["counts"]
        print("Updating backup database. DO NOT TERMINATE")
        col.drop()
        col2.drop()
        col.insert_one(currency.userJson)
        col2.insert_one(count.countJson)
        print("Update complete.")
        
    @commands.command()
    async def forceUpdate(self, ctx):
        if ctx.author.id == 444254890563338241:
            mongo = MongoClient(os.environ['mongo'])
            db = mongo["accounts"]
            col = db["data"]
            col2 = db["counts"]
            import cogsFiles.currency as currency
            import cogsFiles.count as count
            print("Force updating main database. DO NOT TERMINATE")
            col.drop()
            col2.drop()
            col.insert_one(currency.userJson)
            col2.insert_one(count.countJson)
            print("Update complete.")
            await asyncio.sleep(10)
            import cogsFiles.currency as currency
            import cogsFiles.count as count
            db = mongo["accounts_backup"]
            col = db["data"]
            col2 = db["counts"]
            print("Force updating backup database. DO NOT TERMINATE")
            col.drop()
            col2.drop()
            col.insert_one(currency.userJson)
            col2.insert_one(count.countJson)
            print("Update complete.")

    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after ):
        if member.guild.id == 655133163344887820:
            if before.channel == None:
                channel = await self.client.fetch_channel("916495231275397190")
                embed=discord.Embed(title="Member joined voice channel", description=member.name+"#"+member.discriminator+ " joined #"+after.channel.name, color=0x00ff9d)
                embed.set_author(name=member.name+"#"+member.discriminator, icon_url=member.avatar)
                embed.set_footer(text="ID: "+str(member.id)+" - "+str(datetime.datetime.now()))
                await channel.send(embed=embed)     
            if after.channel == None:
                channel = await self.client.fetch_channel("916495231275397190")
                embed=discord.Embed(title="Member left voice channel", description=member.name+"#"+member.discriminator+ " left #"+before.channel.name, color=0xff0000)
                embed.set_author(name=member.name+"#"+member.discriminator, icon_url=member.avatar)
                embed.set_footer(text="ID: "+str(member.id)+" - "+str(datetime.datetime.now()))
                await channel.send(embed=embed)  

        elif member.guild.id == 899267202732142622:
            if before.channel == None:
                channel = await self.client.fetch_channel("926907860691079198")
                embed=discord.Embed(title="Member joined voice channel", description=member.name+"#"+member.discriminator+ " joined #"+after.channel.name, color=0x00ff9d)
                embed.set_author(name=member.name+"#"+member.discriminator, icon_url=member.avatar)
                embed.set_footer(text="ID: "+str(member.id)+" - "+str(datetime.datetime.now()))
                await channel.send(embed=embed)     
            if after.channel == None:
                channel = await self.client.fetch_channel("926907860691079198")
                embed=discord.Embed(title="Member left voice channel", description=member.name+"#"+member.discriminator+ " left #"+before.channel.name, color=0xff0000)
                embed.set_author(name=member.name+"#"+member.discriminator, icon_url=member.avatar)
                embed.set_footer(text="ID: "+str(member.id)+" - "+str(datetime.datetime.now()))
                await channel.send(embed=embed) 

        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(message.guild.id)
        if message.guild.id == 655133163344887820:
            
            channel = await self.client.fetch_channel("916495231275397190")
            embed=discord.Embed(title="Message deleted!", description="'"+message.content+ "' was deleted in #"+message.channel.name, color=0xff0000)
            embed.set_author(name=str(message.author.name)+"#"+str(message.author.discriminator), icon_url=message.author.avatar)
            embed.set_footer(text="ID: "+str(message.author.id)+" - "+str(datetime.datetime.now()))
            await channel.send(embed=embed)  
        elif message.guild.id == 899267202732142622:
            channel = await self.client.fetch_channel("926907860691079198")
            embed=discord.Embed(title="Message deleted!", description="'"+message.content+ "' was deleted in #"+message.channel.name, color=0xff0000)
            embed.set_author(name=str(message.author.name)+"#"+str(message.author.discriminator), icon_url=message.author.avatar)
            embed.set_footer(text="ID: "+str(message.author.id)+" - "+str(datetime.datetime.now()))
            await channel.send(embed=embed)  
    #@commands.command()
    #async def kick(self, ctx: commands.Context, user: discord.Member):
    #    await ctx.send(f'{user.mention} has been kicked from {user.voice.channel.mention}')
    #    await user.move_to(None)

    @commands.command(name='clear', brief='This command will clear messages!')
    async def clear(self, ctx, amount = 5):
        if ctx.author.id == 444254890563338241 or ctx.author.id == 354563683902554113:
            await ctx.channel.purge(limit=amount)
            await ctx.send("Deleted")
        else:
            ctx.reply("no")
    @commands.command(name='invite', brief='Get an invite link for the bot!')
    async def invite(self, ctx):
        embed = discord.Embed()
        embed.description = "Click [here](https://discord.com/oauth2/authorize?client_id=746076570632061040&permissions=1133584&scope=bot) to invite the bot!"
        await ctx.send(embed=embed)
    

def setup(client):
    client.add_cog(moderation(client))