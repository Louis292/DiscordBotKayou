import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Helper function to create or get the "Muted" role
    async def get_or_create_muted_role(self, guild: discord.Guild):
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if not muted_role:
            muted_role = await guild.create_role(
                name="Muted", 
                reason="Création du rôle pour muter les membres"
            )
            for channel in guild.channels:
                # Bloquer les permissions textuelles et vocales dans chaque salon
                await channel.set_permissions(muted_role, 
                    send_messages=False, 
                    speak=False, 
                    connect=False
                )
        return muted_role

    @commands.command()
    @commands.has_permissions(manage_roles=True)  # Nécessite la permission de gérer les rôles
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if not member:
            await ctx.send(embed=discord.Embed(
                description="Vous devez spécifier un utilisateur à mute.",
                color=discord.Color.red()
            ))
            return

        if member == ctx.author:
            await ctx.send(embed=discord.Embed(
                description="Vous ne pouvez pas vous mute vous-même.",
                color=discord.Color.red()
            ))
            return

        muted_role = await self.get_or_create_muted_role(ctx.guild)

        try:
            await member.add_roles(muted_role, reason=reason)
            await ctx.send(embed=discord.Embed(
                description=f"{member.mention} a été mute pour: {reason if reason else 'aucune raison donnée'}.",
                color=discord.Color.green()
            ))
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description="Je n'ai pas les permissions pour mute cet utilisateur.",
                color=discord.Color.red()
            ))

async def setup(bot):
    print("Extension Mute chargée")
    await bot.add_cog(Mute(bot))
