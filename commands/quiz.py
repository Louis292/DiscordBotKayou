import discord
from discord.ext import commands
import random
import asyncio
import json
import os

# Chemin vers le fichier questions_reponses.json
QUESTIONS_FILE = './questions_reponses.json'
SCORE_FILE = './score.json'

# Fonction pour charger les questions depuis questions_reponses.json
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Fonction pour charger les scores depuis score.json
def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Fonction pour sauvegarder les scores dans score.json
def save_scores(scores):
    with open(SCORE_FILE, 'w') as file:
        json.dump(scores, file, indent=4)

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = load_questions()  # Charger les questions depuis le fichier JSON
        self.scores = load_scores()  # Charger les scores depuis le fichier JSON
        self.current_question = None
        self.current_answer = None

    @commands.command(name='quiz')
    async def quiz(self, ctx):
        if not self.questions:
            await ctx.send("Le fichier des questions est vide ou introuvable.")
            return

        # Sélectionner une question aléatoire
        question, answer = random.choice(list(self.questions.items()))
        self.current_question = question
        self.current_answer = answer.lower()

        # Envoyer la question dans un embed
        embed = discord.Embed(
            title="Quiz",
            description=f"Question: {question}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

        def check(m):
            # Vérifier si le message est une réponse correcte et provient du même canal
            return m.channel == ctx.channel and m.content.lower() == self.current_answer

        try:
            # Attendre la réponse correcte pendant 30 secondes
            msg = await self.bot.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            # Temps écoulé sans bonne réponse
            embed = discord.Embed(
                title="Temps écoulé",
                description=f"Personne n'a trouvé la bonne réponse. La réponse était : **{self.current_answer.capitalize()}**",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            # Réponse correcte trouvée
            player = msg.author

            # Ajouter le joueur aux scores ou augmenter son score
            player_id = str(player.id)
            if player_id not in self.scores:
                self.scores[player_id] = 0
            self.scores[player_id] += 1

            # Sauvegarder les scores dans score.json
            save_scores(self.scores)

            embed = discord.Embed(
                title="Bonne réponse!",
                description=f"Félicitations {player.mention}, tu as trouvé la bonne réponse!\n**Score actuel : {self.scores[player_id]}**",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @commands.command(name='score')
    async def score(self, ctx, member: discord.Member = None):
        """Afficher le score d'un joueur (ou du joueur courant s'il n'y a pas de membre spécifié)"""
        if member is None:
            member = ctx.author

        player_id = str(member.id)
        score = self.scores.get(player_id, 0)

        embed = discord.Embed(
            title=f"Score de {member.display_name}",
            description=f"**{score}** points",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @commands.command(name='quiz_top')
    async def quiz_top(self, ctx):
        """Afficher les joueurs avec les meilleurs scores"""
        if not self.scores:
            await ctx.send("Aucun score enregistré pour le moment.")
            return

        # Trier les scores par ordre décroissant
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)

        # Créer un embed pour afficher les meilleurs scores
        embed = discord.Embed(
            title="Top des Joueurs au Quiz",
            description="Voici les joueurs avec les meilleurs scores :",
            color=discord.Color.gold()
        )

        # Ajouter les scores aux champs de l'embed
        for i, (player_id, score) in enumerate(sorted_scores[:10], 1):
            player = ctx.guild.get_member(int(player_id))
            player_name = player.display_name if player else "Inconnu"
            embed.add_field(name=f"{i}. {player_name}", value=f"{score} points", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    print("Extension Quiz chargée")
    await bot.add_cog(Quiz(bot))
