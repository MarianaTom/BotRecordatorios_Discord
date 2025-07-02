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

# Reemplaza estos valores con los IDs reales
CHANNEL_ID_ASISTENCIA = 1389709699301118095  # recordatorio-1
CHANNEL_ID_UPDATE = 1389837483327488011      # recordatorio-2

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

    # Tareas programadas (Jueves)
    scheduler.add_job(send_reminder, CronTrigger(day_of_week='thu', hour=9, minute=0))
    scheduler.add_job(send_last_call, CronTrigger(day_of_week='thu', hour=16, minute=0))
    scheduler.add_job(send_junta_reminder, CronTrigger(day_of_week='thu', hour=12, minute=0))
    scheduler.add_job(send_asistencia_link, CronTrigger(day_of_week='thu', hour=12, minute=1))

    scheduler.start()

async def send_reminder():
    channel = bot.get_channel(CHANNEL_ID_ASISTENCIA)
    if channel:
        with open("recordatorios/recordatorio1.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

async def send_last_call():
    channel = bot.get_channel(CHANNEL_ID_ASISTENCIA)
    if channel:
        with open("recordatorios/recordatorio2.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

async def send_junta_reminder():
    channel = bot.get_channel(CHANNEL_ID_UPDATE)
    if channel:
        with open("recordatorios/recordatorio3.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

async def send_asistencia_link():
    channel = bot.get_channel(CHANNEL_ID_UPDATE)
    if channel:
        with open("recordatorios/recordatorio4.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

@bot.command()
async def testbot(ctx):
    await ctx.send("¡Bot activo y funcionando!")

@bot.command()
async def preview(ctx):
    """Envía una vista previa de todos los recordatorios"""
    for i in range(1, 5):
        with open(f"recordatorios/recordatorio{i}.txt", "r", encoding="utf-8") as f:
            await ctx.send(f"📌 **Preview Recordatorio {i}:**\n{f.read()}")

bot.run(TOKEN)
