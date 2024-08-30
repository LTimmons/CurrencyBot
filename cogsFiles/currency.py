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
from discord.ui import Button, View
from bson.json_util import dumps, loads
try:
    mongo = MongoClient(os.environ['mongo'])
    db = mongo["accounts"]
    col = db["data"]
    cursor = col.find()
    with open('jsonFile.json', 'w') as file:

        for document in cursor:

            file.write(dumps(document))

    with open('jsonFile.json') as json_file:
        userJson = json.load(json_file)
        del userJson["_id"]

except:
    mongo = MongoClient(os.environ['mongo'])
    db = mongo["accounts_backup"]
    col = db["data"]
    cursor = col.find()
    with open('jsonFile.json', 'w') as file:

        for document in cursor:

            file.write(dumps(document))

    with open('jsonFile.json') as json_file:
        userJson = json.load(json_file)
        del userJson["_id"]

os.remove('jsonFile.json')

items = [
    [
        "Fishing Rod", "rod", 10000, 3000, "Used to catch fish!", "🎣", True
    ],
    [
        "Common Fish", "cfish", "n/a", 1000, "Caught using the fishing rod!",
        "🐟", False
    ],
    [
        "Tropical Fish", "tfish", "n/a", 2500, "Caught using the fishing rod!",
        "🐠", False
    ],
    [
        "Metal Detector", "mtd", 50000, 6000, "Search for ancient coins and metal              scraps!", "<:mtd:915281515330551859>", True
    ],
    [
        "Ancient coin", "coin", "n/a", 150000, "An antique coin!", "🪙", False
    ],
    [
        "Metal Scraps", "mscr", "n/a", 150, "Nothing special really.", "🔩",
        False
    ],
    [
        "AK-47", "gun", 100000, 50000, "A gun that shoots people.", "🔫", True
    ]
]

locations = [["Chinese Embassy", "🇨🇳"], ["Tesco", "🛒"], ["The Bank", "🏦"],
             ["Luke's house", "🏠"], ["Heineken factory", "🍺"],
             ["Damo's shed", "🏚️"], ["Gabriel's calculator", "🧮"]]

passwords = [
    "I<3JustinBeiber", "minecraft4lyf", "1pl4yp0k3m0ng03v3ryd4y",
    "johny$ins!sMyDad", "InflatedNuts26", "CockoSaurus", "AmongUs4Lyf",
    "BabaGanoush96", "Password123", "ILoveMommy82", "CeilingWooden99"
]
emails = [
    "sMoistSockStore@gmail.com", "SmallNuts@gmail.com",
    "KissedUrMum@macdonalds.com", "eyBooBoo@yahoo.co.uk",
    "sSecretEmail@bananaduck.onion"
]
lastMessages = [
    "Wow, the banana duck is such a good bot",
    "have you seen how much money Mharc has... me neither!",
    "is it bad that I find beanbean hot?",
    "i have a severe case of crunchy toe juice....help"
]
my_secret = os.environ['TOKEN']


async def create_account(player):

    if str(player) in userJson:
        return
    else:
        userJson[str(player)] = {}
        userJson[str(player)]["balance"] = 0
        userJson[str(player)]["inventory"] = ""
        userJson[str(player)]["daily"] = str(
            datetime.datetime(2020, 5, 17).strftime("%Y-%m-%d"))
        userJson[str(player)]["lastAttempt"] = str(
            datetime.datetime(2020, 5, 17))
        userJson[str(player)]["lastRobbed"] = str(
            datetime.datetime(2020, 5, 17))
        userJson[str(player)]["currentRobStatus"] = "False"


async def addItem(player, item):
    await create_account(player)
    oldInv = await getInv(player)
    newInv = []
    found = False
    for items in oldInv:
        if items[1] == item:
            newInv.append([str(int(items[0]) + 1), items[1]])
            found = True
        else:
            newInv.append([items[0], items[1]])
    if found == False:
        newInv.append(["1", item])
    newInvString = ""

    for items in newInv:
        newInvString += items[0] + "." + items[1] + ","
    userJson[str(player)]["inventory"] = newInvString


async def writeTimeDaily(player, time):
    userJson[str(player)]["daily"] = str(time)


async def addThings():
    print("added")
    userJson["315572693942403073"]["currentRobStatus"] = "False"

