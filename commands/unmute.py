import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)  # Nécessite la permission de gérer les rôles
    async def unmute(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send(embed=discord.Embed(
                description="Vous devez spécifier un utilisateur à unmute.",
                color=discord.Color.red()
            ))
            return

        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            await ctx.send(embed=discord.Embed(
                description="Le rôle 'Muted' n'existe pas.",
                color=discord.Color.red()
            ))
            return

        if muted_role not in member.roles:
            await ctx.send(embed=discord.Embed(
                description=f"{member.mention} n'est pas mute.",
                color=discord.Color.orange()
            ))
            return

        try:
            await member.remove_roles(muted_role, reason="Unmute manuel")
            await ctx.send(embed=discord.Embed(
                description=f"{member.mention} a été unmute.",
                color=discord.Color.green()
            ))
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description="Je n'ai pas les permissions pour unmute cet utilisateur.",
                color=discord.Color.red()
            ))

async def setup(bot):
    print("Extension Unmute chargée")
    await bot.add_cog(Unmute(bot))
