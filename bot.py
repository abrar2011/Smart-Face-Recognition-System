import discord
from discord.ext import commands
from flask import Flask, request
import threading
import asyncio
import serial
import time

TOKEN = "YourBotTokenHere"

LOG_CHANNEL = 1504508733839900855
ALERT_CHANNEL = 1504508750155747642
VERIFY_CHANNEL = 1504522183609946193

ROLE_PING = "<@&1504722323117178962>"

app = Flask(__name__)

# ======================
# ARDUINO
# ======================
arduino = None

try:
    arduino = serial.Serial('COM13', 9600)
    time.sleep(2)
    print("Arduino connected")

except Exception as e:
    print("Arduino NOT connected:", e)


# ======================
# SEND TO ARDUINO
# ======================
def send_arduino(cmd):

    if arduino is not None:

        try:
            arduino.write((cmd + "\n").encode())
            print("ARDUINO →", cmd)

        except Exception as e:
            print("Arduino error:", e)


# ======================
# DISCORD BOT
# ======================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ======================
# SAFE ASYNC
# ======================
def run_async(coro):

    if bot.is_ready():
        asyncio.run_coroutine_threadsafe(
            coro,
            bot.loop
        )


# ======================
# FLASK ROUTE
# ======================
@app.route("/event", methods=["POST"])
def receive_event():

    data = request.json

    print("RECEIVED:", data)

    try:

        event_type = data.get("type")
        payload = data.get("data", {})

        message = payload.get("message", "")
        image = payload.get("image", None)

        # ======================
        # AUTHORIZED / LOG
        # ======================
        if event_type == "log":

            run_async(send_log(message))

            if "AUTHORIZED" in message:
                send_arduino("AUTHORIZED")

            elif "THREAT" in message:
                send_arduino("THREAT")    

        # ======================
        # THREAT
        # ======================
        elif event_type == "alert":

            run_async(
                send_alert(message, image)
            )

            send_arduino("THREAT")

        # ======================
        # UNKNOWN PERSON
        # ======================
        elif event_type == "manual_verification":

            run_async(
                send_unknown(message, image)
            )
            send_arduino("WAITING")
            

        # ======================
        # RESET
        # ======================
        elif event_type == "reset":

            send_arduino("Reset")

    except Exception as e:
        print("Flask handler error:", e)

    return "OK", 200


# ======================-
# START FLASK
# ======================
def run_flask():

    app.run(
        host="127.0.0.1",
        port=5000
    )


# ======================
# BOT READY
# ======================
@bot.event
async def on_ready():

    print("Bot online:", bot.user)

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()


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
async def send_alert(message, image_path):

    channel = bot.get_channel(ALERT_CHANNEL)

    embed = discord.Embed(
        title="🚨 THREAT ALERT",
        description=message,
        color=discord.Color.red()
    )

    file = discord.File(image_path)

    await channel.send(
        ROLE_PING,
        embed=embed,
        file=file
    )


# ======================
# VERIFICATION BUTTONS
# ======================
class VerifyView(discord.ui.View):

    @discord.ui.button(
        label="ALLOW",
        style=discord.ButtonStyle.green
    )
    async def allow(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        send_arduino("ALLOW")

        await interaction.response.send_message(
            "✅ ACCESS GRANTED",
            ephemeral=True
        )



    @discord.ui.button(
        label="DENY",
        style=discord.ButtonStyle.red
    )
    async def deny(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        send_arduino("DENY")

        await interaction.response.send_message(
            "❌ ACCESS DENIED",
            ephemeral=True
        )


# ======================
# UNKNOWN FUNCTION
# ======================
async def send_unknown(
    message,
    image_path
):

    channel = bot.get_channel(
        VERIFY_CHANNEL
    )

    embed = discord.Embed(
        title="🤖 UNKNOWN PERSON",
        description=message,
        color=discord.Color.orange()
    )

    file = discord.File(image_path)

    await channel.send(
        ROLE_PING,
        embed=embed,
        file=file,
        view=VerifyView()
    )


# ======================
# RUN BOT
# ======================
bot.run(TOKEN)
