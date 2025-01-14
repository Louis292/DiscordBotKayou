import discord
from discord.ext import commands
import os

MUSIC_FOLDER = './musique'

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remove')
    async def remove(self, ctx, *, query: str):
        global playlist
        musiques = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]
        if query.isdigit():
            index = int(query) - 1
            if 0 <= index < len(musiques):
                file_path = os.path.join(MUSIC_FOLDER, musiques[index])
                if file_path in playlist:
                    playlist.remove(file_path)
                    embed = discord.Embed(
                        title="Retiré",
                        description=f"La musique **{os.path.basename(file_path)}** a été retirée de la playlist.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Erreur",
                        description="La musique n'est pas dans la playlist.",
                        color=0xFF0000
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Erreur",
                    description="Chiffre de musique invalide.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Le format du chiffre est invalide.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Remove chargée")
    await bot.add_cog(Remove(bot))
