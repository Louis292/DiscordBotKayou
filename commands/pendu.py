import discord
from discord.ext import commands
import random

class Pendu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mots = self.lire_mots_depuis_fichier('liste.txt')
        self.partie_en_cours = False
        self.mot_a_deviner = ""
        self.lettres_trouvees = set()
        self.lettres_tentees = set()
        self.essais_max = 10
        self.essais_restants = self.essais_max

    def lire_mots_depuis_fichier(self, fichier):
        try:
            with open(fichier, 'r') as f:
                mots = f.read().splitlines()
            return mots
        except FileNotFoundError:
            print(f"Erreur : Le fichier {fichier} n'a pas été trouvé.")
            return []

    def choisir_mot(self):
        if self.mots:
            return random.choice(self.mots).lower()
        else:
            return None

    def afficher_mot_actuel(self):
        if not self.mot_a_deviner:
            return None
        # Remplacer les lettres non trouvées par des underscores
        return ' '.join([lettre if lettre in self.lettres_trouvees else '_' for lettre in self.mot_a_deviner])

    @commands.command(name="pendu")
    async def commencer_pendu(self, ctx):
        """Commande pour commencer une nouvelle partie de pendu."""
        if self.partie_en_cours:
            await ctx.send("Une partie est déjà en cours !")
            return

        self.mot_a_deviner = self.choisir_mot()
        
        if not self.mot_a_deviner:
            await ctx.send("Erreur : Aucun mot disponible dans la liste pour commencer le jeu.")
            return

        self.lettres_trouvees.clear()
        self.lettres_tentees.clear()
        self.essais_restants = self.essais_max
        self.partie_en_cours = True

        embed = discord.Embed(title="Pendu", description="Une nouvelle partie commence !", color=discord.Color.blue())
        embed.add_field(name="Mot à deviner", value=self.afficher_mot_actuel(), inline=False)
        embed.add_field(name="Essais restants", value=str(self.essais_restants), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="deviner")
    async def deviner_lettre(self, ctx, lettre: str):
        """Commande pour deviner une lettre."""
        if not self.partie_en_cours:
            await ctx.send("Aucune partie en cours. Utilisez `!pendu` pour en commencer une.")
            return

        lettre = lettre.lower()

        if lettre in self.lettres_tentees:
            await ctx.send(f"La lettre `{lettre}` a déjà été tentée.")
            return

        self.lettres_tentees.add(lettre)

        if lettre in self.mot_a_deviner:
            self.lettres_trouvees.add(lettre)
            await ctx.send(f"Bien joué ! La lettre `{lettre}` est dans le mot.")
        else:
            self.essais_restants -= 1
            await ctx.send(f"Mauvais choix. La lettre `{lettre}` n'est pas dans le mot.")

        if all(l in self.lettres_trouvees for l in self.mot_a_deviner):
            embed = discord.Embed(title="Victoire", description=f"Félicitations ! Le mot était : **{self.mot_a_deviner}**", color=discord.Color.green())
            self.partie_en_cours = False
        elif self.essais_restants <= 0:
            embed = discord.Embed(title="Défaite", description=f"Dommage, le mot était : **{self.mot_a_deviner}**", color=discord.Color.red())
            self.partie_en_cours = False
        else:
            embed = discord.Embed(title="Pendu", description="Continuez à deviner les lettres !", color=discord.Color.blue())
            embed.add_field(name="Mot à deviner", value=self.afficher_mot_actuel(), inline=False)
            embed.add_field(name="Essais restants", value=str(self.essais_restants), inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(name="arreter_pendu")
    async def arreter_pendu(self, ctx):
        """Commande pour arrêter la partie en cours."""
        if not self.partie_en_cours:
            await ctx.send("Aucune partie de pendu en cours.")
        else:
            self.partie_en_cours = False
            await ctx.send(f"Partie de pendu annulée. Le mot était : **{self.mot_a_deviner}**")

# Ajout du cog au bot
async def setup(bot):
    await bot.add_cog(Pendu(bot))
