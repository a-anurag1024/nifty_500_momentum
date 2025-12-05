import pandas as pd
import numpy as np


def calculate_rsi(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """
    Calculates RSI.
    Formula: 100 - (100 / (1 + RS))
    """
    delta = df['Close'].diff()
    
    # Separate gains and losses
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    # Calculate EMA of gains and losses (Wilder's Smoothing)
    # alpha = 1/length mimics Wilder's method
    avg_gain = gain.ewm(alpha=1/length, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/length, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(0)

def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    Calculates MACD.
    Returns DataFrame with columns: ['MACD', 'Signal', 'Histogram']
    """
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    })

def calculate_sma(df: pd.DataFrame, length: int = 50) -> pd.Series:
    return df['Close'].rolling(window=length).mean()

def calculate_ema(df: pd.DataFrame, length: int = 20) -> pd.Series:
    return df['Close'].ewm(span=length, adjust=False).mean()

def calculate_roc(df: pd.DataFrame, length: int = 10) -> pd.Series:
    """
    Rate of Change: ((Price_t - Price_t-n) / Price_t-n) * 100
    """
    return df['Close'].pct_change(periods=length) * 100

def calculate_adx(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
    """
    Calculates ADX (Wilder's Smoothing).
    Returns DataFrame with ['ADX', '+DI', '-DI']
    """
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    # 1. Calculate TR (True Range)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # 2. Calculate Directional Movement (+DM, -DM)
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    
    # Convert to Series for pandas operations
    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)
    
    # 3. Smooth TR, +DM, -DM (Wilder's Smoothing: alpha=1/length)
    tr_smooth = tr.ewm(alpha=1/length, adjust=False).mean()
    plus_dm_smooth = plus_dm.ewm(alpha=1/length, adjust=False).mean()
    minus_dm_smooth = minus_dm.ewm(alpha=1/length, adjust=False).mean()
    
    # 4. Calculate +DI and -DI
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)
    
    # 5. Calculate DX and ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.ewm(alpha=1/length, adjust=False).mean()
    
    return pd.DataFrame({
        'ADX': adx,
        '+DI': plus_di,
        '-DI': minus_di
    })

def calculate_relative_volume(df: pd.DataFrame, ma_length: int = 20) -> pd.Series:
    # Use fillna(1) to avoid division by zero errors at the start of data
    vol_sma = df['Volume'].rolling(window=ma_length).mean()
    return (df['Volume'] / vol_sma).fillna(0)

def calculate_momentum_12m_1m(df: pd.DataFrame) -> pd.Series:
    """
    (Price_t-21 / Price_t-252) - 1
    """
    if len(df) < 252:
        return pd.Series(np.nan, index=df.index)
        
    return (df['Adj Close'].shift(21) / df['Adj Close'].shift(252)) - 1