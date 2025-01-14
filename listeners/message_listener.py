import discord
from discord.ext import commands
import json
import os
import datetime
import uuid  # Pour générer des identifiants uniques


class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remplacez 'YOUR_CHANNEL_ID' par l'ID du salon où vous voulez envoyer les messages
        self.logging_channel_id = 1285552665274875926
        self.level_file = 'levels.json'
        
        # Utiliser un partage SMB monté pour stocker les fichiers
        self.files_folder = './files'
        if not os.path.exists(self.files_folder):
            os.makedirs(self.files_folder)

        # Charger les niveaux depuis le fichier JSON
        self.levels = self.load_levels()

    def load_levels(self):
        if os.path.exists(self.level_file):
            with open(self.level_file, 'r') as file:
                return json.load(file)
        return {}

    def save_levels(self):
        with open(self.level_file, 'w') as file:
            json.dump(self.levels, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorer les messages du bot lui-même pour éviter une boucle infinie
        if message.author == self.bot.user:
            return

        # Récupérer le salon de log
        logging_channel = self.bot.get_channel(self.logging_channel_id)
        if logging_channel:
            # Créer un embed
            embed = discord.Embed(
                title="Nouveau Message",
                description=f"Message de {message.author} dans {message.channel}:\n``{message.content}``",
                color=discord.Color.green()  # Couleur verte
            )

            # Ajouter la date et l'heure de l'envoi
            timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            embed.set_footer(text=f"Envoyé le {timestamp} UTC")

            # Sauvegarder les fichiers joints avec un nom unique
            if message.attachments:
                file_paths = []
                for attachment in message.attachments:
                    # Générer un nom unique pour chaque fichier
                    unique_id = str(uuid.uuid4())  # Générer un identifiant unique
                    file_extension = os.path.splitext(attachment.filename)[1]  # Récupérer l'extension du fichier
                    unique_filename = f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{unique_id}{file_extension}"
                    file_path = os.path.join(self.files_folder, unique_filename)
                    
                    # Sauvegarder le fichier avec un nom unique
                    await attachment.save(file_path)
                    file_paths.append(file_path)

                # Ajouter les fichiers à l'embed si présents
                if file_paths:
                    file_list = '\n'.join([f"[{os.path.basename(path)}]({path})" for path in file_paths])
                    embed.add_field(name="Fichiers joints", value=file_list, inline=False)

            # Envoyer l'embed dans le salon de log
            await logging_channel.send(embed=embed)

        # Mise à jour du niveau de l'utilisateur
        user_id = str(message.author.id)
        if user_id in self.levels:
            self.levels[user_id] += 1
        else:
            self.levels[user_id] = 1
        self.save_levels()


async def setup(bot):
    print("Extension MessageListener chargée")
    await bot.add_cog(MessageListener(bot))
