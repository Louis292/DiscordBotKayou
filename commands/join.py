import discord
from discord.ext import commands

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                # Le bot est déjà connecté à un canal vocal
                await ctx.voice_client.move_to(channel)
                await ctx.send("Bot déplacé vers le canal vocal !")
            else:
                # Le bot n'est pas encore connecté
                await channel.connect()
                await ctx.send("Bot connecté au canal vocal !")
        else:
            await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")

# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Join chargée")
    await bot.add_cog(Join(bot))
