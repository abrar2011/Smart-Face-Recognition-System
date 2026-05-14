import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask, request
import threading
import asyncio

TOKEN = "BotTokenHere"

# channes in my server, change them
LOG_CHANNEL = 1504508733839900855 
ALERT_CHANNEL = 1504508750155747642
VERIFY_CHANNEL = 1504522183609946193

app = Flask(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ======================
# DISCORD SAFE SENDER
# ======================
def run_async(coro):
    asyncio.run_coroutine_threadsafe(coro, bot.loop)


# ======================
# FLASK ROUTE (ONLY ONCE)
# ======================
@app.route("/event", methods=["POST"])
def receive_event():

    data = request.json
    print("RECEIVED:", data)

    event_type = data.get("type")
    message = data.get("message")

    if event_type == "log":
        run_async(send_log(message))

    elif event_type == "alert":
        run_async(send_alert(message))

    elif event_type == "unknown":
        run_async(send_unknown(message))

    return "OK"


# ======================
# FLASK START
# ======================
def run_flask():
    app.run(host="127.0.0.1", port=5000)


# ======================
# BOT READY
# ======================
@bot.event
async def on_ready():
    print("Bot online:", bot.user)

    threading.Thread(target=run_flask, daemon=True).start()

    try:
        synced = await bot.tree.sync(
            guild=discord.Object(id=1504508435654377632) # my server ID, change it
        )
        print("Synced:", len(synced))

    except Exception as e:
        print(e)


# ======================
# LOG FUNCTION
# ======================
async def send_log(text):

    channel = bot.get_channel(LOG_CHANNEL)

    embed = discord.Embed(
        title="📜 LOG",
        description=text,
        color=discord.Color.greyple()
    )

    await channel.send(embed=embed)


# ======================
# ALERT FUNCTION
# ======================
async def send_alert(text):

    channel = bot.get_channel(ALERT_CHANNEL)

    embed = discord.Embed(
        title="🚨 THREAT ALERT",
        description=text,
        color=discord.Color.red()
    )

    await channel.send("@everyone", embed=embed)


# ======================
# UNKNOWN FUNCTION
# ======================
async def send_unknown(text):

    channel = bot.get_channel(VERIFY_CHANNEL)

    embed = discord.Embed(
        title="🤖 UNKNOWN PERSON",
        description=text,
        color=discord.Color.orange()
    )

    await channel.send(embed=embed)


bot.run(TOKEN)
