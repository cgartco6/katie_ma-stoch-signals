import ccxt
import pandas as pd
import pandas_ta as ta

def fetch_ohlcv(symbol: str, timeframe: str = '1m', limit: int = 300):
    """Fetch OHLCV data using CCXT (Binance works well for major pairs)"""
    exchange = ccxt.binance({
        'enableRateLimit': True,
    })
    ohlcv = exchange.fetch_ohlcv(symbol.replace('/', ''), timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) < 200:
        return df
    
    # Simple Moving Averages
    df['ma4'] = ta.sma(df['close'], length=4)      # Green
    df['ma50'] = ta.sma(df['close'], length=50)    # Red
    df['ma200'] = ta.sma(df['close'], length=200)  # White
    
    # Stochastic Oscillator (5,1,1)
    stoch = ta.stoch(df['high'], df['low'], df['close'],
                     k=5, d=1, smooth_k=1)
    df = pd.concat([df, stoch], axis=1)
    
    # Basic Heikin Ashi approximation
    df['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    df['ha_open'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
    df['ha_high'] = df[['high', 'ha_open', 'ha_close']].max(axis=1)
    df['ha_low'] = df[['low', 'ha_open', 'ha_close']].min(axis=1)
    
    return df
