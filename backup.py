import discord
from discord.ext import commands
import cv2
import serial
import threading
import asyncio
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
TOKEN = "BotTokenHere"
CHANNEL_ID = 1504508719713484890

# =========================
# DISCORD BOT
# =========================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# ARDUINO
# =========================
arduino = serial.Serial("COM13", 9600)
time.sleep(2)

# =========================
# CAMERA
# =========================
cam = cv2.VideoCapture(0)

running = True

# =========================
# DISCORD SAFE SENDER
# =========================
def send_discord(message, file_path=None):
    channel = bot.get_channel(CHANNEL_ID)

    async def task():
        if file_path:
            file = discord.File(file_path)
            await channel.send(message, file=file)
        else:
            await channel.send(message)

    asyncio.run_coroutine_threadsafe(task(), bot.loop)

# =========================
# ARDUINO SEND
# =========================
def send_arduino(cmd):
    try:
        arduino.write((cmd + "\n").encode())
        print("→ Arduino:", cmd)
    except Exception as e:
        print("Arduino error:", e)

# =========================
# SNAPSHOT
# =========================
def take_photo():
    ret, frame = cam.read()
    if not ret:
        return None

    path = f"snapshot_{int(time.time())}.jpg"
    cv2.imwrite(path, frame)
    return path

# =========================
# SERIAL LISTENER
# =========================
def read_serial():
    while running:
        if arduino.in_waiting:
            msg = arduino.readline().decode().strip()
            print("Arduino:", msg)

            if msg == "A_PRESSED":
                img = take_photo()
                send_discord("🚪 Access Request", img)

            elif msg == "ALLOW":
                send_discord("✅ Access Granted")
                send_arduino("OPEN")

            elif msg == "DENY":
                send_discord("❌ Access Denied")
                send_arduino("LOCK")

# =========================
# CAMERA WINDOW
# =========================
def camera_loop():
    global running

    while running:
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)

        # ================= UI BAR =================
        cv2.rectangle(frame, (0, 0), (800, 40), (30, 30, 30), -1)

        time_text = datetime.now().strftime("%H:%M:%S")

        cv2.putText(frame, f"Time: {time_text}",
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 255, 255), 1)

        cv2.putText(frame, "BACKUP SECURITY SYSTEM",
                    (250, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 255), 2)

        cv2.imshow("Security Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        # ================= QUIT =================
        if key == ord('q'):
            running = False
            break

        # ================= RESET =================
        elif key == ord('r'):
            send_arduino("Reset")
            print("RESET SENT")

    cam.release()
    cv2.destroyAllWindows()
    print("Camera stopped")

# =========================
# START THREADS
# =========================
def start_threads():
    t1 = threading.Thread(target=read_serial, daemon=True)
    t2 = threading.Thread(target=camera_loop, daemon=True)

    t1.start()
    t2.start()

# =========================
# BOT READY
# =========================
@bot.event
async def on_ready():
    print("Bot ready:", bot.user)
    start_threads()

# =========================
# RUN BOT
# =========================
bot.run(TOKEN)
