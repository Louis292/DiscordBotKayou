import discord
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload')
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx):
        # Lister les extensions actuellement chargées
        extensions = list(self.bot.cogs.keys())

        if not extensions:
            embed = discord.Embed(
                title="Reload",
                description="Aucune extension à recharger.",
                color=discord.Color.green()  # Couleur verte
            )
            await ctx.send(embed=embed)
            return

        # Recharger toutes les extensions
        for extension in extensions:
            try:
                self.bot.unload_extension(f'commands.{extension}')
                self.bot.load_extension(f'commands.{extension}')
                print(f"Extension '{extension}' rechargée.")
                embed = discord.Embed(
                    title="Reload",
                    description=f"Extension '{extension}' rechargée.",
                    color=discord.Color.green()  # Couleur verte
                )
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Erreur",
                    description=f"Erreur lors du rechargement de l'extension '{extension}': {e}",
                    color=discord.Color.red()  # Couleur rouge pour les erreurs
                )
                await ctx.send(embed=embed)
        
        embed = discord.Embed(
            title="Reload",
            description="Toutes les extensions ont été rechargées.",
            color=discord.Color.green()  # Couleur verte
        )
        await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Reload chargée")
    await bot.add_cog(Reload(bot))
