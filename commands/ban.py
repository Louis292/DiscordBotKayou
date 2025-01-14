import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)  # Nécessite la permission de bannir
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if not member:
            await ctx.send(embed=discord.Embed(
                description="Vous devez spécifier un utilisateur à bannir.",
                color=discord.Color.red()
            ))
            return
        
        if member == ctx.author:
            await ctx.send(embed=discord.Embed(
                description="Vous ne pouvez pas vous bannir vous-même.",
                color=discord.Color.red()
            ))
            return
        
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=discord.Embed(
                description=f"{member.mention} a été banni pour: {reason if reason else 'aucune raison donnée'}.",
                color=discord.Color.green()
            ))
        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description="Je n'ai pas les permissions pour bannir cet utilisateur.",
                color=discord.Color.red()
            ))

    @commands.command()
    @commands.has_permissions(ban_members=True)  # Nécessite la permission de débannir
    async def unban(self, ctx, *, member_name: str = None):
        if not member_name:
            await ctx.send(embed=discord.Embed(
                description="Vous devez spécifier un utilisateur à débannir.",
                color=discord.Color.red()
            ))
            return

        banned_users = await ctx.guild.bans()
        member_name_lower = member_name.lower()

        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name.lower() == member_name_lower or f"{user.name.lower()}#{user.discriminator}" == member_name_lower:
                await ctx.guild.unban(user)
                await ctx.send(embed=discord.Embed(
                    description=f"{user.mention} a été débanni.",
                    color=discord.Color.green()
                ))
                return

        await ctx.send(embed=discord.Embed(
            description=f"Le membre `{member_name}` n'a pas été trouvé dans la liste des bannis.",
            color=discord.Color.red()
        ))

async def setup(bot):
    print("Extension Ban/Unban chargée")
    await bot.add_cog(Ban(bot))