async def readTimeDaily(player):
    if "daily" in userJson[str(player)]:
        time = userJson[str(player)]["daily"]
        time = datetime.datetime.strptime(time[:10], '%Y-%m-%d')
    else:
        time = datetime.datetime(2020, 5, 17).strftime("%Y-%m-%d")
        await writeTimeDaily(player, str(time))
    return time


async def readLastAttempt(player):
    if "lastAttempt" in userJson[str(player)]:
        time = userJson[str(player)]["lastAttempt"]
        time = datetime.datetime.strptime(time[:19], '%Y-%m-%d %H:%M:%S')
    else:
        time = datetime.datetime(2020, 5, 17)
        await writeTimeDaily(player, str(time))
    return time


async def readLastRobbed(player):
    if "lastRobbed" in userJson[str(player)]:
        time = userJson[str(player)]["lastRobbed"]
        time = datetime.datetime.strptime(time[:19], '%Y-%m-%d %H:%M:%S')
    else:
        time = datetime.datetime(2020, 5, 17)
        await writeTimeDaily(player, str(time))
    return time


async def readLastVC(player):
    time = userJson[str(player)]["lastJoinedVc"]
    time = datetime.datetime.strptime(time[:19], '%Y-%m-%d %H:%M:%S')

    return time


async def remItem(player, item):
    await create_account(player)
    oldInv = await getInv(player)
    newInv = []
    for items in oldInv:
        if items[1] == item:
            if items[0] != "1":
                newInv.append([str(int(items[0]) - 1), items[1]])
        else:
            newInv.append([items[0], items[1]])

    newInvString = ""

    for items in newInv:
        newInvString += items[0] + "." + items[1] + ","
    userJson[str(player)]["inventory"] = newInvString


async def getItemName(itemID):
    for item in items:
        if item[1] == itemID:
            return item[0]


async def getItemDesc(itemID):
    for item in items:
        if item[1] == itemID:
            return item[4]


async def sellPrice(itemID):
    for item in items:
        if item[1] == itemID:
            return item[3]


async def sort_by_key(list):
    return list['balance']


async def getItemEmoji(itemID):
    for item in items:
        if item[1] == itemID:
            return item[5]


async def addMoney(player, money):

    oldMoney = userJson[str(player)]["balance"]
    newMoney = int(money) + oldMoney
    userJson[str(player)]["balance"] = newMoney


async def getInv(player):
    inv = userJson[str(player)]["inventory"]
    splitInv = inv.split(",")
    invArray = []
    for i in splitInv:
        i2 = i.split(".")
        invArray.append(i2)

    invArray.remove([''])
    return invArray


async def getBal(id):
    return int(userJson[str(id)]["balance"])


