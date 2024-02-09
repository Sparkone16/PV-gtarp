import discord
from discord import Embed
import keep_alive
from discord.ext import commands
from typing import Literal
from enum import Enum
import sqlite3

keep_alive.keep_alive()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)
GUILD = "1127588289407352894"

database = sqlite3.connect('espacenumerique.db')
cursor = database.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS taj (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        birthday date,
        adresse VARCHAR(100),
        ville VARCHAR(100)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fpr (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        birthday DATE,
        adresse VARCHAR(100),
        ville VARCHAR(100),
        fait TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fnpc (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        birthday DATE,
        permis VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS siv (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        marque VARCHAR(100),
        model VARCHAR(50),
        plate VARCHAR(50)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fva (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        plate VARCHAR(50),
        debut DATE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS foves (
        id INTEGER PRIMARY KEY,
        nom VARCHAR(100),
        prenom VARCHAR(100),
        object VARCHAR(100),
        suspect VARCHAR(100)
    )
''')

database.commit()

@bot.event
async def on_ready():
    print("Ready")

@bot.command(name="taj_check", 
             description="/taj_check [nom] [prenom] : Permet de faire une verification au TAJ pour un nom et prenom.")
async def taj_check(ctx: commands.Context, name: str, prenom: str):
    cursor.execute('''
          SELECT *
          FROM taj
          WHERE name = ? AND prenom = ?
    ''', (name, prenom))

    result = cursor.fetchall()
    
    if result is not None:
        name = result[1]
        prenom = result[2]
        birthday = result[3]
        adresse = result[4]
        ville = result[5]
        
        embed = discord.Embed(
        title='Check au TAJ',
        descripton=f'{ctx.author} a fait une demande de TAJ pour {name} {prenom}.',
        colour=discord.Colour.green()
        )
        embed.add_field(name="Nom", value=f"{name}", inline=False)
        embed.add_field(name="Prenom", value=f"{prenom}", inline=False)
        embed.add_field(name="Date de naissance", value=f"{birthday}", inline=False)
        embed.add_field(name="Adresse", value=f"{adresse}", inline=False)
        embed.add_field(name="Ville de résidence", value=f"{ville}", inline=False)
        embed.set_footer(text="Espace Numérique")
        await ctx.send(embed=embed)
        
    else : 
        embed = discord.Embed(
        title='Check au TAJ',
        descripton=f'Aucune donnée de TAJ de {name} {prenom}',
        colour=discord.Colour.grey()
        )
        embed.set_footer(text="Espace Numérique")
        await ctx.send(embed=embed)

  
@bot.command(name="taj_add",
            description="/taj_add [nom] [prenom] [birthday] [adresse] [ville] : Permet d'ajouter une fiche au TAJ")
async def taj_add(ctx: commands.Context, 
                   name: str, 
                   prenom: str,
                   birthday: str,
                   adresse: str,
                   ville: str
                   ):
    embed = discord.Embed(
        title='Ajout au TAJ',
        description=f'{ctx.author} a ajouté une fiche au TAJ pour {name} {prenom}.',
        colour=discord.Colour.green()
    )
    embed.set_footer(text='Espace Numérique')
  
    cursor.execute('''
            INSERT INTO taj (nom, prenom, birthday, adresse, ville) 
            VALUES (?,?,?,?,?)
        ''', (name, prenom, birthday, adresse, ville))
    database.commit()
    await ctx.send(embed=embed)


@bot.command(name="helpy",
             description="/helpy : Permet de vous montrez toutes mes commandes et ses fonctionnalités")
async def helpy(ctx: commands.Context):
    embed = discord.Embed(
        title = "Support",
        description = "Voici toutes mes commandes :",
        colour = discord.Colour.orange()
    )
    embed.add_field(name="/addstock [coke/beldia] [nombre de KG]", value="Permet d'ajouter au stock de la beldia ou de la coke avec la quantité donnée.", inline=False)
    embed.add_field(name="/stock [coke/beldia]", value="Permet de voir le stock de beldia ou de coke.", inline=False)
    embed.add_field(name="/delstock [coke/beldia] [nombre de KG]", value="Permet de retirer du stock de la beldia ou de la coke avec la quantité donnée.", inline=False)
    embed.add_field(name="/calc [prix unitaire] [quantité]", value="Permet de calculer combien une vente a rapporté", inline=False)
    embed.add_field(name="/tarif", value="Permet de voir les prix des drogues", inline=False)
    embed.add_field(name="/addepicerie [modelname] [quantité]", value="Permet d'ajouter une certaine quantité de produit au stock de l'épicerie", inline=False)
    embed.add_field(name="/epicerie [model name]", value="Permet de voir le voir de l'épicerie", inline=False)
    embed.add_field(name="/delepicerie [model name] [quantité]", value="Permet de supprimer une certaine quantité de produit au stock de l'épicerie", inline=False)
    embed.set_footer(text="Grigny !")
    
    await ctx.send(embed=embed)

bot.run("YOUR TOKEN")
