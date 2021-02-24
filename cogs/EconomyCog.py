import discord, json, random, asyncio
import mysql.connector as mysql
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown, guild_only
global hour
hour = 60**2

#----------------------------------------------------------------------------------

async def get_bank_data():
    with open("./data/mainbank.json", 'r', encoding="utf-8") as f:
        users = json.load(f)
    return users


async def open_account(user_id):
    try:
        tempdb = mysql.connect(
            host = "localhost",
            database = "SwitchBot",
            user = "",
            password = ""
        )
        tempcur = tempdb.cursor()

        users = []
        tempcur.execute("SELECT `client_id` FROM `Economy`;")
        for user in tempcur:
            users.append(user[0])
        if str(user_id) in users:
            tempcur.close()
            tempdb.close()
            return False
        else:
            tempcur.execute(f"INSERT INTO `Economy` VALUES ('{str(user_id)}', 69, 420)")
            tempdb.commit()
            tempcur.close()
            tempdb.close()
            return True
    except:
        users = await get_bank_data()

        if str(user_id) in users:
            return False
        else:
            users[str(user_id)] = {}
            users[str(user_id)]["wallet"] = 69
            users[str(user_id)]["bank"] = 420

        with open("./data/mainbank.json", 'w', encoding="utf-8") as f:
            json.dump(users, f)
    return True

async def update_bank(user_id, change = 0, mode = "wallet"):
    try:
        tempdb = mysql.connect(
            host = "localhost",
            database = "SwitchBot",
            user = "",
            password = ""
        )
        tempcur = tempdb.cursor()

        tempcur.execute(f"UPDATE `Economy` SET {mode} = {mode} + {change} WHERE client_id = '{str(user_id)}';")
        tempdb.commit()

        tempcur.execute(f"SELECT `wallet`, `bank` WHERE client_id = '{str(user_id)}';")

        for entry in tempcur:
            ballet, wank = entry[0], entry[1]
        tempcur.close()
        tempdb.close()

        bal = ballet, wank
        return bal

    except Exception as e:
        print(e)
        users = await get_bank_data()

        users[str(user_id)][mode] += change

        with open("./data/mainbank.json", 'w', encoding="utf-8") as f:
            json.dump(users, f)
        bal = users[str(user_id)]["wallet"], users[str(user_id)]["bank"]
        return bal