class Currency(commands.Cog,
               description="A currency system based on your activity!"):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Sell your items!",
                      description="Sell inventory items for money!")
    async def sell(self, ctx, *itemArr):
        sold = True
        try:
            item = itemArr[0]
            count = itemArr[1]
        except:
            await ctx.reply(
                "Please use the correct format: .sell [item] [amount]")
            sold = False
        playerInv = await getInv(ctx.author.id)

        if itemArr == ():
            if sold == True:
                await ctx.reply("What are you trying to sell?")
            sold = False
        countItem = 0
        for items in playerInv:

            if items[1] == item:
                countItem = int(items[0])

        if countItem < int(count) or int(count) < 0:
            if sold == True:
                await ctx.reply("You don't have that many!")
            sold = False

        if sold == True:
            for i in range(int(count)):

                await remItem(ctx.author.id, item)
                await addMoney(ctx.author.id, await sellPrice(item))

            await ctx.reply("You sold your " + count + " " +
                            await getItemName(item) + " for " +
                            str(await sellPrice(item) * int(count)) + "!")

    @commands.command(brief="Get a daily money booster!",
                      description="50,000 every 24 hours!")
    async def daily(self, ctx):
        await addThings()
        lastDaily = str(await readTimeDaily(ctx.author.id))
        currentTime = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        lastDaily = lastDaily[:10]

        if lastDaily != currentTime:
            if datetime.datetime.now().strftime(
                    "%Y-%m-%d") == datetime.datetime(2021, 12,
                                                     25).strftime("%Y-%m-%d"):
                await ctx.reply(
                    "Since its Christmas you just collected 300,000!")
                await addMoney(ctx.author.id, 300000)
                await writeTimeDaily(
                    ctx.author.id,
                    datetime.datetime.now().strftime("%Y-%m-%d"))
            else:
                await ctx.reply("You just collected 50,000!")
                await addMoney(ctx.author.id, 50000)
                await writeTimeDaily(
                    ctx.author.id,
                    datetime.datetime.now().strftime("%Y-%m-%d"))
        else:
            await ctx.reply("Please wait until tomorrow!")

    @commands.command(
        aliases=['bal'],
        brief="Check your account balance!",
        description=
        "Use .balance <user> to check your own, or somebody elses balance!")
    async def balance(self, ctx, *user: str):
        users = userJson
        if user == ():
            user = ctx.author.id
        else:
            user = str(user[0])

        if str(user) not in users:
            user = user.strip('<')
            user = user.strip('>')
            user = user.strip('@')
            user = user.strip('!')
        if str(user) not in users:
            user = ctx.author.id

        if str(user) not in users:
            user = ctx.author.id

        await create_account(user)
        users = userJson

        member = await self.client.fetch_user(user)

        embed = discord.Embed(title="Balance",
                              description="You have " +
                              format(users[str(user)]["balance"], ',d') +
                              " banana chips!",
                              color=0x00ffee)
        embed.set_author(name=member.name)
        embed.set_thumbnail(url=member.avatar).set_footer(text="wow ur rich")
        await ctx.reply(embed=embed)

    @commands.command(
        aliases=['cf'],
        brief="Gamble your money!",
        description="Have a 50/50 chance of doubling or loosing your gamble!")
    async def coinflip(self, ctx, *amount):
        coinsGambled = amount[0]
        gamble = True
        users = userJson
        if amount == ():
            await ctx.reply("How much are we talking???")

        else:
            bal = int(users[str(ctx.author.id)]["balance"])

            if coinsGambled == "max" or coinsGambled == "all":

                coinsGambled = str(bal)

            if int(coinsGambled) > bal:
                await ctx.reply("You don't have that much!")
                gamble = False
            if int(coinsGambled) < 0:
                await ctx.reply("You cant gamble negative money!")
                gamble = False
            if int(coinsGambled) > 40000:
                await ctx.reply(
                    "You cant gamble more than 40,000. This is to allow the economy to grow!"
                )
                gamble = False
            if gamble == True:
                win = random.randint(0, 1)
                if win == 1:
                    embed = discord.Embed(color=0x00ff40)
                    embed.add_field(name="You won!",
                                    value="You won " + coinsGambled + "!",
                                    inline=False)
                    await ctx.send(embed=embed)
                    await addMoney(ctx.author.id, int(coinsGambled))
                if win == 0:
                    embed = discord.Embed(color=0xff0000)
                    embed.add_field(name="You lost!",
                                    value="You lost " + coinsGambled + "!",
                                    inline=False)
                    await ctx.send(embed=embed)
                    await addMoney(ctx.author.id, -(int(coinsGambled)))

    @commands.command(brief="Hack a user and steal some money!",
                      description="Rob a user and expose their login details!")
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def hack(self, ctx, *userTarget):

        users = userJson

        target = userTarget[0]
        target = target.strip('<')
        target = target.strip('>')
        target = target.strip('@')
        target = target.strip('!')

        if target in users and target != str(ctx.author.id):
            checker = userJson[target]["currentRobStatus"]
            userJson[target]["currentRobStatus"] = "True"

            lastAttemptMins = (datetime.datetime.now() - await
                               readLastAttempt(target)).total_seconds() / 60.0
            lastRobbedMins = (datetime.datetime.now() - await
                              readLastRobbed(target)).total_seconds() / 60.0
            if checker == "True":
                await ctx.reply("This user is being robbed elsewhere buddy.")
                self.hack.reset_cooldown(ctx)
            elif lastAttemptMins < 5:
                await ctx.reply(
                    "Somebody already tried to hack this user so they activated their firewall. Try again in 5 minutes."
                )
                self.hack.reset_cooldown(ctx)
            elif lastRobbedMins < 30:
                await ctx.reply(
                    "This user has been robbed in the last 30 minutes so their security is very tight. You have no chance."
                )
                self.hack.reset_cooldown(ctx)
            else:
                chance = random.randint(1, 100)
                rob = False

                member = await self.client.fetch_user(int(target))

                message = await ctx.reply("Hacking " + member.name + " now...")
                await asyncio.sleep(1)
                await message.edit(content="Brute forcing 2fa...")
                await asyncio.sleep(1)
                await message.edit(content="Logging into account...")
                await asyncio.sleep(1)
                await message.edit(content="Email: `" + member.name +
                                   random.choice(emails) + "`")
                await asyncio.sleep(1)
                await message.edit(content="Password: `" +
                                   random.choice(passwords) + "`")
                await asyncio.sleep(1)

                await message.edit(content="Last DM: '" +
                                   random.choice(lastMessages) + "'")
                await asyncio.sleep(2)
                await message.edit(content="Breaching their wallet now...")
                await asyncio.sleep(2)
                targetBal = int(await getBal(int(target)))
                if await getBal(ctx.author.id) >= targetBal:
                    if chance <= 35:
                        rob = True
                else:
                    if chance <= 15:
                        rob = True

                if rob == True:
                    chanceBigSteal = random.randint(1, 100)
                    if chanceBigSteal < 21:
                        stealPerc = random.randint(35, 40)
                    else:
                        stealPerc = random.randint(15, 35)

                    stealAmount = round(targetBal * stealPerc * 0.01)
                    await addMoney(ctx.author.id, stealAmount)
                    await addMoney(int(target), -stealAmount)

                    await message.edit(content="You stole " +
                                       str(stealAmount) + "!")
                    embed = discord.Embed(color=0x2b00ff)
                    embed.set_thumbnail(url=ctx.author.avatar)
                    embed.add_field(name="You got robbed!",
                                    value="You lost " + str(stealAmount) + "!",
                                    inline=False)
                    embed.set_footer(text="Robbed by " + ctx.author.name)
                    userJson[target]["lastRobbed"] = str(
                        datetime.datetime.now())

                    await member.send(embed=embed)

                else:
                    await message.edit(content="You stole nothing!!")
                    userJson[target]["lastAttempt"] = str(
                        datetime.datetime.now())

        else:
            await ctx.reply("Who even is that?")
            self.hack.reset_cooldown(ctx)

        userJson[target]["currentRobStatus"] = "False"

    @commands.command(aliases=['sfh'])
    async def sendFakeHack(self, ctx, target, amount="1345321"):
        if ctx.author.id == 444254890563338241 or ctx.author.id == 248831543684890625:
            target = target.strip('<')
            target = target.strip('>')
            target = target.strip('@')
            target = target.strip('!')

            member = await self.client.fetch_user(int(target))
            embed = discord.Embed(color=0x2b00ff)
            embed.set_thumbnail(url=ctx.author.avatar)
            embed.add_field(name="You got robbed!",
                            value="You lost " + amount + "!",
                            inline=False)
            embed.set_footer(text="Robbed by " + ctx.author.name)

            await member.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def heist(self, ctx):

        await create_account(ctx.author.id)
        inventory = await getInv(ctx.author.id)
        gun = False
        for i in inventory:
            if i[1] == "gun":
                gun = True

        if gun == True:

            buttonT = random.choice(locations)
            button = Button(label=buttonT[0],
                            style=discord.ButtonStyle.green,
                            emoji=buttonT[1])

            button1T = random.choice(locations)
            while button1T == buttonT:
                button1T = random.choice(locations)
            button1 = Button(label=button1T[0],
                             style=discord.ButtonStyle.green,
                             emoji=button1T[1])
            button2T = random.choice(locations)
            while button2T == buttonT or button2T == button1T:
                button2T = random.choice(locations)
            button2 = Button(label=button2T[0],
                             style=discord.ButtonStyle.green,
                             emoji=button2T[1])

            async def button_callback(interaction):
                if interaction.user != ctx.author:
                    await interaction.response.send_message(
                        content="This isn't for you!", ephemeral=True)
                else:
                    failchance = random.randint(0, 100)
                    if failchance < 10:
                        await interaction.response.edit_message(
                            content=
                            "You got caught by the police and lost 50,000!",
                            view=None)
                        await addMoney(ctx.author.id, -50000)
                    else:
                        robAmount = random.randint(20000, 60000)
                        await interaction.response.edit_message(
                            content="You robbed " + buttonT[0] +
                            " and stole £" + str(robAmount) + "!",
                            view=None)
                        await addMoney(ctx.author.id, robAmount)

            async def button_callback1(interaction):
                if interaction.user != ctx.author:
                    await interaction.response.send_message(
                        content="This isn't for you!", ephemeral=True)
                else:
                    failchance = random.randint(0, 100)
                    if failchance < 10:
                        await interaction.response.edit_message(
                            content=
                            "You got caught by the police and lost 50,000!",
                            view=None)
                        await addMoney(ctx.author.id, -50000)
                    else:
                        robAmount = random.randint(20000, 60000)
                        await interaction.response.edit_message(
                            content="You robbed " + button1T[0] +
                            " and stole £" + str(robAmount) + "!",
                            view=None)
                        await addMoney(ctx.author.id, robAmount)

            async def button_callback2(interaction):

                if interaction.user != ctx.author:
                    await interaction.response.send_message(
                        content="This isn't for you!", ephemeral=True)
                else:
                    failchance = random.randint(0, 100)
                    if failchance < 10:
                        await interaction.response.edit_message(
                            content=
                            "You got caught by the police and lost 50,000!",
                            view=None)
                        await addMoney(ctx.author.id, -50000)
                    else:
                        robAmount = random.randint(20000, 60000)
                        await interaction.response.edit_message(
                            content="You robbed " + button2T[0] +
                            " and stole £" + str(robAmount) + "!",
                            view=None)
                        await addMoney(ctx.author.id, robAmount)

            button.callback = button_callback
            button1.callback = button_callback1
            button2.callback = button_callback2
            view = View()
            view.add_item(button)
            view.add_item(button1)
            view.add_item(button2)

            await ctx.send("Where do you want to rob?", view=view)

        else:
            await ctx.send("Buy a gun first lol.")
            self.heist.reset_cooldown(ctx)

    @commands.command(bried="Share some banana chips",
                      description="Give another player some money!")
    async def give(self, ctx, target, amount):
        await create_account(ctx.author.id)
        balance = await getBal(ctx.author.id)
        target = target.strip('<')
        target = target.strip('>')
        target = target.strip('@')
        target = target.strip('!')
        if target in userJson:
            if amount.isdecimal() and int(amount) > 0:
                if int(amount) <= int(balance):
                    await addMoney(target, int(amount))
                    await addMoney(ctx.author.id, -int(amount))
                    await ctx.reply("Transaction completed!")
                else:
                    await ctx.reply("You don't have that much!")
            else:
                await ctx.reply("That's not a valid number!")

        else:
            await ctx.reply("Who even is that?")

    @commands.command(brief="Beg for some extra change!",
                      description="A chance to gain 50-600 coins! ")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await create_account(ctx.author.id)
        money = random.randint(50, 600)
        await ctx.reply("The Banana Duck was mercyful and granted you " +
                        str(money) + " banana chips!")
        await addMoney(ctx.author.id, money)

    @commands.command(brief="View the shop!",
                      description="A list of purchasable items!")
    async def shop(self, ctx, *item):
        await create_account(ctx.author.id)
        if item == ():
            embed = discord.Embed(title="Shop")

            for i in items:
                if i[6] == True:

                    embed.add_field(name=i[5] + " " + i[0] + " - £" +
                                    format(i[2], ',d') + " ```" + i[1] + "```",
                                    value=str(i[4]),
                                    inline=False)

            await ctx.reply(embed=embed)

        else:
            for i in items:
                if item[0] == i[1]:
                    embed = discord.Embed(title="Shop")
                    if str(i[2]) == "n/a":
                        embed.add_field(name=i[0] + " - " + str(i[4]),
                                        value="Buy: " + str(i[2]) +
                                        " \nSell: £" + str(i[3]),
                                        inline=False)
                    else:
                        embed.add_field(name=i[0] + " - " + str(i[4]),
                                        value="Buy: £" + str(i[2]) +
                                        " \nSell: £" + str(i[3]),
                                        inline=False)
                    await ctx.reply(embed=embed)

    @commands.command(
        aliases=['lb', 'global'],
        brief="View the richest players globally!",
        description="A list of the 5 richest players in my JSON file!")
    async def leaderboard(self, ctx):
        users = userJson
        try:
            del users["_id"]
        except:
            return

        peopleArray = []
        for people in users:

            peopleArray.append([people, users[str(people)]["balance"]])

        peopleArray.sort(key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="Leaderboard")
        embed.set_author(name=(ctx.message.author.name))
        for i in range(5):
            member = await self.client.fetch_user(int(peopleArray[i][0]))

            embed.add_field(name=str(i + 1) + ": " + member.name,
                            value=peopleArray[i][1],
                            inline=False)

        await ctx.reply(embed=embed)

    @commands.command(brief="For admins!", aliases=["gm"], hidden=True)
    async def givemoney(self, ctx, *data):
        if ctx.author.id != 444254890563338241:
            await ctx.reply("lol no")
        elif ctx.author.name == "lukes kitten":
            await ctx.reply("you really thought...")
        else:
            user = data[0]
            money = data[1]
            user = user.strip('<')
            user = user.strip('>')
            user = user.strip('@')
            user = user.strip('!')
            await addMoney(user, int(money))
            await ctx.reply("Added!")

    @commands.command(brief="Buy items from the shop!",
                      description="Buy items with your precious money!")
    async def buy(self, ctx, *data):
        
        await create_account(ctx.author.id)
        sold = False
        for i in items:
            if i[1] == data[0] and i[6] == True and sold == False:
                sold = True
                users = userJson
                bal = users[str(ctx.author.id)]["balance"]
                if bal < i[2]:
                    await ctx.reply("You're a bit short on money there mate!")
                else:
                    await addMoney(ctx.author.id, -i[2])
                    await addItem(ctx.author.id, data[0])
                    await ctx.reply("You bought a " +
                                    await getItemName(data[0]) + "!")

        if sold == False:
            await ctx.reply("Invalid product code!")

    @commands.command(aliases=['inv', 'i'],
                      brief="View your inventory!",
                      description="A list of the items in your inventory!")
    async def inventory(self, ctx):
        await create_account(ctx.author.id)
        embed = discord.Embed(title="Inventory")
        embed.set_author(name=(ctx.message.author.name + "'s inventory"),
                         icon_url=ctx.message.author.avatar)
        inventory = await getInv(ctx.author.id)
        for i in inventory:

            embed.add_field(name=await getItemEmoji(i[1]) + " " +
                            await getItemName(i[1]) + " x" + str(i[0]) +
                            " ```" + str(i[1]) + "```",
                            value=await getItemDesc(i[1]),
                            inline=False)

        await ctx.reply(embed=embed)

    @commands.command(aliases=['f'],
                      brief="Go fishing!",
                      description="Catch some fish by using a fishing rod!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(self, ctx):
        await create_account(ctx.author.id)
        inventory = await getInv(ctx.author.id)
        rod = False
        for i in inventory:
            if i[1] == "rod":
                rod = True

        if rod == True:
            cfishCount = random.randint(1, 3)
            tfishCount = random.randint(0, 1)
            for i in range(cfishCount):
                await addItem(ctx.author.id, "cfish")
            for i in range(tfishCount):
                await addItem(ctx.author.id, "tfish")
            await ctx.reply("You won " + str(cfishCount) +
                            " common fishies, and " + str(tfishCount) +
                            " tropical fishies!")
        else:
            await ctx.reply("Buy a rod u mong!")
            self.fish.reset_cooldown(ctx)

    @commands.command(aliases=['s'],
                      brief="Go metal detecting!",
                      description="You might find something lucky!")
    @commands.cooldown(1, 45, commands.BucketType.user)
    async def search(self, ctx):
        await create_account(ctx.author.id)
        inventory = await getInv(ctx.author.id)
        mtd = False
        for i in inventory:
            if i[1] == "mtd":
                mtd = True

        if mtd == True:
            scraps = random.randint(10, 30)
            coinChance = random.randint(0, 100)
            if coinChance < 8:
                for i in range(scraps):
                    await addItem(ctx.author.id, "mscr")
                await addItem(ctx.author.id, "acoin")
                await ctx.reply(
                    "You found " + str(scraps) +
                    " metal scraps. BUT YOU ALSO FOUND AN ANCIENT COIN!!!")

            else:

                for i in range(scraps):
                    await addItem(ctx.author.id, "mscr")

                await ctx.reply("You found " + str(scraps) + " metal scraps")

        else:
            await ctx.reply("Buy a metal detector u mong!")
            self.search.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"{round(error.retry_after, 2)} seconds left")
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot: return
        await create_account(message.author.id)
        try:
            if message.content[0] != ".":
                await addMoney(message.author.id, 100)
        except:
            await addMoney(message.author.id, 100)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == None:
            await create_account(member.id)
            userJson[str(member.id)]["lastJoinedVc"] = str(
                datetime.datetime.now())

        if after.channel == None or after.channel.id == 924110614324981760:
            if before.channel.id != 924110614324981760:
                mins = (datetime.datetime.now() -
                        await readLastVC(member.id)).total_seconds() / 60.0

                moneyToAdd = int(1500 * mins)

                await addMoney(member.id, moneyToAdd)
                print(moneyToAdd)


def setup(client):
    client.add_cog(Currency(client))
