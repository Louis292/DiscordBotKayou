import discord
from discord.ext import commands

class StatusListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Définir le statut du bot
        await self.bot.change_presence(activity=discord.Game(name="KAYOU"))

        print(f'{self.bot.user} est connecté et prêt.')

async def setup(bot):
    print("Extension StatusListeners chargées")
    await bot.add_cog(StatusListener(bot))
