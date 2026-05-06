import pandas as pd

def is_ma_approaching_cross(row, prev, price, threshold_factor=0.00025):
    diff = abs(row['ma4'] - row['ma50'])
    return diff < (threshold_factor * price)


def generate_signals(df: pd.DataFrame):
    if len(df) < 210:
        return None, None
    
    row = df.iloc[-1]
    prev = df.iloc[-2]
    
    price = row['close']
    
    # Stochastic
    stoch_k = row.get('STOCHk_5_1_1', row.get('STOCHk_5_1_1', None))
    stoch_d = row.get('STOCHd_5_1_1', row.get('STOCHd_5_1_1', None))
    prev_stoch_k = prev.get('STOCHk_5_1_1', None)
    
    if stoch_k is None or stoch_d is None:
        return None, None
    
    stoch_cross_up = (prev_stoch_k <= prev.get('STOCHd_5_1_1')) and (stoch_k > stoch_d)
    stoch_cross_down = (prev_stoch_k >= prev.get('STOCHd_5_1_1')) and (stoch_k < stoch_d)
    stoch_turning_up = stoch_k > prev_stoch_k and stoch_k < 50
    stoch_turning_down = stoch_k < prev_stoch_k and stoch_k > 50
    
    # MA Cross
    green_cross_up = (prev['ma4'] <= prev['ma50']) and (row['ma4'] > row['ma50'])
    green_cross_down = (prev['ma4'] >= prev['ma50']) and (row['ma4'] < row['ma50'])
    
    # Slope after cross
    ma_bullish_slope = row['ma4'] > prev['ma4'] and row['ma50'] > prev['ma50']
    ma_bearish_slope = row['ma4'] < prev['ma4'] and row['ma50'] < prev['ma50']
    
    # White MA (200) filter
    white_bullish = price > row['ma200']
    white_bearish = price < row['ma200']
    
    # === CONFIRMED SIGNAL (Katie's full rules) ===
    confirmed = None
    if green_cross_up and stoch_cross_up and white_bullish and ma_bullish_slope:
        confirmed = {
            "type": "CONFIRMED",
            "direction": "BUY / CALL",
            "strength": "STRONG - ENTER"
        }
    elif green_cross_down and stoch_cross_down and white_bearish and ma_bearish_slope:
        confirmed = {
            "type": "CONFIRMED",
            "direction": "SELL / PUT",
            "strength": "STRONG - ENTER"
        }
    
    # === PRE-SIGNAL (Early Warning) ===
    pre = None
    approaching = is_ma_approaching_cross(row, prev, price)
    
    if approaching and (stoch_turning_up or stoch_k > stoch_d) and white_bullish:
        pre = {
            "type": "PRE-SIGNAL",
            "direction": "Potential BUY / CALL - Monitor",
            "strength": "Medium - Prepare"
        }
    elif approaching and (stoch_turning_down or stoch_k < stoch_d) and white_bearish:
        pre = {
            "type": "PRE-SIGNAL",
            "direction": "Potential SELL / PUT - Monitor",
            "strength": "Medium - Prepare"
        }
    
    return pre, confirmed
