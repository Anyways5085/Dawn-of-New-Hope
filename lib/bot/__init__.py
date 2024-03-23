from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord.ext.commands import CommandNotFound
from glob import glob
from ..db import db
import random

PREFIX = "d!"
OWNER_IDS = [592619320421384232]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cog/*.py")]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix = PREFIX, 
            owner_ids = OWNER_IDS, 
            intents = Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        self.setup()
        print("running setup...")

        with open("lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.scheduler.start()

            print(f'Logged in as {bot.user} (ID: {bot.user.id})')
            print('------')

            channel = self.get_channel(1196264790490886264)
            await channel.send(f'Logged in as {bot.user} (ID: {bot.user.id})')

        else:
            print(f'Reconnected as {bot.user} (ID: {bot.user.id})')
            print('------')

    async def on_disconnect(self):
        print("bot disconnected")

    #error
    async def on_command_error(self,ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        
        elif hasattr(exc,"original"):
            raise exc.original
        
        else:
            raise exc

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        raise

    
    async def on_message(self,message):
        pass

# commands


# @Bot.command(pass_context=True) # transfur command.
# async def transfur(ctx):
#     required_role = discord.utils.get(ctx.guild.roles, name="FirstAttitude")  #role check.
#     target_role = discord.utils.get(ctx.guild.roles, name="The Council")      # find target role

#     if required_role not in ctx.author.roles:
#         await ctx.send(f"you cant do that mate.")
#     else:
#         if target_role in ctx.author.roles:
#             await ctx.author.remove_roles(target_role)
#             await ctx.send(f"transfurred back to normal.")
#         else:
#             await ctx.author.add_roles(target_role)
#             await ctx.send(f"you have transfurred to {target_role}.")

# @Bot.command()  #return server ID
# async def serverid(ctx):
#   serverId = ctx.message.guild.id
#   await ctx.send(serverId)

# @Bot.command() #simple test command.
# async def test(ctx, content='test'):
#     await ctx.send(content)

# @Bot.command() #vip server command.
# async def vip(ctx,):
#     await ctx.send("Vip Server owned by wolf.\nhttps://www.roblox.com/games/166986752?privateServerLinkCode=38028909888988386962674670711828")

bot = Bot()