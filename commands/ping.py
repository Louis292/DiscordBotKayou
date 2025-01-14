import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        # Vérifier si l'utilisateur a la permission de gérer le serveur
        if ctx.author.guild_permissions.manage_guild:
            latency = round(self.bot.latency * 1000)  # Latency en millisecondes

            # Créer un embed bleu avec le message de ping
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Le ping du bot est de **{latency}ms**.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            # Embed rouge pour les erreurs de permissions
            embed = discord.Embed(
                title="Permission refusée",
                description="Vous n'avez pas la permission de gérer le serveur.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Ping chargée")
    await bot.add_cog(Ping(bot))
