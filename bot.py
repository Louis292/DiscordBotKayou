import discord
from discord.ext import commands
import os
import asyncio

# Lire le token du fichier token.txt
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

# Intents nécessaires (vous pouvez les ajuster selon vos besoins)
intents = discord.Intents.default()
intents.message_content = True

# Créer une instance de bot
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_commands():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
            except Exception as e:
                print(f'Erreur lors du chargement de l\'extension {filename}: {e}')

async def load_listeners():
    for filename in os.listdir('./listeners'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'listeners.{filename[:-3]}')
            except Exception as e:
                print(f'Erreur lors du chargement de l\'extension {filename}: {e}')


# Définir un événement de démarrage pour confirmer que le bot est connecté
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

# Fonction principale pour démarrer le bot
async def main():
    await load_commands()
    await load_listeners()
    await bot.start(TOKEN)

# Démarrer le bot en exécutant la fonction main
asyncio.run(main())
