import discord
from discord.ext import commands
import yt_dlp
import os

# Dossier de téléchargement
MUSIC_FOLDER = './musique'

# Assurer que le dossier musique existe
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

# Configuration du chemin relatif de ffmpeg
FFMPEG_LOCATION = '/usr/bin/ffmpeg'  # Chemin absolu vers ffmpeg

# Fonction pour créer des embeds
def create_embed(title, description, color=0x00FF00):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

class Download(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='download')
    async def download(self, ctx, *, query: str):
        embed = create_embed("Téléchargement", f"Téléchargement de la musique pour : {query}")
        await ctx.send(embed=embed)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(MUSIC_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'ffmpeg_location': FFMPEG_LOCATION,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(query, download=False)
                file_title = info_dict.get('title', None)
                file_name = f"{file_title}.mp3"
                file_path = os.path.join(MUSIC_FOLDER, file_name)

                if os.path.exists(file_path):
                    embed = create_embed("Fichier Déjà Présent",
                                         f"Le fichier **{file_name}** existe déjà dans {MUSIC_FOLDER}.")
                    await ctx.send(embed=embed)
                else:
                    ydl.download([query])
                    embed = create_embed("Téléchargement Réussi",
                                         f"Musique **{file_name}** téléchargée et stockée dans {MUSIC_FOLDER}.")
                    await ctx.send(embed=embed)
            except Exception as e:
                embed = create_embed("Erreur", f"Une erreur est survenue : {str(e)}", color=0xFF0000)
                await ctx.send(embed=embed)

# Fonction setup asynchrone pour ajouter le Cog au bot
async def setup(bot):
    print("Extension Download chargée")
    await bot.add_cog(Download(bot))
