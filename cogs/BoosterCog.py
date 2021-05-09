import discord, better_profanity, json, random
import mysql.connector as mysql
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown, guild_only
from discord.ext import commands
hour = 60*60

async def get_booster_info():
    with open("./data/boosterinfo.json", 'r', encoding="utf-8") as f:
        users = json.load(f)

    return users
async def get_bank_data():
    with open("./data/mainbank.json", 'r', encoding="utf-8") as f:
        users = json.load(f)
    return users

async def open_account(user_id):
    try:
        tempdb = mysql.connect(
            host = "localhost",
            database = "Switchbot",
            user = "root",
            password = "root"
        )
        tempcur = tempdb.cursor()

        users = []
        tempcur.execute("SELECT `client_id` FROM `Economy`;")
        for user in tempcur:
            users.append(user[0])
        if str(user_id) in users:
            tempdb.close()
            tempcur.close()
            return False
        else:
            tempcur.execute(f"INSERT INTO `Economy` VALUES ('{str(user_id)}', 69, 420)")
            tempdb.commit()
            tempdb.close()
            tempcur.close()
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





class booster(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @guild_only()
    async def booster_menu(self, ctx):
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="The booster menu (but for mobile)", color=discord.Colour.purple())
            embed.add_field(name="1️⃣preview", value="**get the latest preview of newest Switch N Snap video that's in the making**")
            embed.add_field(name="2️⃣extra_bonus", value="**every 12 hours you'll be able to get even more money using this command (can range from 0-102)**")
            embed.add_field(name="3️⃣change_role_name {name}", value="**if you want to change your booster role, you can by using this command**")
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="The booster menu", color=discord.Colour.purple())
        embed.add_field(name="preview", value="`get the latest preview of newest Switch N Snap video that's in the making`")
        embed.add_field(name="extra_bonus", value="`every 12 hours you'll be able to get even more money using this command (can range from 0-102)`")
        embed.add_field(name="change_role_name {name}", value="`if you want to change your booster role, you can by using this command`")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return

    @commands.command()
    @commands.has_role(661115568450961410)
    @cooldown(1, 60*69, BucketType.user)
    @guild_only()
    async def change_role_name(self, ctx, *, name=None):
        better_profanity.profanity.load_censor_words()

        if name == "" or name == " " or name == None:
            await ctx.send(f"{ctx.message.author.mention}, you have to input a role name")
            return
        if better_profanity.profanity.contains_profanity(name):
            await ctx.message.delete()
            await ctx.send(f"{ctx.message.author.mention}, that name contains profanity!")
            return
        try:
            db = mysql.connect(
            host = "localhost",
            database = "SwitchBot",
            user = "",
            password = ""
            )
            cursor = db.cursor()

            cursor.execute(f"SELECT `custom_role_name` FROM `Boosters` WHERE client_id = '{str(ctx.message.author.id)}';")
            for i in cursor:
                name_in_users = str(i[0])
            if name.lower() == name_in_users.lower():
                await ctx.send(f"{ctx.message.author.mention}, the name you inputted is the same name that you have now")
            
            cursor.execute(f"SELECT `has_custom_role`, `custom_role_id` FROM `Boosters` WHERE client_id = '{str(ctx.message.author.id)}';")
            for i in cursor:
                has_custom_role = i[0]
                custom_role_id = i[1]
            if has_custom_role == None or custom_role_id == None:
                await ctx.send(f"{ctx.message.author.mention}, it seems that you have no custom role (according to the database)\n if you think this is a mistake (as in you have boosted for more than two months) pls ping wiki to fix this")
                return

            await ctx.send("alright changing your role name...")
            async with ctx.channel.typing():
                cursor.execute(f"SELECT `custom_role_id` FROM `Boosters` WHERE client_id = '{str(ctx.message.author.id)}';")
                for i in cursor:
                    role = i[0]
                role = ctx.guild.get_role(role)
                await role.edit(reason=f"{ctx.message.author.name} decided to change their custom role to {name}",
                                name=name)
                sanitized = "\\"
                for i in name:
                    sanitized += i + '\\'
                cursor.execute(f"UPDATE `Boosters` SET `custom_role_name`='{sanitized}' WHERE client_id = '{str(ctx.message.author.id)}';")
                db.commit()
                cursor.close()
                db.close()
            await ctx.send(f"{ctx.message.author.mention}, your role name has been changed!")
            return

        except:
            users = await get_booster_info()
            name_in_users = str(users[str(ctx.message.author.id)]["custom role name"])
            if name.lower() == name_in_users.lower():
                await ctx.send(f"{ctx.message.author.mention}, the name you inputted is the same name that you have now")

            if users[str(ctx.message.author.id)]["has custom role"] == None or users[str(ctx.message.author.id)]["custom role id"] == None:
                await ctx.send(f"{ctx.message.author.mention}, it seems that you have no custom role (according to the database)\n if you think this is a mistake (as in you have boosted for more than two months) pls ping wiki to fix this")
                return

            await ctx.send("alright changing your role name...")
            async with ctx.channel.typing():
                role = int(users[str(ctx.message.author.id)]["custom role id"])
                role = ctx.guild.get_role(role)
                await role.edit(reason=f"{ctx.message.author.name} decided to change their custom role to {name}",
                                name=name)
                users[str(ctx.message.author.id)]["custom role name"] = name

                with open("./data/boosterinfo.json", 'w', encoding="utf-8") as f:
                    json.dump(users, f)
            await ctx.send(f"{ctx.message.author.mention}, your role name has been changed!")
            return
    @change_role_name.error
    async def change_role_name_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.message.author.mention}, you're not boosting the server to use command, try boosting the server!")
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(f"{ctx.message.author.mention}, you're on cooldown for " + "%d hours, %d minutes, and %d seconds" % (hour, minutes, seconds))
        return

    @commands.command()
    @commands.has_role(661115568450961410)
    @guild_only()
    async def preview(self, ctx):
        with open("./data/latest_video.txt", 'r', encoding="utf-8") as f:
            video = f.read()
        if video == "" or video == " ":
            await ctx.send(f"{ctx.message.author.mention}, it seems that there is no preview available right now :pensive:")
            return
        try:
            await ctx.message.author.send(video)
            await ctx.message.author.send("please respect that these previews are only for people who boost and don't release these to people who haven't boosted")
        except:
            await ctx.send(f"{ctx.message.author.mention}, I'm not able to DM you for some reason, try allowing your DMs")
            return
        await ctx.send(f"{ctx.message.author.mention}, check your DMs")
        return
    @preview.error
    async def preview_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.message.author.mention}, you must boost the server to use this commands")
        return

    @commands.command()
    @commands.has_role(661115568450961410)
    @cooldown(1, hour*12, BucketType.user)
    @guild_only()
    async def extra_bonus(self, ctx):
        await open_account(ctx.message.author.id)
        await get_bank_data()

        earnings = random.randrange(0, 102)

        await ctx.send(f"{ctx.message.author.mention}, you earned {earnings} amount of snips")

        await update_bank(user_id=ctx.message.author.id, change=earnings)
        return
    @extra_bonus.error
    async def extra_bonus_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(f"{ctx.message.author.mention} you're on cooldown for " + "%d hours, %d minutes, and %d seconds" % (hour, minutes, seconds))
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.message.author.mention}, you must boost the server to use booster-only commands")
            return

def setup(client):
    client.add_cog(booster(client))