#---------------------------------------------------------------------------------------------------------------------------

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @guild_only()
    async def economy(self, ctx):
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="economy menu (but for mobile)", description="anything related to money!",color=discord.Colour.blue())
            embed.add_field(name="1️⃣balance {optional pinging someone}", value="**check your balance**")
            embed.add_field(name="2️⃣give", value="**give snips to your friends!**")
            embed.add_field(name="3️⃣withdraw", value="**withdraw any money from the bank**")
            embed.add_field(name="4️⃣deposit", value="**put any money into the bank**")
            embed.add_field(name="5️⃣beg", value="**when you're too poor you can get beg for some money**")
            embed.add_field(name="6️⃣gambling", value="**if you want to gamble your life away, you can do it here!**")
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="economy menu", description="anything related to money!",color=discord.Colour.blue())
        embed.add_field(name="balance {optional pinging someone}", value="`check your balance`")
        embed.add_field(name="give", value="`give snips to your friends!`")
        embed.add_field(name="withdraw", value="`withdraw any money from the bank`")
        embed.add_field(name="deposit", value="`put any money into the bank`")
        embed.add_field(name="beg", value="`when you're too poor you can get beg for some money`")
        embed.add_field(name="gambling", value="`if you want to gamble your life away, you can do it here!`")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=("bal", "wallet", "mon", "money", "monz", "cash", "dough", "moolah", "monies", "monie"))
    @guild_only()
    async def balance(self, ctx, member : discord.Member = None):
        try:
            #init
            db = mysql.connect(
                host = "localhost",
                database = "SwitchBot",
                user = "",
                password = ""
            )
            cursor = db.cursor()

            #making sure that person is put into the db
            persconfirm = False
            cursor.execute("SELECT `client_id` FROM `Economy`;")
            for pers in cursor:
                if pers[0] != str(ctx.message.author.id):
                    pass
                else:
                    persconfirm = True
            if persconfirm == False:
                await open_account(ctx.message.author.id)

            #main code

            if member == None:
                cursor.execute(f"SELECT wallet, bank FROM `Economy` WHERE client_id = '{str(ctx.message.author.id)}';")
                for i in cursor:
                    wallet_amt, bank_amt = i[0], i[1]
            else:
                cursor.execute(f"SELECT wallet, bank FROM `Economy` WHERE client_id = '{str(member.id)}';")
                for i in cursor:
                    wallet_amt, bank_amt = i[0], i[1]
            if member == None:
                embed = discord.Embed(title=f"{ctx.message.author.name}'s amount of snips", color=discord.Colour.green())
            else:
                embed = discord.Embed(title=f"{member.name}'s amount of snips", color=discord.Colour.green())

            embed.add_field(name="in wallet", value=wallet_amt)
            embed.add_field(name="in bank", value=bank_amt)
            embed.set_footer(text = f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            cursor.close()
            db.close()

        except:
            if member == None:
                await open_account(ctx.message.author.id)
            else:
                try:
                    await open_account(member.id)
                except:
                    await ctx.send(f"{ctx.message.author.mention}, it seems that I'm not able to retrieve this person")
                    return

            users = await get_bank_data()

            if member == None:
                wallet_amt = users[str(ctx.message.author.id)]["wallet"]
                bank_amt = users[str(ctx.message.author.id)]["bank"]
            else:
                wallet_amt = users[str(member.id)]["wallet"]
                bank_amt = users[str(member.id)]["bank"]
            if member == None:
                embed = discord.Embed(title=f"{ctx.message.author.name}'s amount of snips", color=discord.Colour.green())
            else:
                embed = discord.Embed(title=f"{member.name}'s amount of snips", color=discord.Colour.green())

            embed.add_field(name="in wallet", value=wallet_amt)
            embed.add_field(name="in bank", value=bank_amt)
            embed.set_footer(text = f"Command by {ctx.message.author.name} (backup database)", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        return

    @commands.command()
    @guild_only()
    async def withdraw(self, ctx, amount = 0):
        await open_account(ctx.message.author.id)

        bal = await update_bank(ctx.message.author.id)

        amount = int(amount)
        if amount == 0:
            msg = await ctx.send("You withdrew 0 snips!")
            await asyncio.sleep(4.1)
            await msg.edit(content="You're actually an idiot trying to withdraw nothing. Really just super stupid <:kek:746957664961036338>")
            return
        if amount == 0:
            await ctx.send('you must input an amount to withdraw')
            return
        if amount > bal[1]:
            await ctx.send("sorry, but you don't have enough money")
            return
        if amount<0:
            await ctx.send("did you just..try to withdraw less than nothing?")
            return

        await update_bank(ctx.message.author.id, amount)
        await update_bank(ctx.message.author.id, -1*amount, "bank")

        await ctx.send(f"you withdrew {amount} of snips!")
        return

    @commands.command(aliases=("dep", "Deposit", "Dep"))
    @guild_only()
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.message.author.id)
        #Thanks Riptyde for this idea
        bal = await update_bank(ctx.message.author.id)
        if amount == "all":
            wallet = await update_bank(ctx.message.author.id)
            wallet = wallet[0]
            if wallet == 0:
                msg = await ctx.send("You deposited 0 snips!")
                await asyncio.sleep(4.1)
                await msg.edit(content="You're actually an idiot trying to deposit nothing. Really just super stupid <:kek:746957664961036338>")
                return
            await update_bank(ctx.message.author.id, -1*wallet)
            await update_bank(ctx.message.author.id, wallet, "bank")
            await ctx.send(f"you deposited {wallet} snips")
            return
        else:
            if amount == None:
                await ctx.send("...well you have to input something")
                return
            amount = int(amount)
            if amount == 0:
                msg = await ctx.send("You deposited 0 snips!")
                await asyncio.sleep(4.1)
                await msg.edit(content="You're actually an idiot trying to deposit nothing. Really just super stupid <:kek:746957664961036338>")
                return
            if amount > bal[0]:
                await ctx.send("sorry, but you don't have enough money")
                return
            if amount<0:
                await ctx.send("did you just..try to desposit less than nothing?")
                return

            await update_bank(ctx.message.author.id, -1*amount)
            await update_bank(ctx.message.author.id, amount, "bank")

            await ctx.send(f"you deposited {amount} snips!")
            return

    @cooldown(1, hour*12, BucketType.user)
    @commands.command()
    @guild_only()
    async def beg(self, ctx):
        await open_account(ctx.message.author.id)

        outcome = random.choice([True, False])

        if outcome == True:
            earnings = random.randrange(1, 420)
            await ctx.send(f"{ctx.message.author.mention}, someone took pity for you and gave you {earnings} snips!")
            await update_bank(ctx.message.author.id, change=earnings)
        else:
            await ctx.send(f"{ctx.message.author.mention}, after begging you werent able to get any money :pensive:")
        return
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(f"{ctx.message.author.mention} you're on cooldown for " + "%d hours, %d minutes, and %d seconds" % (hour, minutes, seconds))
        return

    @commands.command()
    @guild_only()
    async def give(self, ctx, member : discord.Member=None, amount=None):
        if member == None:
            await ctx.send(f"""{ctx.message.author.mention}, you must put the command in this type of format:
                                `s.give @Wiki#5420 69420`""")
            return
        await open_account(ctx.message.author.id)
        await open_account(member.id)

        bal = await update_bank(ctx.message.author.id)


        amount = int(amount)
        if amount == 0:
            await ctx.send('you must input an amount to give')
            return
        if amount > bal[0]:
            await ctx.send("sorry, but you don't have enough money")
            return
        if amount<0:
            await ctx.send("did you just..try to give someone less than nothing?")
            return


        await update_bank(user_id=ctx.message.author.id, change=-1*amount)
        await update_bank(member.id, amount)
        await ctx.send(f"send {amount} to {member.name}")
        return

def setup(client):
    client.add_cog(Economy(client))
