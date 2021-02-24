import discord, json, os, random, asyncio
import mysql.connector as mysql
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown, guild_only


#--------------------------------------------------------------------------------------------------------------------------
async def get_bank_data():
    with open("./data/mainbank.json", 'r', encoding="utf-8") as f:
        users = json.load(f)
    return users

async def open_account(user_id):
    try:
        tempdb = mysql.connect(
            host = "localhost",
            database = "SwitchBot",
            user = "clientSidePers",
            password = "2H6r4H#jyu7J"
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
            user = "clientSidePers",
            password = "2H6r4H#jyu7J"
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



#all the code above is just used for functional programming to make stuff easier for the code below
class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @guild_only()
    async def gambling(self, ctx):
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="Gambling menu", description="the gambling menu to fill your gambling addiction")
            embed.add_field(name="1️⃣gambleflip", value="**it's like coinflipping but gambling**")
            embed.add_field(name="2️⃣rob", value="**you're gonna rob someone? There's a risk though!!**")
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Gambling menu", description="the gambling menu to fill your gambling addiction")
        embed.add_field(name="gambleflip", value="`it's like coinflipping but gambling`")
        embed.add_field(name="rob", value="`you're gonna rob someone? There's a risk though!!`")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return

    @cooldown(1, 30, BucketType.user)
    @commands.command()
    @guild_only()
    async def gambleflip(self, ctx, amount=0):
        await open_account(ctx.message.author.id)

        bal = await update_bank(ctx.message.author.id)
        try:
            amount = int(amount)
        except:
            await ctx.send("you have to input an actual number")
        if amount > bal[0]:
            await ctx.send("sorry, but you don't have enough money")
            return
        if amount<0:
            await ctx.send("you have to put a positive number")
            return
        if amount == 0:
            await ctx.send("you have to gamble something")
            return

        final = str(random.choice(("Tails", "Heads")))
        choice = str(random.choice(("Tails", "Heads")))
        await ctx.send(f"you chose {choice}!")
        await asyncio.sleep(1)

        if final == choice:
            await ctx.send("you won!")
            await asyncio.sleep(2)
            await update_bank(ctx.message.author.id, amount)
        else:
            await ctx.send("you lost!")
            await asyncio.sleep(2)
            await update_bank(ctx.message.author.id, -1*amount)
            await ctx.send(f"you lost {amount} snips!")
            return

        await ctx.send(f"you won {amount} snips!")
        return
    @gambleflip.error
    async def gambleflip_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're cooldown for {error.retry_after:,.2f} seconds :pensive:", delete_after=error.retry_after)
        return

    @cooldown(1, 60*12, BucketType.user)
    @commands.command(aliases=("mug", "steal", "Steal", "Mug"))
    @guild_only()
    async def rob(self, ctx, member:discord.Member=None):
        if member == None:
            await ctx.send(f"{ctx.message.author.mention}, you have to put a user to have to steal from, enjoy your cooldown because Wiki's too lazy to program a way to preven this <:kek:777419299261513728>")
            return
        await open_account(ctx.message.author.id)
        await open_account(member.id)
        member_id = int(member.id)

        bal = await update_bank(ctx.message.author.id)
        bal = bal[0]
        bal2 = await update_bank(member.id)
        bal2 = bal2[0]

        summarized_money_won = bal2/2 if bal2 % 2 == 0  else int(bal2/2.5)

        if bal2 <= 0:
            await ctx.send(f"{member.name} has no money in their wallet right now.")
            return
        else:
            stolen_money = random.randrange(0, summarized_money_won)
            if bal < 200:
                await ctx.send("you don't have any money in your wallet to even get perform a robbery (has to be above 200)")
                return
            else:
                lost_money = random.randrange(0, bal)

        good_scenarios = random.choice((f"you tripped {member.name} and they dropped {stolen_money} snips, so you took it!",
                                        f"you went into {member.name}'s house and stole {stolen_money} snips!",
                                        f"you bonked {member.name} on the head, they lost {stolen_money} snips!",
                                        f"you politely asked {member.name} for snips, they said sure....you got {stolen_money} snips."))
        #----------------------------------------------------------------------------------------------------------------------------------
        bad_scenarios = random.choice((f"you tripped {member.name} and they had zipper pockets so they dropped nothing, later on you got jumped and they took {lost_money} snips from you!",
                                        f"you went into {member.name}'s house and they had a strong security system, the cops chased after you and arrested you. You were charged with burgalry and gave {member.name} {lost_money} snips!",
                                        f"you bonked {member.name} on the head, and they had a reverse card and took {lost_money} snips from you!",
                                        f"you politely asked {member.name} for snips, they said no and asked for your snips instead...you said yes and gave them {lost_money} snips."))
        check_scenario = random.choice((True, False))
        if check_scenario == True:
            await ctx.send(good_scenarios)
            await update_bank(ctx.message.author.id, stolen_money)
            await update_bank(member_id, -1*stolen_money)
            return
        else:
            await ctx.send(bad_scenarios)
            await update_bank(ctx.message.author.id, -1*lost_money)
            await update_bank(member_id, lost_money)
            return
    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(f"{ctx.message.author.mention} you have to wait " + "%d hours, %d minutes, and %d seconds before you can strike again! :pensive:" % (hour, minutes, seconds))
        return


def setup(client):
    client.add_cog(Gambling(client))
