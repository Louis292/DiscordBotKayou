import discord
from discord.ext import commands
import os

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Assurer que le répertoire 'files' existe
        if not os.path.exists('files'):
            os.makedirs('files')

    @commands.command()
    async def say(self, ctx, *, message: str = None):
        await ctx.message.delete()  # Supprimer le message d'origine

        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file_path = os.path.join('files', attachment.filename)
                try:
                    await attachment.save(file_path)
                    await ctx.send(file=discord.File(file_path))
                except discord.errors.NotFound:
                    await ctx.send("Le fichier n'a pas pu être trouvé.")

        if message:
            if ctx.message.reference:
                replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                await replied_message.reply(message)
            else:
                await ctx.send(message)

async def setup(bot):
    print("Extension Say chargée")
    await bot.add_cog(Say(bot))
