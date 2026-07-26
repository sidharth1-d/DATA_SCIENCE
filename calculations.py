import pandas as pd
import numpy as np

def calculate_volatility(df, window=20):
    """Calculate historical volatility (annualized)."""
    if df.empty or len(df) < window:
        return df
    
    # Calculate daily returns
    df['Returns'] = df['Close'].pct_change()
    
    # Calculate rolling standard deviation of returns (daily volatility)
    df['Daily_Vol'] = df['Returns'].rolling(window=window).std()
    
    # Annualize volatility (assuming 252 trading days)
    df['Hist_Vol'] = df['Daily_Vol'] * np.sqrt(252) * 100
    
    return df

def calculate_technical_indicators(df):
    """Calculate moving averages, RSI, and support/resistance."""
    if df.empty:
        return df
        
    # Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    # RSI (14 periods)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    # Prevent division by zero
    loss = loss.replace(0, np.nan)
    rs = gain / loss
    
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI'] = df['RSI'].fillna(100) # If loss is 0, RSI is 100
    
    # Support and Resistance (Recent 20 days max/min)
    df['Resistance'] = df['High'].rolling(window=20).max()
    df['Support'] = df['Low'].rolling(window=20).min()
    
    return df

def calculate_risk_sentiment(vix_val, rsi_val):
    """Calculate a composite risk sentiment score (0-100) and category."""
    # Simplified sentiment calculation
    # High VIX = High Risk (Fear)
    # Low RSI = Oversold (Fear), High RSI = Overbought (Greed)
    
    # Normalize VIX (assuming 10 is low, 40 is high)
    vix_score = min(max((vix_val - 10) / 30 * 100, 0), 100)
    
    # Sentiment is inverse of VIX score (High VIX = Low Sentiment/Fear)
    vix_sentiment = 100 - vix_score
    
    # Combined score (weighted)
    if pd.isna(rsi_val):
        rsi_val = 50
        
    composite_score = (vix_sentiment * 0.6) + (rsi_val * 0.4)
    
    if composite_score < 30:
        level = "Extreme Fear"
        color = "red"
    elif composite_score < 45:
        level = "Fear"
        color = "orange"
    elif composite_score < 55:
        level = "Neutral"
        color = "gray"
    elif composite_score < 70:
        level = "Greed"
        color = "green"
    else:
        level = "Extreme Greed"
        color = "darkgreen"
        
    return {
        "score": round(composite_score, 1),
        "level": level,
        "color": color
    }
