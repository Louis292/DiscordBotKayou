import discord
from discord.ext import commands
import os


class TempVoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # ID du salon vocal spécifique où les salons temporaires seront créés
        self.trigger_channel_id = 1292407125699461174  # Remplacez par l'ID du salon vocal spécifique
        self.temp_channels = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Si un membre rejoint le salon vocal spécifique
        if after.channel and after.channel.id == self.trigger_channel_id:
            # Créer un nouveau salon vocal temporaire
            guild = after.channel.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=True),  # Empêche tout le monde de rejoindre
                member: discord.PermissionOverwrite(
                    view_channel=True,
                    mute_members=True,     # Permet de mute les autres utilisateurs dans le salon
                    deafen_members=True,   # Permet de mettre en sourdine les autres utilisateurs
                    move_members=True      # Permet de kick/move des utilisateurs
                )
            }

            temp_channel = await guild.create_voice_channel(
                name=f"🎙️・𝗦𝗮𝗹𝗼𝗻・𝗗𝗲・{member.display_name}",
                category=after.channel.category,  # Le salon est créé dans la même catégorie
                overwrites=overwrites  # Appliquer les permissions spécifiées
            )

            # Déplacer le membre dans ce nouveau salon vocal
            await member.move_to(temp_channel)

            # Stocker l'ID du créateur pour surveiller les départs
            self.temp_channels[temp_channel.id] = member.id

        # Si un membre quitte un salon vocal
        if before.channel and before.channel.id in self.temp_channels:
            temp_channel_id = before.channel.id

            # Vérifier si le créateur du salon a quitté et si le salon est vide
            if len(before.channel.members) == 0:
                # Supprimer le salon vocal temporaire
                await before.channel.delete()
                del self.temp_channels[temp_channel_id]


async def setup(bot):
    print("Extension TempVoiceChannels chargée")
    await bot.add_cog(TempVoiceChannels(bot))
