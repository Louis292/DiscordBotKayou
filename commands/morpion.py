import discord
from discord.ext import commands
import random

class Morpion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.board = [":white_large_square:"] * 9  # Plateau de jeu
        self.current_player = "X"  # Le joueur commence toujours

    # Fonction pour afficher le plateau
    def format_board(self):
        board = ""
        for i in range(0, 9, 3):
            board += "".join(self.board[i:i + 3]) + "\n"
        return board

    # Fonction pour vérifier si quelqu'un a gagné
    def check_winner(self, player):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Lignes
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colonnes
            (0, 4, 8), (2, 4, 6)              # Diagonales
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] != ":white_large_square:":
                return True
        return False

    # Fonction pour vérifier si le plateau est plein
    def is_board_full(self):
        return ":white_large_square:" not in self.board

    # Fonction pour jouer un coup
    async def play_turn(self, ctx, pos, player):
        if self.board[pos] == ":white_large_square:":
            if player == "X":
                self.board[pos] = ":regional_indicator_x:"
            else:
                self.board[pos] = ":o2:"
            return True
        return False

    # Fonction pour le coup du bot avec l'algorithme Minimax
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(":regional_indicator_x:"):
            return -10
        if self.check_winner(":o2:"):
            return 10
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ":white_large_square:":
                    board[i] = ":o2:"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ":white_large_square:"
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ":white_large_square:":
                    board[i] = ":regional_indicator_x:"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ":white_large_square:"
                    best_score = min(score, best_score)
            return best_score

    async def bot_turn(self):
        best_move = None
        best_score = -float('inf')
        for i in range(9):
            if self.board[i] == ":white_large_square:":
                self.board[i] = ":o2:"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ":white_large_square:"
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            self.board[best_move] = ":o2:"
        return best_move

    @commands.command()
    async def morpion(self, ctx):
        self.board = [":white_large_square:"] * 9  # Réinitialiser le plateau
        self.current_player = "X"  # Le joueur commence toujours

        # Envoyer l'état initial du plateau
        board_message = await ctx.send(embed=self.create_embed("À toi de jouer!", self.format_board()))

        # Ajouter des réactions d'emoji pour les choix
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        for emoji in emojis:
            await board_message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis

        # Boucle de jeu
        while True:
            try:
                # Attendre que le joueur réagisse
                reaction, user = await self.bot.wait_for('reaction_add', check=check)

                # Traduire l'emoji en position sur le plateau
                pos = emojis.index(str(reaction.emoji))

                # Jouer le coup du joueur
                if await self.play_turn(ctx, pos, "X"):
                    await board_message.edit(embed=self.create_embed(f"Ton coup", self.format_board()))
                    await board_message.clear_reaction(reaction.emoji)

                    # Vérifier si le joueur a gagné
                    if self.check_winner(":regional_indicator_x:"):
                        await board_message.edit(embed=self.create_embed("Félicitations, tu as gagné!", self.format_board()))
                        break

                    # Si le plateau est plein, c'est une égalité
                    if self.is_board_full():
                        await board_message.edit(embed=self.create_embed("Égalité!", self.format_board()))
                        break

                    # Tour du bot
                    bot_choice = await self.bot_turn()
                    await board_message.edit(embed=self.create_embed(f"Le bot joue", self.format_board()))

                    # Vérifier si le bot a gagné
                    if self.check_winner(":o2:"):
                        await board_message.edit(embed=self.create_embed("Le bot a gagné!", self.format_board()))
                        break

                    # Si le plateau est plein après le coup du bot, c'est une égalité
                    if self.is_board_full():
                        await board_message.edit(embed=self.create_embed("Égalité!", self.format_board()))
                        break
                else:
                    await ctx.send("Cette case est déjà prise!", delete_after=5)
            except discord.errors.NotFound:
                break

    # Fonction pour créer un embed pour le jeu
    def create_embed(self, title, board):
        embed = discord.Embed(title=title, description=board, color=discord.Color.green())
        return embed

async def setup(bot):
    print("Extension morpion chargée")
    await bot.add_cog(Morpion(bot))
