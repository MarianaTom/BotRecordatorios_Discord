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
    scheduler.add_job(send_reminder, CronTrigger(day_of_week='tue', hour=23, minute=30))
    # Aviso jueves 2:59 PM
    scheduler.add_job(send_last_call, CronTrigger(day_of_week='tue', hour=23, minute=31))
    scheduler.start()

async def send_reminder():
    channel = bot.get_channel(1389709699301118095)
    if channel:
        with open("recordatorios/recordatorio1.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

async def send_last_call():
    channel = bot.get_channel(1389837483327488011) 
    if channel:
        with open("recordatorios/recordatorio2.txt", "r", encoding="utf-8") as f:
            await channel.send(f.read())

@bot.command()
async def testbot(ctx):
    await ctx.send("¡Bot activo y funcionando!")

@bot.command()
async def preview(ctx):
    """Envía ambos recordatorios manualmente como ejemplo."""
    with open("recordatorios/recordatorio1.txt", "r", encoding="utf-8") as f1:
        await ctx.send(f"📌 **Preview Recordatorio 1:**\n{f1.read()}")

    with open("recordatorios/recordatorio2.txt", "r", encoding="utf-8") as f2:
        await ctx.send(f"📌 **Preview Recordatorio 2:**\n{f2.read()}")

bot.run(TOKEN)
