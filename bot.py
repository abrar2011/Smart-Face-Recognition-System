import discord
from discord.ext import commands
from flask import Flask, request
import asyncio
import threading
import serial
import time
import cv2
import requests

TOKEN = "Bot_Token_Here"

VERIFY_CHANNEL = 1505909726318170153
ROLE_PING = "<@&1504722323117178962>"

# =========================
# ARDUINO
# =========================
arduino = serial.Serial(
    "COM4",
    9600,
    timeout=1
)

time.sleep(2)

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# DISCORD BOT
# =========================
intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# SERIAL SENDER
# =========================
def send_arduino(cmd):

    arduino.write(
        (cmd + "\n").encode()
    )

    print("→ Arduino:", cmd)

# =========================
# SAFE ASYNC
# =========================
def run_async(coro):

    asyncio.run_coroutine_threadsafe(
        coro,
        bot.loop
    )

# =========================
# CAMERA SNAPSHOT
# =========================
def take_photo():

    cam = cv2.VideoCapture(0)

    ret, frame = cam.read()

    path = (
        f"request_"
        f"{int(time.time())}.jpg"
    )

    cv2.imwrite(path, frame)

    cam.release()

    return path

# =========================
# BUTTON UI
# =========================
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

# =========================
# UNKNOWN PERSON
# WITH BUTTONS
# =========================
async def send_unknown(
    message,
    image_path
):

    channel = bot.get_channel(
        VERIFY_CHANNEL
    )

    embed = discord.Embed(
        title="UNKNOWN PERSON",
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

# =========================
# THREAT ALERT
# NO BUTTONS
# =========================
async def send_threat(
    message,
    image_path
):

    channel = bot.get_channel(
        VERIFY_CHANNEL
    )

    embed = discord.Embed(
        title="⚠ THREAT DETECTED",
        description=message,
        color=discord.Color.red()
    )

    file = discord.File(image_path)

    await channel.send(
        ROLE_PING,
        embed=embed,
        file=file
    )

# =========================
# FLASK ROUTE
# =========================
@app.route(
    "/event",
    methods=["POST"]
)
def receive_event():

    data = request.json

    event_type = data["type"]

    payload = data["data"]

    # =========================
    # AUTHORIZED
    # =========================
    if event_type == "AUTHORIZED":

        send_arduino("AUTHORIZED")

    # =========================
    # THREAT
    # NO BUTTONS
    # =========================
    elif event_type == "THREAT":

        send_arduino("THREAT")

        run_async(
            send_threat(
                payload["message"],
                payload["image"]
            )
        )

    # =========================
    # UNKNOWN
    # WITH BUTTONS
    # =========================
    elif event_type == "UNKNOWN":

        send_arduino("WAITING")

        run_async(
            send_unknown(
                payload["message"],
                payload["image"]
            )
        )

    # =========================
    # RESET
    # =========================
    elif event_type == "RESET":

        send_arduino("Reset")

    return "OK"

# =========================
# SERIAL LISTENER
# =========================
def serial_listener():

    while True:

        if arduino.in_waiting:

            msg = (
                arduino.readline()
                .decode()
                .strip()
            )

            print("SERIAL:", msg)

            # =========================
            # MANUAL REQUEST
            # =========================
            if msg == "A_PRESSED":

                path = take_photo()

                requests.post(
                    "http://127.0.0.1:5000/event",
                    json={
                        "type": "UNKNOWN",
                        "data": {
                            "message":
                            "Manual Request",
                            "image": path
                        }
                    }
                )

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():

    print("BOT READY")

    threading.Thread(
        target=serial_listener,
        daemon=True
    ).start()

    threading.Thread(
        target=lambda:
        app.run(
            host="127.0.0.1",
            port=5000
        ),
        daemon=True
    ).start()

# =========================
# START BOT
# =========================
bot.run(TOKEN)
