import json, discord, wikipedia, asyncio, datetime
from discord.ext import commands



class AllEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        if member.bot:
            asyncio.sleep(3)
            member_role = self.client.get_role(643121101035012126)
            bot_role = self.client.get_role(693706143251562498)
            await member.remove_roles(member_role)
            await member.add_roles(bot_role)
            return
        """
        print(f"{member.name} has joined the server.")
        beta = self.client.get_channel(693680984306221126)
        pp = self.client.get_guild(643082091961122816)

        for crash in pp.emojis:
            if crash.name == "kirby":
                global bazinga
                bazinga = crash

        await beta.send(f"Hey gamers, {member.name} has joined the arena! {bazinga}")

        try:
            await asyncio.sleep(5)
            await member.send("HOLD UP!")
            await asyncio.sleep(3)
            await member.send("Before you do anything, make sure to read <#693678101019754496>\nalso you can get your roles from <#693970245404065892>; like games, events, and announcments that you want to get notified of!.\n Okay that's basically everything that you need to know, make sure to stay hydrated. Enjoy the server!\n")
            print("and I was able to DM them! :D")
        except:
            print("they have their DMs close, so I couldn't message them D:")
        return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} left the server')
        bababooey = self.client.get_channel(693942943039488050)
        nu = discord.Embed(title=f"{member} has left the server 😔", color=discord.Colour.red())
        await bababooey.send(embed=nu)
        return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot or after.bot:
            return

        for r in before.roles:
            if r not in after.roles:
                if r.id == 661115568450961410:
                    with open("./data/boosterinfo.json", 'r', encoding="utf-8") as f:
                        boosters = json.load(f)

                    boosters[str(before.id)]["has custom role"] = False
                    boosters[str(before.id)]["custom role name"] = None
                    boosters[str(before.id)]["custom role id"] = None

                    with open("./data/boosterinfo.json", 'w', encoding="utf-8") as f:
                        json.dump(boosters, f)
        return

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(f"the {ctx.command} command was invoked successfully by {ctx.message.author}!")
        if str(ctx.message.channel).lower() == "private":
            print("^ this command was used in a DM")
        return
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if str(error).lower().endswith("TypeError: object NoneType can't be used in 'await' expression".lower()):
            return
        try:
            for emoji in ctx.guild.emojis:
                if emoji.name == "joe":
                    await ctx.message.add_reaction(emoji)
        except:
            await ctx.message.add_reaction('🦧')
        name = ctx.message.author.name
        tag = ctx.message.author.discriminator
        if (name, tag)==("Wiki", "5420"):
            if str(error).lower().startswith("you are on cooldown."):
                return
            if str(error).lower() == "Command raised an exception: UnboundLocalError: local variable 'page' referenced before assignment".lower():
                await ctx.send("you must specify the object you're searching for.\n For example. `s.wiki_summary bill gates (person)`, or `s.wiki_summary wikipedia (website)`")
                return
            e = discord.Embed(title=str(error), color=discord.Colour.red())
            await ctx.send(embed=e)
            return
        if str(error).lower().startswith("you are on cooldown."):
            return
        if str(error).lower() == "Command raised an exception: UnboundLocalError: local variable 'page' referenced before assignment".lower():
            await ctx.send("you must specify the object you're searching for.\n For example. `s.wiki_summary bill gates (person)`, or `s.wiki_summary wikipedia (website)`")
            return
        if isinstance(error, wikipedia.exceptions.DisambiguationError):
            return
        if isinstance(error, discord.errors.Forbidden):
            return
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(content=f"❌||**{ctx.message.author.name}, that command was not found**", delete_after=4.0)
            return
        elif isinstance(error, commands.MissingRole):
            return
        elif isinstance(error, commands.errors.ExtensionAlreadyLoaded):
            await ctx.send(content="❌||**The cog is already loaded!**", delete_after=2.0)
            return
        elif isinstance(error, commands.errors.ExtensionError):
            await ctx.send(content="❌||**There was an error while trying to activate the cog. Check terminal for details!**", delete_after=3.3)
        elif isinstance(error, commands.errors.ExtensionNotFound):
            await ctx.send(content="❌||**After searching, I wasn't able to find the cog that you were looking for!**", delete_after=3.3)
            return
        elif isinstance(error, commands.errors.ExtensionFailed):
            await ctx.send(content="❌||**There was a problem loading the cog; It failed. Check terminal for more details!**", delete_after=3.3)
        elif isinstance(error, commands.errors.ExtensionNotLoaded):
            print("this command went through")
            await ctx.send(content="❌||**The cog hasn't been loaded in!**", delete_after=3.3)
            return
        elif isinstance(error, commands.MissingPermissions):
            return
        await ctx.send(content=error, delete_after=5.0)
        print(f"\n\nthe {ctx.command} command raised an error! {error}\n\n")
        return
def setup(client):
    client.add_cog(AllEvents(client))
