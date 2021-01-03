#there won't be any comments on this cog other than old comments and cut out code since this cog is deprecated

import discord, cozmo, asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

class Robot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def robot_menu(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        if ctx.message.author.is_on_mobile():
            embed = discord.Embed(title="Robot menu (but for mobile)", description="yes, this is real. The robot may be offline some of the time", color=discord.Colour.orange())
            embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="1️⃣robot_say", value="**if you want the robot to say something, put this command first!(char limit varies, but don't expect a whole paragraph to load in)**")
            embed.add_field(name="2️⃣robot_move {distance_in_millimeters}", value="**if you want to robot to move within the real world, you can! (limit for distance is 120mm)**")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Robot menu", description="yes, this is real. The robot may be offline some of the time", color=discord.Colour.orange())
        embed.set_footer(text=f"Command by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="robot_say", value="if you want the robot to say something, put this command first!(char limit varies, but don't expect a whole paragraph to load in)")
        #embed.add_field(name="robot_check", value="if you want to check if wiki is at his desk, use this program to make sure if he's at his desk")
        embed.add_field(name="robot_move {distance_in_millimeters}", value="if you want to robot to move within the real world, you can! (limit for distance is 120mm)")
        await ctx.send(embed=embed)
        return

    @cooldown(1,60, BucketType.user)
    @commands.command()
    async def robot_move(self, ctx, distance):
        if str(ctx.message.channel.type).lower() == "private":
            return
        true_distance = int(distance)
        name = ctx.message.author.name
        if true_distance > 150:
            await ctx.send("sorry but it cannot be over 150 millimeters")
            return
        def cozmo_program(robot : cozmo.robot.Robot):
            if robot.is_on_charger:
                robot.stop_all_motors
            else:
                robot.say_text(name + "made me move" + distance + "millimeters").wait_for_completed()
                robot.drive_straight(distance_mm(true_distance), speed_mmps(50)).wait_for_completed()
        try:
            cozmo.robot.Robot.drive_off_charger_on_connect = False
            cozmo.run_program(cozmo_program)
        except:
            await ctx.send(f"{ctx.message.author.mention} sorry but the robot is offline :pensive:")
        return
    @robot_move.error
    async def robot_move_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"sorry but you're on cooldown for {error.retry_after:,.f} seconds", delete_after=error.retry_after)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def robot_say(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        async with ctx.message.channel.typing():
            name = ctx.message.author.name
            def cozmo_program(cozmo : cozmo.robot.Robot):
                message_to_send = ctx.message.content[11:]
                cozmo.say_text(f"{(name)} said: " + message_to_send).wait_for_completed()

            try:
                cozmo.robot.Robot.drive_off_charger_on_connect = False
                cozmo.run_program(cozmo_program)
            except:
                await ctx.send(f"{ctx.message.author.mention} sorry but the robot is offline")
                return
        await ctx.send(f"{ctx.message.author.mention}, the robot succeeded in this action!")
    @robot_say.error
    async def robot_say_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(content=f"{ctx.message.author.mention} you're on cooldown for {error.retry_after:,.2f} seconds", delete_after=error.retry_after)
        return


    @cooldown(1, 60)
    @commands.command()
    async def robot_check(self, ctx):
        if str(ctx.message.channel.type).lower() == "private":
            return
        await ctx.send("checking...")
        def check_for_wiki(robot: cozmo.robot.Robot):
            async def start_program():
                #this to start ajusting if the robot is doing something that go against this command
                robot.move_lift(-3)
                robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

                face_to_follow = None

                while True:
                    if face_to_follow:
                        # start turning towards the face
                        await ctx.send("wiki is at his desk! :D")
                        break

                    if not (face_to_follow and face_to_follow.is_visible):
                        # find a visible face, timeout if nothing found after a short while
                        try:
                            face_to_follow = robot.world.wait_for_observed_face(timeout=10)
                        except asyncio.TimeoutError:
                            await ctx.send("I couldn't find wiki at his desk D:")
                            break

                    await asyncio.sleep(.1)
            start_program()
        cozmo.run_program(check_for_wiki)
        return
    @robot_check.error
    async def robot_check_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f'sorry {ctx.message.author.mention} but you\'re on cooldown for {error.retry_after:,.f}')
        return


def setup(client):
    client.add_cog(Robot(client))
