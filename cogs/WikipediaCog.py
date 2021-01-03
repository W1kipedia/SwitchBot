import discord, wikipedia
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
from wikipedia.wikipedia import search

class Wikipedia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=("Wikipedia_menu", "Wiki_menu", "wiki_menu"))
    async def wikipedia_menu(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="Wikipedia menu (but for mobile)", description="if you want to search up an article, you can now!", color = discord.Colour.dark_red())
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="1️⃣wiki_summary", value="**It is a quick (or long) summary on the article you type in**")
            embed.add_field(name="2️⃣wiki_search", value="**I recommend using this command first so that way you can understand what to type in correctly**")
            embed.add_field(name="3️⃣wiki_page", value="**this is a risky command mostly because it will more than likely exceed 6000 characters, but if you know it won't; you can use it :D**")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Wikipedia menu", description="if you want to search up an article, you can now!", color = discord.Colour.dark_red())
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="wiki_summary", value="It is a quick (or long) summary on the article you type in")
        embed.add_field(name="wiki_search", value="I recommend using this command first so that way you can understand what to type in correctly")
        embed.add_field(name="wiki_page", value="this is a risky command mostly because it will more than likely exceed 6000 characters, but if you know it won't; you can use it :D")
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=("Wiki_search", "Wikipedia_search", "wikipedia_search"))
    async def wiki_search(self, ctx, *, search=""):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if search == "" or search == " ":
            await ctx.send("you didn't put anything to search for")
        if ctx.message.channel.id == 693942287910305842:
            final = ""
            lst = wikipedia.search(search)
            for i in lst:
                final += i + "\n"
            await ctx.send("a list of articles:" + "\n" + "```" + "\n" + final + "```")
        else:
            await ctx.send(f"this command is only allowed in <#693942287910305842>")
        return


    #for the summary and page I need help with notifying the person who triggers the command that the page is over the character limit
    #either by putting it in an embed or finding a way to catch the err
    #also the error catching is inefficient, and any help to fix any of these is appreciated
    @cooldown(1, 10, BucketType.user)
    @commands.command()
    async def wiki_summary(self, ctx, * , search=""):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if search == "" or search == " ":
            await ctx.send("it seems you didn't put anything in your search")
            return
        if ctx.message.channel.id == 693942287910305842:
            try:
                summary = wikipedia.summary(search)
                page = wikipedia.page(search)
                await ctx.send("```\n" + summary + "```")
            except wikipedia.exceptions.DisambiguationError:
                await ctx.send("wasn't able to find what you were looking for, try using `wiki_search` to list a few, and copy/paste it into here")
            except wikipedia.exceptions.PageError:
                await ctx.send("couldn't find the page you were looking for :pensive:")
            except wikipedia.exceptions.RedirectError:
                await ctx.send("RedirectError bro, try again..?")
            except wikipedia.exceptions.WikipediaException:
                await ctx.send("I got a weird exception that isn't recognizable by the code, ping wiki about his problem pls")
                await ctx.send("unless you were missing an argument, then don't ping him")
            finally:
                await ctx.send(page.url)
        else:
            await ctx.send("you must go to <#693942287910305842> to use this command")
        return
    @wiki_summary.error
    async def wiki_summary_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"{ctx.message.author.mention} sorry but you're on cooldown for {error.retry_after:,.f} seconds")
        return

    @cooldown(1, 10, BucketType.user)
    @commands.command()
    async def wiki_page(self, ctx, *, search=""):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if search == "" or search == " ":
            await ctx.send("it seems you didn't put anything in your search")
            return
        if ctx.message.channel.id == 693942287910305842:
            try:
                page = wikipedia.page(search)
                await ctx.send("```\n" + page.content + "\n```")
            except wikipedia.exceptions.DisambiguationError:
                await ctx.send("wasn't able to find what you were looking for, try using `wiki_search` to list a few, and copy/past it into here")
            except wikipedia.exceptions.PageError:
                await ctx.send("couldn't find the page you were looking for :pensive:")
            except wikipedia.exceptions.RedirectError:
                await ctx.send("RedirectError bro, try again..?")
            except wikipedia.exceptions.WikipediaException:
                await ctx.send("I got a weird exception that isn't recognizable by the code, ping wiki about his problem pls")
            finally:
                await ctx.send(page.url)
        else:
            await ctx.send("sorry but you can only use this command in <#693942287910305842> ")
        return
    @wiki_page.error
    async def wiki_page_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"sorry but you're on cooldown {ctx.message.author.mention} for {error.retry_after:,.f} seconds")
        return

def setup(client):
    client.add_cog(Wikipedia(client))