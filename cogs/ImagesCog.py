import discord, datetime, random, json
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
class Images(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=("images", "image_menu", "image_misc"))
    @guild_only()
    async def image_commands(self, ctx):
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="Image Menu (but for mobile)", description="a menu of images that you can bring up!(you can submit some images to me so i can add it to the list :D)", color=discord.Colour.blue())
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="1️⃣joe", value="**joe moment**")
            embed.add_field(name="2️⃣joey", value="**joey moment (joe's son)**")
            embed.add_field(name="3️⃣cole", value="**cole moment (joe's brother)**")
            embed.add_field(name="4️⃣alex", value="**alex moment (joey's uncle)**")
            embed.add_field(name="5️⃣chester", value="**chester moment (joe's father/joey's grandpa)**")
            embed.add_field(name="6️⃣derp", value="**this exists..that's kinda it**")
            embed.add_field(name="7️⃣cryson", value="**When you feel nothing but pain**")
            embed.add_field(name="8️⃣candice", value="**candice moment (joe's bigger sister)**")
            embed.add_field(name="9️⃣perhaps", value="**whenever someone says probably always respond with this command**")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Image Menu", description="a menu of images that you can bring up!(you can submit some images to me so i can add it to the list :D)", color=discord.Colour.blue())
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="joe", value="`joe moment`")
        embed.add_field(name="joey", value="`joey moment (joe's son)`")
        embed.add_field(name="cole", value="`cole moment (joe's brother)`")
        embed.add_field(name="alex", value="`alex moment (joey's uncle)`")
        embed.add_field(name="chester", value="`chester moment (joe's father/joey's grandpa)`")
        embed.add_field(name="derp", value="`this exists..that's kinda it`")
        embed.add_field(name="cryson", value="`When you feel nothing but pain`")
        embed.add_field(name="candice", value="`candice moment (joe's bigger sister)`")
        embed.add_field(name="perhaps", value="`whenever someone says probably always respond with this command`")
        await ctx.send(embed=embed)
        return

    @cooldown(1, 5, BucketType.user)
    @commands.command()
    @guild_only()
    async def joe(self, ctx):
        embed = discord.Embed(title="Joe moment", description="")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://media.discordapp.net/attachments/693941496147214357/753068754228871309/cat_next_to_camera.jpg")
        await ctx.send(embed=embed)
        return
    @joe.error
    async def joe_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f'buddy, you\'re on cooldown for {error.retry_after:,.2f} seconds', delete_after=error.retry_after)

    @cooldown(1, 15, BucketType.user)
    @commands.command()
    @guild_only()
    async def joey(self, ctx):
        embed = discord.Embed(title="Joey Moment", description="")
        embed.set_image(url="https://media.discordapp.net/attachments/693941496147214357/762032313567019048/IMG_20201003_102333.jpg?width=555&height=475")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    @joey.error
    async def joey_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds man :pensive:", delete_after=error.retry_after)
        return

    @cooldown(2, 10, BucketType.user)
    @commands.command()
    @guild_only()
    async def cryson(self, ctx):
        embed = discord.Embed(title="p     a       i      n", description="", color=discord.Colour.red())
        embed.set_image(url="https://media.discordapp.net/attachments/693942287910305842/767628023251206174/pfpcarson.gif?width=475&height=475")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    @cryson.error
    async def cryson_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} gamer you're on cooldown for {error.retry_after:,.2f} seconds\ngo drink some milk or something while you're waiting", delete_after=error.retry_after)
        return

    @cooldown(2, 15, BucketType.user)
    @commands.command()
    @guild_only()
    async def cole(self, ctx):
        embed = discord.Embed(title="cole moment", description="")
        embed.set_image(url="https://media.discordapp.net/attachments/693941496147214357/768460791962664970/20201021_000957.jpg")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    @cole.error
    async def cole_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds\ngo drink milk or something while you're waiting", delete_after=error.retry_after)
        return

    @cooldown(1, 86400, BucketType.user)
    @commands.command(aliases=("doncon", "DONCON"))
    @guild_only()
    async def derp(self, ctx):
        embed = discord.Embed(title="", description="")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://media.discordapp.net/attachments/626617640634286081/754460623496151182/image0.png")
        await ctx.send(embed=embed)
        return
    @derp.error
    async def derp_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(str(f"{ctx.author.mention} sorry to say but, you're on cooldown from using doncon for " + "%d hours, %d minutes, and %d seconds" % (hour, minutes, seconds)))
        return

    @cooldown(1, 15, BucketType.user)
    @commands.command()
    @guild_only()
    async def perhaps(self, ctx):
        dropping = ["https://media.discordapp.net/attachments/609936758100066311/755835062066479174/perhaps.jpg",
                    "https://media.discordapp.net/attachments/693942287910305842/753764523261034566/perhaps1.jpg?width=394&height=475"]
        random_thing = random.choice(dropping)
        embed = discord.Embed(title="perhaps", description="")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.set_image(url=f"{random_thing}")
        await ctx.send(embed=embed)
        if random_thing == "https://media.discordapp.net/attachments/693942287910305842/753764523261034566/perhaps1.jpg?width=394&height=475":
            dropping.append("https://media.discordapp.net/attachments/609936758100066311/755835062066479174/perhaps.jpg")
            await ctx.send("your chances are now more slim")
        return
    @perhaps.error
    async def perhaps_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds 😳", delete_after=error.retry_after)
            return

    @cooldown(1, 15, BucketType.user)
    @commands.command()
    @guild_only()
    async def candice(self, ctx):
        embed = discord.Embed(title="Candice moment", description="")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="https://media.discordapp.net/attachments/693942287910305842/753749038356103318/cat_next_to_camera2.jpg")
        await ctx.send(embed=embed)
        return
    @candice.error
    async def candice_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"pretty weird {ctx.message.author.mention} how you think that your cooldown isn't {error.retry_after:,.2f} seconds", delete_after=error.retry_after)

    @commands.command()
    @cooldown(1, 15, BucketType.user)
    @guild_only()
    async def alex(self, ctx):
        embed = discord.Embed(title="Alex moment")
        embed.set_image(url="https://media.discordapp.net/attachments/693941496147214357/773255455857704980/image0.png?width=465&height=475")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    @alex.error
    async def alex_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention}, you're on cooldown for {error.retry_after:,.2f} seconds", delete_after=error.retry_after)
        return

    @commands.command()
    @cooldown(1, 15, BucketType.user)
    @guild_only()
    async def chester(self, ctx):
        embed = discord.Embed(title="Chester moment")
        embed.set_image(url="https://media.discordapp.net/attachments/693680984306221126/777590561393082388/20201115_124701.jpg?width=470&height=474")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    @chester.error
    async def chester_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention}, you're on cooldown for {error.retry_after:,.2f} seconds", delete_after=error.retry_after)
        return


def setup(client):
    client.add_cog(Images(client))
