import discord
from discord.ext import commands
import os
import random

MUSIC_FOLDER = './musique'
FFMPEG_LOCATION = '/usr/bin/ffmpeg'  # Chemin absolu vers ffmpeg

# Playlist pour stocker les musiques à jouer
playlist = []
current_music_index = 0  # Pour suivre l'index de la musique en cours

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play')
    async def play(self, ctx, *, query: str = None):
        global playlist, current_music_index

        musiques = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]

        if query:
            try:
                index = int(query) - 1
                if 0 <= index < len(musiques):
                    file_path = os.path.join(MUSIC_FOLDER, musiques[index])
                    playlist = [file_path]
                    current_music_index = index

                    if ctx.voice_client is None:
                        if ctx.author.voice:
                            channel = ctx.author.voice.channel
                            await channel.connect()
                            print(f"Bot has connected to {channel}.")
                        else:
                            embed = discord.Embed(
                                title="Erreur",
                                description="Vous devez être dans un canal vocal pour jouer de la musique.",
                                color=0xFF0000
                            )
                            await ctx.send(embed=embed)
                            return

                    voice_client = ctx.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()

                    print(f"Playing file: {file_path}")
                    voice_client.play(discord.FFmpegPCMAudio(file_path, executable=FFMPEG_LOCATION))
                    embed = discord.Embed(
                        title="Lecture",
                        description=f"Lecture de **{os.path.basename(file_path)}**.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Erreur",
                        description="Chiffre de musique invalide.",
                        color=0xFF0000
                    )
                    await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(
                    title="Erreur",
                    description="Le format du chiffre est invalide.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
        else:
            if musiques:
                playlist = [os.path.join(MUSIC_FOLDER, m) for m in musiques]
                current_music_index = 0  # Réinitialiser l'index

                if ctx.voice_client is None:
                    if ctx.author.voice:
                        channel = ctx.author.voice.channel
                        await channel.connect()
                        print(f"Bot has connected to {channel}.")
                    else:
                        embed = discord.Embed(
                            title="Erreur",
                            description="Vous devez être dans un canal vocal pour jouer de la musique.",
                            color=0xFF0000
                        )
                        await ctx.send(embed=embed)
                        return

                await self.play_random_music(ctx)
            else:
                embed = discord.Embed(
                    title="Erreur",
                    description="Aucune musique trouvée dans le dossier.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)

    async def play_random_music(self, ctx):
        global playlist, current_music_index
        if playlist:
            voice_client = ctx.voice_client

            if voice_client is None:
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    voice_client = await channel.connect()

            if voice_client.is_playing():
                voice_client.stop()

            file_path = playlist[current_music_index]
            current_music_index = (current_music_index + 1) % len(playlist)

            voice_client.play(discord.FFmpegPCMAudio(file_path, executable=FFMPEG_LOCATION),
                              after=lambda e: self.bot.loop.create_task(self.play_random_music(ctx)))

            embed = discord.Embed(
                title="Lecture Aléatoire",
                description=f"Lecture de **{os.path.basename(file_path)}**.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Aucune musique trouvée dans le dossier.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Passe à la musique suivante dans la playlist."""
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await self.play_random_music(ctx)
            embed = discord.Embed(
                title="Skip",
                description="Musique suivante jouée.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Aucune musique n'est en cours de lecture.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @commands.command(name='musique')
    async def musique(self, ctx):
        """Affiche la liste des musiques disponibles avec leur numéro."""
        musiques = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]
        if musiques:
            description = "\n".join([f"{i+1}. {m}" for i, m in enumerate(musiques)])
            embed = discord.Embed(
                title="Liste des Musiques",
                description=description,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description="Aucune musique trouvée dans le dossier.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)


async def setup(bot):
    print("Extension Play chargée")
    await bot.add_cog(Play(bot))
