import discord
from discord.ext import commands

class CountMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def countmessages(self, ctx):
        if not ctx.message.reference:
            await ctx.send(embed=discord.Embed(
                description="Vous devez répondre à un message pour utiliser cette commande.",
                color=discord.Color.red()
            ))
            return

        # Récupérer le message auquel l'utilisateur a répondu
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        # Initialiser le compteur de messages
        message_count = 0
        
        # Parcourir l'historique des messages depuis celui auquel on a répondu
        async for message in ctx.channel.history(after=replied_message, oldest_first=True):
            message_count += 1
        
        # Envoyer le nombre de messages comptés
        await ctx.send(embed=discord.Embed(
            description=f"Il y a eu {message_count} messages depuis celui auquel vous avez répondu.",
            color=discord.Color.green()
        ))

async def setup(bot):
    print("Extension CountMessages chargée")
    await bot.add_cog(CountMessages(bot))
