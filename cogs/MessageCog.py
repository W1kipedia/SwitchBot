import discord, asyncio, os
from better_profanity import profanity
from discord.ext import commands


class messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        sample_message = str(message.content).lower()
        if not message.author.bot:
            if message.content.startswith("<@!752666067536576512>"):
                await message.channel.send(content=f"what do you want {message.author.mention}, you know you can just do `s.help` to get all the commands right?", delete_after=5.0)
                return
            if int(message.channel.id) == 738155429342871623:
                async def add_reactions():
                    for emote in message.guild.emojis:
                        if emote.name == "yes":
                            global yes
                            yes = emote
                        elif emote.name == "no":
                            global no
                            no = emote
                        elif emote.name == "thronking":
                            global thronking
                            thronking = emote
                        else:
                            pass
                    #=================================================================
                    await message.add_reaction(yes)
                    await message.add_reaction(no)
                    await message.add_reaction(thronking)
                    return
                try:
                    with open("/tmp/Switch-bot/guest.txt", 'r') as e:
                        if message.author.id == int(e.read()):
                            await message.author.remove_roles(message.guild.get_role(832068361932111872))
                            await add_reactions()
                            os.system("shred -z -v /tmp/Switch-Bot/guest.txt; rm /tmp/Switch-bot/guest.txt")
                            return
                except FileNotFoundError:
                    pass
                if message.author.id == 547971853990494208:
                    await add_reactions()
                    return
            profanity.load_censor_words_from_file("./data/profanity.txt")
            #profanity.load_censor_words()
            if profanity.contains_profanity(sample_message):
                await message.delete()
                await message.channel.send(content=f"{message.author.mention} you cannot use that word here", delete_after=5.0)
        return

def setup(client):
    client.add_cog(messages(client))