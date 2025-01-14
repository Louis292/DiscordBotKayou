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

class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='top')
    async def top(self, ctx):
        levels = load_levels()
        sorted_users = sorted(levels.items(), key=lambda x: x[1], reverse=True)
        top_list = [f'<@{user_id}>: {level} messages' for user_id, level in sorted_users[:10]]

        embed = discord.Embed(
            title="Classement des Top Utilisateurs",
            description='\n'.join(top_list),
            color=discord.Color.green()  # Couleur verte
        )

        await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Top chargée")
    await bot.add_cog(Top(bot))
