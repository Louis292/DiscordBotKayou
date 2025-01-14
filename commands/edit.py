import discord
from discord.ext import commands

class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='edit')
    async def edit(self, ctx, *, new_content: str):
        # Vérifier si le message auquel on répond est d'un bot
        if ctx.message.reference:
            original_message_id = ctx.message.reference.message_id
            original_message = await ctx.channel.fetch_message(original_message_id)

            if original_message.author == self.bot.user:
                # Modifier le message
                await original_message.edit(content=new_content)
                embed = discord.Embed(
                    title="Message Modifié",
                    description=f"Le message a été modifié avec succès.",
                    color=discord.Color.green()  # Couleur verte
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Erreur",
                    description="Vous devez répondre à un message du bot pour le modifier.",
                    color=discord.Color.red()  # Couleur rouge pour les erreurs
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Vous devez répondre à un message du bot pour le modifier.",
                color=discord.Color.red()  # Couleur rouge pour les erreurs
            )
            await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Edit chargée")
    await bot.add_cog(Edit(bot))
