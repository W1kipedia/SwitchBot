#first I notify myself on what is happening
print("booting up...")
#import all the good stuff
import discord, datetime, os, sys, webbrowser
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
from itertools import cycle
intents = discord.Intents.all()
client = commands.Bot(command_prefix = ["s.", "S."], intents=intents)
client.remove_command("help")
statuses = cycle(('cycle', 'cycle2'))
confirm = 0

@client.event
async def on_ready():
    change_status.start()
    print("bot is online.")
    print(datetime.datetime.now())
    return

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(statuses)))
    return

@client.command(aliases=('commands', 'menu'))
@guild_only()
async def help(ctx):
    if ctx.message.author.is_on_mobile():
        embed = discord.Embed(title="Help menu (but for mobile)",
        description="to show all the commands that are currently programmed into me!",
        color=discord.Colour.green())
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="🐱funni", value="**funni commands to use because they're funni**")
        embed.add_field(name="📖Wikipedia_menu", value="**search up an article on wikipedia!**")
        embed.add_field(name="❓help", value="**.  .  .I don't need to explain this**")
        embed.add_field(name="💬tts", value="**If you're too shy/lazy to talk in the vc. You can make the bot do it for you but using these commands**")
        embed.add_field(name="📈booster_menu", value="**a menu that is exclusive for people who boost the server**")
        embed.add_field(name="💸economy", value="**anything related to the economy (gambling and bank stuff) will be here)**")
        embed.add_field(name="📐mod_menu", value="**moderation menu `can only be accessed by people with Staff role`**")
        embed.add_field(name="🤖robot_menu", value="**the creator has a robot, and you can make it do stuff with the commands in this menu>**")
        embed.add_field(name="🔏wiki_help/admin_menu", value="**a menu specifically made for the creator of me**")
        embed.add_field(name="📷image_commands", value="**want to put up a random image? The images available are in here**")
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title="Help menu", description="to show all the commands that are currently programmed into me!", color=discord.Colour.green())
    embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
    embed.add_field(name="funni", value="`funni commands to use because they're funni`")
    embed.add_field(name="Wikipedia_menu", value="`search up an article on wikipedia!`")
    embed.add_field(name="help", value="`.  .  .I don't need to explain this`")
    embed.add_field(name="tts", value="`If you're too shy/lazy to talk in the vc. You can make the bot do it for you but using these commands`")
    embed.add_field(name="booster_menu", value="`a menu that is exclusive for people who boost the server`")
    embed.add_field(name="economy", value="`anything related to the economy (gambling and bank stuff) will be here)`")
    embed.add_field(name="mod_menu", value="`moderation menu`**can only be accessed by people with Staff role **")
    embed.add_field(name="robot_menu", value="`the creator has a robot, and you can make it do stuff with the commands in this menu>`")
    embed.add_field(name="wiki_help/admin_menu", value="`a menu specifically made for the creator of me`")
    embed.add_field(name="image_commands", value="`want to put up a random image? The images available are in here`")
    await ctx.send(embed=embed)
    return

@client.command()
async def restart(ctx, seconds=None):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==("Wiki", "5420"):
        await client.change_presence(activity=discord.Game("restarting..."))
        await ctx.send("restarting...")
        if seconds == None:
            os.system("./data/restarter.py")
        else:
            os.system(f"python ./data/restarter.py {seconds}")
        sys.exit()
    else:
        await ctx.send("sorry but you're not wiki")
    return

@client.command()
async def opt_in(ctx):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==('Wiki', '5420'):
        global confirm
        confirm = 1
        await ctx.send('people are now able to use open_url')
    else:
        await ctx.send(f"{ctx.message.author.mention} you are not <@547971853990494208> so you cannot use this command")
    return
@client.command()
async def opt_out(ctx):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name,tag)==('Wiki', '5420'):
        global confirm
        confirm = 0
        await ctx.send("people are no longer able to use open_url command")
    else:
        await ctx.send(f"{ctx.message.author.mention} you are not <@547971853990494208> so you cannot use this command")
    return

