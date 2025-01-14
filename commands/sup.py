import discord
from discord.ext import commands

class Sup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sup")
    async def sup(self, ctx):
        # Vérifier si le message est une réponse
        if ctx.message.reference is not None:
            # Récupérer le message référencé
            message_reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            
            # Obtenir tous les messages dans le canal
            messages = await ctx.channel.history(limit=None).flatten()
            messages_to_delete = []

            # Collecter les messages à supprimer
            for message in messages:
                # Vérifier si le message est entre le message référencé et le message envoyé
                if message.created_at > message_reference.created_at and message.id != ctx.message.id:
                    messages_to_delete.append(message)

            # Supprimer les messages collectés
            if messages_to_delete:
                # Limiter le nombre de messages à supprimer à 100, car Discord a une limite
                await ctx.channel.delete_messages(messages_to_delete[:100])
                
                # Créer un embed pour confirmer la suppression
                embed = discord.Embed(
                    title="Messages supprimés",
                    description=f"{len(messages_to_delete)} messages ont été supprimés.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                # Pas de messages à supprimer
                embed = discord.Embed(
                    title="Aucun message à supprimer",
                    description="Il n'y a pas de messages à supprimer entre le message référencé et le vôtre.",
                    color=discord.Color.yellow()
                )
                await ctx.send(embed=embed)
        else:
            # Embed rouge pour les erreurs
            embed = discord.Embed(
                title="Erreur",
                description="Vous devez répondre à un message pour utiliser cette commande.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Sup chargée")
    await bot.add_cog(Sup(bot))
