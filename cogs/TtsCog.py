from better_profanity.better_profanity import Profanity
from gtts import gTTS
from discord.ext import commands
from better_profanity import profanity
import discord, os
profanity.load_censor_words_from_file("./data/profanity.txt")

class tts(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tts(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="tts menu (but for mobile", color=discord.Colour.orange())
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="1️⃣join", value="**if you want to start making the bot talk, you can make it join with this command**")
            embed.add_field(name="2️⃣leave", value="**if you're done with the bot, you can make it leave (or it'll leave automatically too)**")
            embed.add_field(name="3️⃣speak", value="**If you want to start making the bot talk you can use this command and with whatever words you desire**")
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="tts menu", color=discord.Colour.orange())
        embed.set_footer(text=f"Command by {ctx.message.author.name}")
        embed.add_field(name="join", value="`if you want to start making the bot talk, you can make it join with this command`")
        embed.add_field(name="leave", value="`if you're done with the bot, you can make it leave (or it'll leave automatically too)`")
        embed.add_field(name="speak", value="`If you want to start making the bot talk you can use this command and with whatever words you desire`")
        await ctx.send(embed=embed)
        return

#come back to this another time whenever you learn *args so you can use a true or false boolean

    @commands.command() 
    async def speak(self, ctx,*, prompt = None):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if profanity.contains_profanity(prompt):
            return
        j = discord.utils.get(self.client.voice_clients, guild=ctx.message.guild)
        yeet = ctx.message.author.voice
        if yeet == None or prompt == None:
            await ctx.send("*no*")
            return
        channel = yeet.channel
        if j == None:
            await ctx.message.add_reaction('🤝')
            await channel.connect()
        #start playing
        output = gTTS(text=prompt)
        output.save("playing.mp3")
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.message.guild)
        await voice.play(discord.FFmpegPCMAudio(executable="ENTER PATH FOR FFMPEG EXECUTABLE", source="./playing.mp3"))
        await voice.disconnect()
        return

    @commands.command()
    async def join(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.message.guild)
        if voice == None:
            pass
        channel = ctx.message.author.voice.channel
        if channel == None:
            await ctx.send("*no*")
            return
        await channel.connect()
        await ctx.message.add_reaction('🤝')
        return
    @commands.command()
    async def leave(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        pp = self.client.get_guild(643082091961122816)

        for crash in pp.emojis:
            if crash.name == "kirby":
                global bazinga
                bazinga = crash

        await ctx.message.add_reaction(bazinga)
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.message.guild)
        if voice == None:
            await ctx.send("idk about you, but I don't think I'm in a vc")
            return
        await voice.disconnect()
        await ctx.message.add_reaction(bazinga)
        return

def setup(client):
    client.add_cog(tts(client))
