import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

async def send_signal(signal: dict, pair: str):
    emoji = "⚠️" if signal.get("type") == "PRE-SIGNAL" else "🚨"
    msg = f"""
{emoji} KATIE {signal['type']} {emoji}
Pair: {pair}
Direction: {signal['direction']}
Strength: {signal['strength']}
Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Expiration: 1 minute
Note: Pre = Prepare | Confirmed = Enter
No risk management applied.
    """.strip()
    
    await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=msg)
