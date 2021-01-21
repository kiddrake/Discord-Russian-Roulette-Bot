import discord
from discord.ext import commands
import random
import asyncio
from itertools import cycle

client = commands.Bot(command_prefix = "-rr ")
client.remove_command('help')

client.game_type = None
client.game_status = "Off"
client.player_list = []
client.current_player = None
client.list_iteration = None
client.list_position = None
client.probability = 6

@client.event
async def on_ready():
    print("All Good :)")

@client.command(aliases = ['Classic', 'classic'])
async def classic_game_start(ctx):
    if not client.game_status == "Off":
        await ctx.send("There's already a game going on right now!")
        return
    client.game_type = "Classic"
    client.player_list.append(ctx.message.author)
    client.game_status = "Collecting Players"
    await ctx.send(f'{ctx.message.author.mention} started a game (classic)!\nJoin the game by entering "-rr join"\n20 seconds remaining...')
    await asyncio.sleep(10)
    await ctx.send("10 seconds remaining...")
    await asyncio.sleep(10)
    client.game_status = "On"
    random.shuffle(client.player_list)
    client.list_iteration = cycle(client.player_list)
    client.current_player = next(client.list_iteration)
    await ctx.send("Game Start!")
    await ctx.send(f"Your turn to pull the trigger... {client.player_list[0].mention}")

@client.command(aliases = ['Battleroyale', 'battleroyale', 'Royale', 'royale'])
async def battle_royale_game_start(ctx):
    if not client.game_status == "Off":
        await ctx.send("There's already a game going on right now!")
        return
    client.game_type = "Battle Royale"
    client.player_list.append(ctx.message.author)
    client.game_status = "Collecting Players"
    await ctx.send(f'{ctx.message.author.mention} started a game (battle royale)!\nJoin the game by entering "-rr join"\n20 seconds remaining...')
    await asyncio.sleep(10)
    await ctx.send("10 seconds remaining...")
    await asyncio.sleep(10)
    client.game_status = "On"
    random.shuffle(client.player_list)
    client.list_position = 0
    client.current_player = client.player_list[0]
    await ctx.send("Game Start!")
    await ctx.send(f"Your turn to pull the trigger... {client.current_player.mention}")

@client.command(aliases = ['Join', 'join'])
async def player_join(ctx):
    if client.game_status == "On":
        await ctx.send("Wait for the next game!")
        return
    if client.game_status == "Off":
        await ctx.send('There is no game to join :( Start one with "-rr classic" or "-rr battleroyale" command!')
        return
    if ctx.message.author in client.player_list:
        await ctx.send(f"You're already in the game, {ctx.message.author.mention}")
        return
    client.player_list.append(ctx.message.author)
    await ctx.send(f"{ctx.message.author.mention} joined!")

@client.command(aliases = ["Shoot", "shoot", "Fire", "fire", "Shot", "shot"])
async def shots_fired(ctx):
    if client.game_status == "Off":
        await ctx.send('There is no game to join :( Start one with "-rr classic" or "-rr battleroyale" command!')
        return
    if not ctx.message.author in client.player_list:
        await ctx.send("Wait for the next game!")
        return
    if not client.current_player == ctx.message.author:
        await ctx.send("It's not your turn yet...")
        return
    if client.game_type == "Classic":
        chance_number  = random.randint(1, client.probability)
        if chance_number == 1:
            client.game_type = None
            client.game_status = "Off"
            client.player_list = []
            client.current_player = None
            client.list_iteration = None
            client.list_position = None
            client.probability = 6
            await ctx.send("<:Sniperpistol:744699847294058497><:SmallBoom:744719971162259506>")
            await ctx.send(f"<:RIP:744698510733213757>{ctx.message.author.mention}")
            return
        else:
            await ctx.send(f"{ctx.message.author.mention} was lucky...")
            client.current_player = next(client.list_iteration)
            await ctx.send(f"It's your turn, {client.current_player.mention}")
            return
    if client.game_type == "Battle Royale":
        chance_number  = random.randint(1, client.probability)
        if chance_number == 1:
            await ctx.send("<:Sniperpistol:744699847294058497><:SmallBoom:744719971162259506>")
            await ctx.send(f"<:RIP:744698510733213757>{ctx.message.author.mention}")
            if client.player_list.index(ctx.message.author) + 1 == len(client.player_list):
                del client.player_list[-1]
                client.list_position = 0
                client.current_player = client.player_list[0]
            else:
                await ctx.send("<:Sniperpistol:744699847294058497><:SmallBoom:744719971162259506>")
                await ctx.send(f"<:RIP:744698510733213757>{ctx.message.author.mention}")
                client.player_list.remove(ctx.message.author)
                client.current_player = client.player_list[client.list_position]
            if len(client.player_list) == 1:
                await ctx.send(f"{client.player_list[0].mention} won!")
                client.game_type = None
                client.game_status = "Off"
                client.player_list = []
                client.current_player = None
                client.list_iteration = None
                client.list_position = None
                client.probability = 6
                return
        else:
            if client.player_list[-1] == ctx.message.author:
                client.list_position = 0
            else:
                client.list_position += 1
            client.current_player = client.player_list[client.list_position]
            await ctx.send(f"{ctx.message.author.mention} was lucky...")
            await ctx.send(f"It's your turn, {client.current_player.mention}")

@client.command(aliases = ['Chance', 'chance'])
async def set_probability(ctx, probabaility):
    if client.game_status == "Off":
        await ctx.send("There is no game going on right now!")
        return
    if client.game_status == "On":
        await ctx.send("The game is already going on! Can't use that command!")
        return
    if int(probabaility) == 1:
        await ctx.send(f"{ctx.message.author.mention} Here's the National Suicide Hotline: 1-800-273-8255")
        return
    client.probability = int(probabaility)
    await ctx.send(f"Cylinder now has {client.probability} chambers!")

@client.command()
async def test(ctx):
    await ctx.send(f"Status: {client.game_status}")
    await ctx.send(f"Players: {client.player_list}")

@client.command()
async def reset(ctx):
    client.game_type = None
    client.game_status = "Off"
    client.player_list = []
    client.current_player = None
    client.list_iteration = None
    client.list_position = None
    client.probability = 6
    await ctx.send("Reset complete!")

client.run('Secret ;)')