@client.command()
async def go_offline(ctx):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==("Wiki", "5420"):
        await client.change_presence(activity=discord.Game("shutting down..."))
        await ctx.send("shutting down...")
        sys.exit("SHUTTING DOWN PROGRAM")
    else:
        await ctx.send(f"{ctx.message.author.mention} you're not the creator, you cannot use this command")
    return

@client.command()
@cooldown(1, 7200, BucketType.user)
async def open_url(ctx, url=None):
    if ctx.message.channel.type == "private":
        return
    if confirm == 1:
        if url == None:
            await ctx.send(f"{ctx.message.author.mention} you have to put a url stupid")
        else:
            print(f"{ctx.message.author} opened up {url}")
            await ctx.send(f"okay opening up {url} on wiki's computer")
            async with ctx.channel.typing():
                webbrowser.open(url=url)
            await ctx.send("browser opening completed!\n||I hate you all||")
    else:
        await ctx.send("wiki has turned off this feature, if you think this is a mistake pls ping him")
    return
@open_url.error
async def open_url_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        time = float(error.retry_after)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        await ctx.send(f"{ctx.message.author.mention} you're on cooldown for:\n" + "%d hours, %d minutes, and %d seconds" % (hour, minutes, seconds))
    return

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
async def load(ctx, extension):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==("Wiki", "5420"):
        client.load_extension(f"cogs.{extension}")
        await ctx.send("{} loaded successfully!".format(extension))
    else:
        await ctx.send("you're not wiki >:c")
@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send(content="❌||**The cog is already loaded!**", delete_after=2.0)
        return
    if isinstance(error, commands.ExtensionError):
        await ctx.send(content="❌||**There was an error while trying to activate the cog. Check terminal for details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send(content="❌||**After searching, I wasn't able to find the cog that you were looking for!**", delete_after=3.3)
        return
    if isinstance(error, commands.ExtensionFailed):
        await ctx.send(content="❌||**There was a problem loading the cog; It failed. Check terminal for more details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotLoaded):
        print("this command went through")
        await ctx.send(content="❌||**The cog hasn't been loaded in!**", delete_after=3.3)
        return

@client.command()
async def unload(ctx, extension):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==("Wiki", "5420"):
        client.unload_extension(f"cogs.{extension}")
        await ctx.send("{} unload succesfully!".format(extension))
    else:
        await ctx.send("sorry but you're not wiki")
@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send(content="❌||**The cog is already loaded!**", delete_after=2.0)
        return
    if isinstance(error, commands.ExtensionError):
        await ctx.send(content="❌||**There was an error while trying to activate the cog. Check terminal for details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send(content="❌||**After searching, I wasn't able to find the cog that you were looking for!**", delete_after=3.3)
        return
    if isinstance(error, commands.ExtensionFailed):
        await ctx.send(content="❌||**There was a problem loading the cog; It failed. Check terminal for more details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotLoaded):
        print("this command went through")
        await ctx.send(content="❌||**The cog hasn't been loaded in!**", delete_after=3.3)
        return

@client.command()
async def reload(ctx, extension):
    name = ctx.message.author.name
    tag = ctx.message.author.discriminator
    if (name, tag)==("Wiki", "5420"):
        try:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
        except:
            client.load_extension(f"cogs.{extension}")
        await ctx.send("{} reloaded succesfully!".format(extension))
    else:
        await ctx.send("sorry but you're not wiki")
@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send(content="❌||**The cog is already loaded!**", delete_after=2.0)
        return
    if isinstance(error, commands.ExtensionError):
        await ctx.send(content="❌||**There was an error while trying to activate the cog. Check terminal for details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send(content="❌||**After searching, I wasn't able to find the cog that you were looking for!**", delete_after=3.3)
        return
    if isinstance(error, commands.ExtensionFailed):
        await ctx.send(content="❌||**There was a problem loading the cog; It failed. Check terminal for more details!**", delete_after=3.3)
    if isinstance(error, commands.ExtensionNotLoaded):
        print("this command went through")
        await ctx.send(content="❌||**The cog hasn't been loaded in!**", delete_after=3.3)
        return

try:
    blacklisted_cog = sys.argv[1]
    client.unload_extension(f"cogs.{blacklisted_cog}")
except:
    pass

with open("./data/token.txt", 'r', encoding="utf-8") as z:
    client.run(z.read())
