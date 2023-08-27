import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!dl ', intents=intents)

@bot.event
async def on_ready():
    print("Stormia is ready!")

async def send_message(ctx, title, description, color):
    s = discord.Embed(title=title, description=description, color=color)
    s.set_footer(text=str(ctx.author)+" | "+str(ctx.author.id), icon_url=ctx.author.avatar.url)
    await ctx.send(embed=s)

colors = {"list": 0x3498db, "commands": 0xffffff, "reset": 0x3498db, "insert": 0x2ecc71, "pause": 0xf1c40f, "resume": 0x2ecc71, "add": 0x2ecc71, "drop": 0xe74c3c, "status": 0x3498db}

host = "stormia-api"
port = os.getenv('port')
API_URL = f"http://{host}:{port}"

try:
    requests.get(f"{API_URL}")
except:
    print("Failed to connnect to database")

@bot.event
async def on_command_error(ctx, error):
    response = requests.get(f"{API_URL}")
    data = response.json()
    await send_message(ctx, "Invalid Command", data["message"], colors["commands"])
    
@bot.command('commands')
async def handle_commands(ctx):
    response = requests.get(f"{API_URL}")
    data = response.json()
    await send_message(ctx, "Commands", data["message"], colors["commands"])

@bot.command('list')
async def handle_list(ctx):
    response = requests.get(f"{API_URL}/list")
    data = response.json()
    await send_message(ctx, "Report", data["message"], colors['list'])

@bot.command('clockin')
async def handle_resume(ctx):
    response = requests.put(f"{API_URL}/resume/{ctx.author.id}")
    data = response.json()
    await send_message(ctx, "Clock In", data["message"], colors['resume'])

@bot.command('clockout')
async def handle_pause(ctx):
    response = requests.put(f"{API_URL}/pause/{ctx.author.id}")
    data = response.json()
    await send_message(ctx, "Clock Out", data["message"], colors['pause'])

@bot.command('insert')
async def handle_insert(ctx, user : discord.Member):
    response = requests.post(f"{API_URL}/insert/{user.id}")
    data = response.json()
    await send_message(ctx, "Insert", data["message"], colors['insert'])

@bot.command('drop')
async def handle_drop(ctx, user : discord.Member):
    response = requests.delete(f"{API_URL}/drop/{user.id}")
    data = response.json()
    await send_message(ctx, "Drop", data["message"], colors['drop'])

@bot.command('reset')
async def handle_reset(ctx, user = None):
    if user:
        response = requests.put(f"{API_URL}/reset/{str(user)[2:len(user)-1]}")
        data = response.json()
        await send_message(ctx, "Reset", data["message"], colors['reset'])
    else:
        response = requests.put(f"{API_URL}/reset")
        data = response.json()
        await send_message(ctx, "Reset", data["message"], colors['reset'])

@bot.command('status')
async def handle_status(ctx, user = None):
    if user:
        response = requests.get(f"{API_URL}/status/{str(user)[2:len(user)-1]}")
        data = response.json()
        await send_message(ctx, "Status", data["message"], colors['status'])
    else:
        response = requests.get(f"{API_URL}/status/{ctx.author.id}")
        data = response.json()
        await send_message(ctx, "Status", data["message"], colors['status'])

@bot.command('add')
async def handle_add(ctx, time, user = None):
    if user:
        response = requests.put(f"{API_URL}/add/{int(time)}/{str(user)[2:len(user)-1]}")
        data = response.json()
        await send_message(ctx, "Add", data["message"], colors['add'])
    else:
        response = requests.put(f"{API_URL}/add/{int(time)}/{ctx.author.id}")
        data = response.json()
        await send_message(ctx, "Add", data["message"], colors['add'])

bot.run(token)