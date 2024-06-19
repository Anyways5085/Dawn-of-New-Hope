from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test") #simple test command.
    async def test(self, ctx, content='test'):
        await ctx.send(content)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.read:
            self.bot.cogs_ready.ready_up("fun")
        

def setup(bot):
    bot.add_cog(Fun(bot))