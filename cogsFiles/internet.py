import discord
from discord.ext import commands
import json
import os
import random
import praw
import asyncpraw
import requests
import urbandictionary as ud
reddit = asyncpraw.Reddit(client_id = "ThRqj2eADuklyyyKEXxaJQ",
                client_secret = "pqzyy-HKEYkU9g5_wXbMqhUQxyZ0FA",
                username = str(os.environ['username']),
                password = str(os.environ['password']),
                user_agent = "python"
                )



url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': str(os.environ['rapidAPIkey'])
    }


async def postReddit(sub, ctx):
        await ctx.send("Loading...")



        memePosts = []
        subredditMemes = await reddit.subreddit(sub)
        topMemes = subredditMemes.top(limit = 50)

        async for submission in topMemes:
    
            memePosts.append(submission)
        randomImage = random.choice(memePosts)

        extension = randomImage.url[len(randomImage.url) - 3 :].lower()
        
        while "jpg" != extension and "png" != extension and "gif" != extension:
            randomsub = random.choice(memePosts)
            extension = randomsub.url[len(randomsub.url) - 3 :].lower()
        name = randomImage.title
        url = randomImage.url

        e = discord.Embed(title=name)
        e.set_image(url=url)

        await ctx.reply(embed=e)
        
class internet(commands.Cog, description="Pull items from the internet!"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def urban(self, ctx, *searchItem):
        if searchItem != ():
            querystring = {"term":str(ctx.message.content)[7:]}
            r = requests.request("GET", url, headers=headers, params=querystring)
            r = r.json()
            try:
                embed=discord.Embed(title="Urban Dictionary", description=str(ctx.message.content)[7:], color=0xbb00ff)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                embed.add_field(name="Description", value=(r['list'][0]['definition']).replace("[", "").replace("]", ""), inline=False)
                embed.add_field(name="Examples", value=(r['list'][0]['example']).replace("[", "").replace("]", ""), inline=True)
                await ctx.send(embed=embed)
            except:
                await ctx.reply("Word/phrase not found!")

    @commands.command(brief="See something cute!", description="Pulls a cute image from r/animalpics!")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def animal(self, ctx):
        await postReddit("animalpics", ctx)
        


    @commands.command(brief="See a meme!", description="Pulls a meme from r/memes!")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def meme(self, ctx):
        await postReddit("memes", ctx)

    @commands.command(brief="See anime!", description="Pulls an image from r/animemes!")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def anime(self, ctx):
        await postReddit("Waifu", ctx)

def setup(client):
    client.add_cog(internet(client))