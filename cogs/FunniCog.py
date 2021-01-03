import discord, random, asyncio, os
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

class Funni(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=('funni_menu', "funni_help"))
    async def funni(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="funni menu (but for mobile)", description="all funni commands that you can use", color=discord.Colour.blue())
            embed.add_field(name="1️⃣delay", value="**shows the delay between me and the server**")
            embed.add_field(name="2️⃣sponser", value="**I would like to thank our sponser...**")
            embed.add_field(name="3️⃣8ball/eightball", value="**wanna ask a question? Ask away!**")
            embed.add_field(name="4️⃣OwO/owo", value="**translate any text using this command!**")
            embed.add_field(name="5️⃣encrypt", value="**decrypt any message that you want!**")
            embed.add_field(name="6️⃣decrypt", value="**decrypt any message that was encrypted with me!**")
            embed.add_field(name="7️⃣open_url", value="**force open a url on wiki's browser (ABSOLUTELY NOT ANY NSFW LINKS/MATERIAL ARE ALLOWED)**")
            embed.add_field(name="8️⃣coinflip", value="**just say the command and I'll automatically flip a coin!(I have butter fingers sometimes so I'm sorry if I mess something up)**")
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="funni menu", description="all funni commands that you can use", color=discord.Colour.blue())
        embed.add_field(name="delay", value="`shows the delay between me and the server`")
        embed.add_field(name="sponser", value="`I would like to thank our sponser...`")
        embed.add_field(name="8ball/eightball", value="`wanna ask a question? Ask away!`")
        embed.add_field(name="OwO/owo", value="`translate any text using this command!`")
        embed.add_field(name="encrypt", value="`decrypt any message that you want!`")
        embed.add_field(name="decrypt", value="`decrypt any message that was encrypted with me!`")
        embed.add_field(name="open_url", value="`force open a url on wiki's browser (ABSOLUTELY NOT ANY NSFW LINKS/MATERIAL ARE ALLOWED)`")
        embed.add_field(name="coinflip", value="`just say the command and I'll automatically flip a coin!(I have butter fingers sometimes so I'm sorry if I mess something up)`")
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return

    @commands.command(aliases=('8ball', 'eight_ball'))
    async def eightball(self, ctx, *, question=None):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if question==None:
            await ctx.send(f"bruh you need to put a question {ctx.message.author.mention}")
        else:
            responses = ('It is certain.',
                        'It is decidedly so.',
                        'Without a doubt.',
                        'Yes – definitely.',
                        'You may rely on it.',
                        'As I see it, yes.',
                        'Most likely.',
                        'Outlook good.',
                        'Yes.',
                        'Signs point to yes.',
                        'Reply hazy, try again.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        'Don\'t count on it.',
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Very doubtful.',)
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
        return

    @commands.command(aliases=('owo', 'owo_translate'))
    async def OwO(self, ctx, *, context):
        if str(ctx.message.channel.type).lower() == "private":
            return
        translate = ""
        for letter in context:
            if letter == "o" or letter == "O":
                translate += "OwO"
            elif letter == "u" or letter == "U":
                translate += "UwU"
            else:
                translate += letter
        await ctx.send(f'original text: {context}\n OwO translate: {(translate)}')
        return

    @cooldown(1, 3, BucketType.user)
    @commands.command()
    async def coinflip(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        possible = ('Heads!', 'Tails!', 'Heads!', 'Tails!', 'fuck, I dropped the coin. Use the command again')

        await ctx.send(f'{random.choice(possible)}')
        return
    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds!", delete_after=error.retry_after)
        return


    #this is a major issue, after trying to make the code a bit more pretty I made it unstable
    #I currently am too busy to fix it, so if anyone is 
    """
    @cooldown(1, 60*60, BucketType.user)
    @commands.command(aliases=("sponsor", "spons"))
    async def sponser(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        sponsers = []
        await ctx.send("don't forget to..")
        await asyncio.sleep(1.2)
        await ctx.send("check out todays sponser!")
        await asyncio.sleep(1.7)
        for file in os.listdir("./sponsers"):
            if file.endswith('.txt'):
                with open(os.path.join("./sponsers", file), 'r') as f:
                    sponsers += f
        something_useful = str(random.choice(sponsers))
        andre = something_useful.split(',')
        for e in andre:
            await ctx.send("***__" + e + "__***")
            asyncio.sleep(2)
        return
    @sponser.error
    async def sponser_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = float(error.retry_after)
            minutes = time // 60
            time %= 60
            seconds = time
            await ctx.send(str(f"{ctx.message.author.mention}, you're on cooldown for " + "%d minute(s) and %d second(s)" % (minutes, seconds)))
        return
    """
    @commands.command()
    async def encrypt(self, ctx, *, context):
        if str(ctx.message.channel.type).lower() == "private":
            return
        message_to_send = ""
        for i in range(0, len(context)):
            message_to_send = message_to_send + chr(ord(context[i]) - 2)

        await ctx.send(message_to_send)
        return
    @commands.command()
    async def decrypt(self, ctx, *, context):
        if str(ctx.message.channel.type).lower() == "private":
            return
        message_to_send = ""
        for i in range(0, len(context)):
            message_to_send = message_to_send + chr(ord(context[i]) + 2)
        await ctx.send(message_to_send)
        return

    @cooldown(1, 5, BucketType.user)
    @commands.command(aliases=("ping", "pong"))
    async def delay(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        msg = await ctx.send("⚙ calculating...")
        await asyncio.sleep(3)
        await msg.edit(content=f'💡 message delay is {round(self.client.latency * 1000)}ms')
        return
    @delay.error
    async def delay_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            user = ctx.message.author.name
            tag = ctx.message.author.discriminator
            if (user, tag)==("Bob557", "5208") or ctx.message.author.id == 312726571079303168:
                await ctx.send(content=f"Haha, fuck you bob. You're on cooldown for {error.retry_after:,.2f} seconds", delete_after=error.retry_after)
            else:
                await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds", delete_after=error.retry_after)
        return

def setup(client):
    client.add_cog(Funni(client))
