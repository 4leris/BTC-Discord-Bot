import discord
import requests
import asyncio
import os
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # or DISCORD_BOT_TOKEN if shared

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def update_btc_price():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
            data = response.json()
            price = data["bitcoin"]["usd"]

            status = f"🪙 BTC: ${price:,.0f}"  # Comma formatting
            await client.change_presence(activity=discord.Game(name=status))
            print("✅ Updated BTC status to:", status)

        except Exception as e:
            print("❌ Error updating BTC price:", e)

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(update_btc_price())

from keep_alive import keep_alive
keep_alive()

client.run(TOKEN)
