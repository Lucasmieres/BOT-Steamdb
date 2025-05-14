import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

# Carregar variáveis do arquivo .env
load_dotenv()
CHAVE = os.getenv("CHAVE")

# Verificar se a variável CHAVE foi carregada corretamente
if CHAVE is None:
    print("Erro: CHAVE não encontrada no arquivo .env")
else:
    print("CHAVE carregada com sucesso!")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Jogos com seus AppIDs da Steam
jogos = {
    "ETS2": 227300,
    "FS22": 1248130,
    "SnowRunner": 1465360,
    "GTA V": 271590,
    "Battlefield 1": 1238840,
    "Battlefield 4": 1238860,
    "CS2": 730,
    "Project Zomboid": 108600,
    "Need for Speed Heat": 1222680,
    "EA FIFA 25": 2669320,
}

def get_steam_players(app_id):
    try:
        url = f"https://steamcharts.com/app/{app_id}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        players_now = soup.select_one('.app-stat .num').text.strip()
        peak_24h = soup.select('.app-stat .num')[1].text.strip()
        return f"Agora: {players_now} | Pico 24h: {peak_24h}"
    except:
        return "Erro ao buscar dados"

@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Comando /jogos sincronizado ({len(synced)} comandos).")
    except Exception as e:
        print(e)

@bot.tree.command(name="jogos", description="Ver jogadores online dos jogos do servidor")
async def jogos_command(interaction: discord.Interaction):
    await interaction.response.defer()
    resposta = "**Jogadores online agora:**\n"
    for nome, app_id in jogos.items():
        dados = get_steam_players(app_id)
        resposta += f"**{nome}** → {dados}\n"
    await interaction.followup.send(resposta)

bot.run(CHAVE)
