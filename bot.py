import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

# ✅ Nuevos IDs del servidor final
ID_ASISTENCIA = 1098776649060864051
ID_UPDATE = 1073289305662967940

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Función para leer archivos
def cargar_mensaje(nombre_archivo):
    ruta = os.path.join("recordatorios", nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# ✅ Comando para enviar recordatorio de avance semanal
@bot.command()
async def r_avance(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    mensaje = cargar_mensaje("mensaje_avance.txt")
    await canal.send(mensaje)
    await ctx.send("✅ Recordatorio de avance enviado.")

# ✅ Comando para enviar recordatorio urgente
@bot.command()
async def r_urgente(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    mensaje = cargar_mensaje("mensaje_avanceUrgente.txt")
    await canal.send(mensaje)
    await ctx.send("✅ Recordatorio urgente enviado.")

# ✅ Comando para enviar recordatorio de asistencia con imagen y enlace
@bot.command()
async def r_asistencia(ctx):
    canal = bot.get_channel(ID_UPDATE)
    with open("recordatorios/JuntaSemanal.png", "rb") as f:
        imagen = discord.File(f)
    link = cargar_mensaje("asistenciaJunta.txt")
    mensaje = await canal.send("@everyone", file=imagen)
    await mensaje.reply(f"Registra tu asistencia: [Aquí]({link})")
    await ctx.send("✅ Recordatorio de asistencia enviado.")

# ✅ Comando para prueba única en el servidor final
@bot.command()
async def prueba_final(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    if canal:
        await canal.send("🔧 *Probando bot en servidor final. Favor de ignorar este mensaje.*")
        await ctx.send("✅ Mensaje de prueba enviado al canal de asistencia.")
    else:
        await ctx.send("❌ No se encontró el canal de asistencia.")

bot.run(TOKEN)
