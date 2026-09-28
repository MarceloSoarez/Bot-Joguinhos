import discord
from discord.ext import commands
import requests
import urllib.parse

intents = discord.Intents.default()
intents.message_content = True

class BotPromos(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos Slash sincronizados com sucesso!")

bot = BotPromos()

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user.name} (ID: {bot.user.id})")

# ==================== FUNÇÕES DE BUSCA NAS LOJAS ====================

def buscar_steam(nome_jogo):
    # Usa diretamente a URL de pesquisa da Steam ignorando preferências com o termo buscado
    query = urllib.parse.quote(nome_jogo)
    url = f"https://store.steampowered.com/search/?term={query}&hwtype=0&supportedlang=brazilian&ndl=1&ignore_preferences=1"
    return "Verificar preço na Steam", url

def buscar_nuuvem(nome_jogo):
    url = f"https://www.nuuvem.com/br-pt/catalog/page/1/search/{urllib.parse.quote(nome_jogo)}"
    return "Verificar preço na Nuuvem", url

def buscar_fanatical(nome_jogo):
    url = f"https://www.fanatical.com/pt/search?search={urllib.parse.quote(nome_jogo)}"
    return "Verificar ofertas na Fanatical", url

def buscar_gmg(nome_jogo):
    url = f"https://www.greenmangaming.com/pt/search?query={urllib.parse.quote(nome_jogo)}"
    return "Verificar ofertas na GMG", url

def buscar_eneba(nome_jogo):
    query = urllib.parse.quote(nome_jogo)
    url = f"https://www.eneba.com/br/store/all?drms[]=steam&regions[]=global&regions[]=latam&regions[]=brazil&text={query}&types[]=game"
    return "Verificar ofertas na Eneba", url

# ==================== COMANDO SLASH ====================

@bot.tree.command(name="promo", description="Compara o preço de um jogo na Steam e busca nas lojas de keys.")
@discord.app_commands.describe(nome="Nome do jogo que você quer pesquisar")
async def promo(interaction: discord.Interaction, nome: str):
    await interaction.response.defer(thinking=True)

    preco_steam, link_steam = buscar_steam(nome)
    _, link_nuuvem = buscar_nuuvem(nome)
    _, link_fanatical = buscar_fanatical(nome)
    _, link_gmg = buscar_gmg(nome)
    _, link_eneba = buscar_eneba(nome)

    embed = discord.Embed(
        title=f"🎮 Comparador de Preços: {nome}",
        description="Atalhos de busca direta nas principais lojas:",
        color=discord.Color.blue()
    )

    embed.add_field(name="💻 Steam", value=f"[{preco_steam}]({link_steam})", inline=False)
    embed.add_field(name="🛒 Nuuvem", value=f"[Verificar preço na Nuuvem]({link_nuuvem})", inline=False)
    embed.add_field(name="🔑 Fanatical", value=f"[Verificar ofertas na Fanatical]({link_fanatical})", inline=False)
    embed.add_field(name="🟢 Green Man Gaming", value=f"[Verificar ofertas na GMG]({link_gmg})", inline=False)
    embed.add_field(name="🌐 Eneba *(Global/LATAM/BR)*", value=f"[Verificar ofertas na Eneba]({link_eneba})", inline=False)

    embed.set_footer(text="Clique nos links para conferir os valores exatos em cada loja.")

    await interaction.followup.send(embed=embed)

bot.run("MTIzOTI3MjAwNDE0MjQ5Nzk3NQ.G7iQ1p.-oA-Z5mJ8QRAnBCW3Qu0hrVRX9POLo9KZhrlqY")