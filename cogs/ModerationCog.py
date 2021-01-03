import discord, datetime, json, asyncio
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role("Staff")
    async def mod_menu(self, ctx):
        embed = discord.Embed(title="Moderator menu", description="`Someone acting up? Decide their fate`", color=discord.Colour.red())
        embed.add_field(name="Mute/Unmute {member's name}", value="mute someone or unmute them")
        embed.add_field(name="ban {member's name} {optional reason}", value="ban someone duh")
        embed.add_field(name="unban {member's name and tag} {optional reason}", value="unban someone duh")
        embed.add_field(name="kick {member's name} {optional reason}", value="kick someone obviously")
        embed.add_field(name="delete {amount}", value="delete any messages (if you don't use an amount 1 message will auto delete)")
        embed.add_field(name="DM {member's name} {message to send}", value="DM someone anonymously (THE CREATOR CAN SEE WHO SAID SOMETHING TO SOMEONE ELSE, SO WATCH WHAT YOU SAY!")
        await ctx.send(embed=embed)
        return
    @mod_menu.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("I'm sorry, but you're missing the staff role")
        return

    @commands.command(aliases=("del", "purge"))
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
        return
    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("imagine trying to use the delete command without the manage message perm")
        return

    #ever since the booster cog and other role-altering things as been added, more variables had to be considered for the mute() and unmute() commands
    #I'm pretty sure it's ok but if anyone wants to contribute on this, go ahead
    @commands.command()
    @commands.has_role("Staff")
    async def mute(self, ctx, member : discord.Member):
        Muted_role = ctx.guild.get_role(696463147934154816)
        Member_role = ctx.guild.get_role(643121101035012126)
        with open("./data/boosterinfo.json", 'r', encoding="utf-8") as f:
            info = json.load(f)
        if str(member.id) not in info:
            pass
        else:
            if info[str(member.id)]["has custom role"] == False:
                pass
            if info[str(member.id)]["custom role id"] != None and info[str(member.id)]["custom role name"] != None:
                booster_role = ctx.guild.get_role(info[str(member.id)]["custom role id"])
                await member.remove_roles(booster_role)

        await member.add_roles(Muted_role)
        await member.remove_roles(Member_role)
        await ctx.send(str(member.mention + " has been muted >:c"))
        return
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("you're missing the Staff role to mute someone, you knew this but still")
        return

    @commands.command()
    @commands.has_role("Staff")
    async def unmute(self, ctx, member : discord.Member):
        Muted_role = ctx.guild.get_role(696463147934154816)
        Member_role = ctx.guild.get_role(643121101035012126)
        with open("./data/boosterinfo.json", 'r', encoding="utf-8") as f:
            info = json.load(f)
        if str(member.id) not in info:
            pass
        else:
            if info[str(member.id)]["has custom role"] == False:
                pass
            if info[str(member.id)]["custom role id"] != None and info[str(member.id)]["custom role name"] != None:
                booster_role = ctx.guild.get_role(info[str(member.id)]["custom role id"])
                await member.add_roles(booster_role)

        await member.add_roles(Member_role)
        await member.remove_roles(Muted_role)
        await ctx.send(f" {member.mention} has been unmuted :D")
        return
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("you're missing the Staff role to unmute someone, you also knew this but still")
        return


    #a problem with the ban and unban commands is that when trying to DM the member on the reason on why they got banned/kicked the bot raises and err saying that they couldn't DM the member even if their DMs were open
    #tl;dr needs fix for DMing members before they get banned or kicked
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason= "no reason was provided"):
        try:
            await member.send(f"you've been banned from Switch N' Snap for `{reason}`")
            await asyncio.sleep(1)
        except:
            await ctx.send(content="cannot DM member", delete_after=3.0)
        await member.ban(reason=reason)
        await ctx.message.delete()
        embed = discord.Embed(title=f"{member} was banned", color = discord.Colour.red()) if reason == "no reason was provided" else discord.Embed(title=f"{member} was banned for \"{reason}\"", color=discord.Colour.red())
        await ctx.send(embed=embed)
        return
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm sorry, but you don't have the perms to ban someone")
        return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *,member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split("#")

        for banned_entry in banned_users:
            user = banned_entry.user

            if(user.name, user.discriminator)==(member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(f"{member} has been unbanned by {ctx.message.author.mention} :D")
                return
        await ctx.send(f"{member} wasn't found on the ban list D:")
        return
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("sorry bud, you're not breaking your friend out of jail. You don't have ban perms")
        return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="reason wasn't provided"):
        try:
            await member.send.channel(f"you were kicked by {ctx.message.author} from Switch N' Snap for {reason}")
            await asyncio.sleep(1)
        except:
            await ctx.send(f"{member.mention} has their DMs close D:")
        await member.kick(reason=reason)
        await ctx.send(f"{member} was removed from the server for {reason}")
        return
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            ctx.send("bruh, you're missing the perms to kick someone")
        return

    @commands.command(aliases=("dm", "Dm", "dM"))
    @commands.has_role("Staff")
    async def DM(self, ctx, member : discord.Member, *, message):
        await ctx.message.delete()
        await ctx.send(content=f"alright messaging {member}", delete_after=2.0)
        try:
            await member.send(f"a staff member has decided to DM you:`{message}`")
            await ctx.send(content=f"{member} was successfully DM'd", delete_after=2.0)
        except:
            ctx.send(content=f"{member.name} has their DMs closed, or just isn't accepting DMs right now D:", delete_after=2.0)
        return
    @DM.error
    async def DM_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            ctx.send("ahem, you know you're not staff right?")
        return

def setup(client):
    client.add_cog(Moderation(client))
