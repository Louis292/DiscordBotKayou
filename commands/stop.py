import discord
from discord.ext import commands

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop')
    async def stop(self, ctx):
        voice_client = ctx.voice_client

        if voice_client:
            voice_client.stop()
            await voice_client.disconnect()
            embed = discord.Embed(
                title="Arrêt",
                description="La musique a été arrêtée et le bot a quitté le canal vocal.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Le bot n'est pas dans un canal vocal.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Stop chargée")
    await bot.add_cog(Stop(bot))
