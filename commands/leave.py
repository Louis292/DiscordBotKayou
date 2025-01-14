import discord
from discord.ext import commands

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leave')
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Bot déconnecté du canal vocal !")
        else:
            await ctx.send("Le bot n'est pas dans un canal vocal.")

# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Leave chargée")
    await bot.add_cog(Leave(bot))
