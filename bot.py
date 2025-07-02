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

CHANNEL_ID_ASISTENCIA = 1389709699301118095
CHANNEL_ID_UPDATE = 1389837483327488011

# Bandera para evitar duplicados
enviando_prueba = False

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

    scheduler.add_job(send_reminder, CronTrigger(day_of_week='wed', hour=16, minute=6))
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
    for i in range(1, 5):
        with open(f"recordatorios/recordatorio{i}.txt", "r", encoding="utf-8") as f:
            await ctx.send(f"📌 **Preview Recordatorio {i}:**\n{f.read()}")

@bot.command()
async def pruebaenvio(ctx):
    global enviando_prueba

    if enviando_prueba:
        await ctx.send("⏳ Ya se está ejecutando una prueba de envío. Intenta más tarde.")
        return

    enviando_prueba = True
    print("👉 Ejecutando comando pruebaenvio...")

    try:
        channel1 = bot.get_channel(CHANNEL_ID_ASISTENCIA)
        channel2 = bot.get_channel(CHANNEL_ID_UPDATE)

        if channel1:
            with open("recordatorios/recordatorio1.txt", "r", encoding="utf-8") as f:
                await channel1.send(f.read())
            with open("recordatorios/recordatorio2.txt", "r", encoding="utf-8") as f:
                await channel1.send(f.read())
        else:
            await ctx.send("❌ No encontré el canal de asistencia.")

        if channel2:
            with open("recordatorios/recordatorio3.txt", "r", encoding="utf-8") as f:
                await channel2.send(f.read())
            with open("recordatorios/recordatorio4.txt", "r", encoding="utf-8") as f:
                await channel2.send(f.read())
        else:
            await ctx.send("❌ No encontré el canal de actualizaciones.")

        await ctx.send("✅ Prueba de envíos completada.")
    except Exception as e:
        await ctx.send(f"⚠️ Error al enviar recordatorios: {e}")
    finally:
        enviando_prueba = False

bot.run(TOKEN)
