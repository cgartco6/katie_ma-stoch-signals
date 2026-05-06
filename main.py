import asyncio
import schedule
import time
from data_fetcher import fetch_ohlcv, add_indicators
from strategy import generate_signals
from telegram_bot import send_signal
import config
import pandas as pd

async def check_all_pairs():
    for pair in config.MAJOR_PAIRS:
        try:
            df = fetch_ohlcv(pair, config.TIMEFRAME, limit=350)
            df = add_indicators(df)
            
            pre_signal, confirmed_signal = generate_signals(df)
            
            for sig in [pre_signal, confirmed_signal]:
                if sig:
                    await send_signal(sig, pair)
                    print(f"[{pd.Timestamp.now()}] {sig['type']} → {pair} | {sig['direction']}")
        except Exception as e:
            print(f"Error on {pair}: {e}")


def run_bot():
    schedule.every(30).seconds.do(lambda: asyncio.run(check_all_pairs()))
    
    print("🚀 Katie MA + Stoch Signals Bot with Pre-Signals Started")
    print(f"Monitoring {len(config.MAJOR_PAIRS)} major pairs on 1m timeframe")
    
    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    run_bot()
