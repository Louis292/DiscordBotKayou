import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    async def clear(self, ctx, amount: int = None):
        # Vérifier si l'utilisateur a répondu à un message
        if ctx.message.reference:
            # Récupérer le message auquel l'utilisateur a répondu
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

            if ctx.message.content.strip() == "!clear *":
                # Supprimer tous les messages entre le message auquel l'utilisateur a répondu et le message actuel
                await ctx.message.delete()  # Supprimer la commande elle-même

                # Récupérer les messages à partir de celui auquel on a répondu jusqu'au plus récent
                def check(message):
                    return message.created_at > replied_message.created_at

                deleted = await ctx.channel.purge(limit=None, check=check)

                await ctx.send(f"{len(deleted)} messages ont été supprimés.", delete_after=5)
            else:
                # Supprimer uniquement le message auquel l'utilisateur a répondu
                await ctx.message.delete()  # Supprimer la commande elle-même
                await replied_message.delete()
                await ctx.send("Le message auquel vous avez répondu a été supprimé.", delete_after=5)
        else:
            # Vérifier si un montant de messages est fourni et est supérieur à 0
            if amount is None or amount <= 0:
                await ctx.send("Le nombre de messages à supprimer doit être supérieur à 0.", delete_after=5)
                return

            # Supprimer les messages normalement en fonction du montant fourni
            deleted = await ctx.channel.purge(limit=amount)
            await ctx.send(f"{len(deleted)} messages ont été supprimés.", delete_after=5)

# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Clear chargée")
    await bot.add_cog(Clear(bot))
