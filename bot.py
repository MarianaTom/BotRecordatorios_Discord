import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
scheduler = AsyncIOScheduler(timezone="America/Mexico_City")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    # Recordatorio jueves 2:00 PM
    scheduler.add_job(send_reminder, CronTrigger(day_of_week='thu', hour=14, minute=0))
    # Aviso jueves 2:59 PM
    scheduler.add_job(send_last_call, CronTrigger(day_of_week='thu', hour=14, minute=59))
    scheduler.start()

async def send_reminder():
    channel = bot.get_channel(CHANNEL_ID)  # Reemplaza con tu ID de canal
    if channel:
        with open("recordatorios/recordatorio1.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

async def send_last_call():
    channel = bot.get_channel(CHANNEL_ID)  # Reemplaza con tu ID de canal
    if channel:
        with open("recordatorios/recordatorio2.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

@bot.command()
async def testbot(ctx):
    await ctx.send("¡Bot activo y funcionando!")

bot.run(TOKEN)