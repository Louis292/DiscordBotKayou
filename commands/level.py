import discord
from discord.ext import commands
import json
import os

LEVEL_FILE = 'levels.json'

# Charger les niveaux depuis le fichier JSON
def load_levels():
    if os.path.exists(LEVEL_FILE):
        with open(LEVEL_FILE, 'r') as file:
            return json.load(file)
    return {}

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='level')
    async def level(self, ctx):
        levels = load_levels()
        user_id = str(ctx.author.id)
        level = levels.get(user_id, 0)

        embed = discord.Embed(
            title="Ton Niveau",
            description=f'{ctx.author.mention}, tu as envoyé : **{level}** messages.',
            color=discord.Color.green()  # Couleur verte
        )

        await ctx.reply(embed=embed)

async def setup(bot):
    print("Extension Level chargée")
    await bot.add_cog(Level(bot))
