import discord
from discord.ext import commands
import json
import os
import random
from discord.utils import get
import asyncio

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Brandon!", description="chad")
    async def brandon(self, ctx):
        await ctx.reply("https://tenor.com/view/gigagigagiga-giga-chad-based-gif-22621614")

    @commands.command(brief="Viviana!", description="Kurwa!",aliases = ["vivi"])
    async def viviana(self, ctx):
        await ctx.reply("https://cdn.discordapp.com/attachments/782027622897025055/913908782571085854/B52FDA0F-86E9-46FC-A7F5-D04DB48D79F1.jpg")

    @commands.command(brief="Damian!", description="Kurwa!")
    async def damo(self, ctx):
        await ctx.reply("""Spierdajal bo spie!
The Government of Poland takes place in the framework of a unitary parliamentary representative democratic republic, whereby the President is the head of state and the Prime Minister is the head of government.[1][2] However, its form of government has also been identified as semi-presidential.[3][4][5][6]

Executive power is exercised, within the framework of a multi-party system, by the President and the Government, which consists of the Council of Ministers led by the Prime Minister. Its members are typically chosen from the majority party or coalition, in the lower house of parliament (the Sejm), although exceptions to this rule are not uncommon. The government is formally announced by the President, and must pass a motion of confidence in the Sejm within two weeks.

Legislative power is vested in the two chambers of parliament, Sejm and Senate. Members of Sejm are elected by proportional representation, with the proviso that non-ethnic-minority parties must gain at least 5% of the national vote to enter the lower house. Currently five parties are represented. Parliamentary elections occur at least every four years.""")

    @commands.command(brief="Make me dm somebody!", description="Make me send a direct message to another user!")
    async def dm(self, ctx, *data):
        user0 = data[0]
        user = user0.strip('<')
        user = user.strip('>')
        user = user.strip('@')
        user = user.strip('!')

        message = ""
        for i in data:
            if user0 != i:
                message += i + " "
        try:
            user = await self.client.fetch_user(int(user))
            embed=discord.Embed(color=0x8000ff)
            embed.set_thumbnail(url=ctx.author.avatar)
            embed.add_field(name="New Message!", value=message, inline=False)
            embed.set_footer(text="From " + ctx.author.name)

            await user.send(embed=embed) 

            await ctx.reply("Sent!")
        except:
            await ctx.reply("User not found! Try .dm [user] [message]")
                
            

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel != None:
            id = int(after.channel.id)
            if id == 913913053035249664:
                channel = await self.client.fetch_channel(913910964691296256)

                await member.move_to(channel)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 655133163344887820:
            channel = await self.client.fetch_channel("692816936899313705")
            await channel.send("Hey <@!"+str(member.id)+">, welcome to Banana Duck 🎉🤗 !")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 655133163344887820:
            channel = await self.client.fetch_channel("692816936899313705")
            await channel.send(str(member.name)+ " just left the server 🙁")



def setup(client):
    client.add_cog(Fun(client))
    