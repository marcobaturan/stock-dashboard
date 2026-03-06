import pandas as pd
import numpy as np

def get_moving_averages(data: pd.DataFrame) -> dict[str, pd.Series]:
    """Calculates 20, 50, and 200-day moving averages using pandas."""
    if "Close" not in data.columns:
        return {}

    return {
        "MA20": data["Close"].rolling(window=20).mean(),
        "MA50": data["Close"].rolling(window=50).mean(),
        "MA200": data["Close"].rolling(window=200).mean(),
    }

def get_fibonacci(data: pd.DataFrame) -> dict[str, float]:
    """Calculates Fibonacci retracement levels based on historical minimum and maximum."""
    if "High" not in data.columns or "Low" not in data.columns:
        return {}
        
    max_price = data["High"].max()
    min_price = data["Low"].min()
    diff = max_price - min_price

    levels = {
        "0.0": min_price,
        "0.236": min_price + (diff * 0.236),
        "0.382": min_price + (diff * 0.382),
        "0.5": min_price + (diff * 0.5),
        "0.618": min_price + (diff * 0.618),
        "0.786": min_price + (diff * 0.786),
        "1.0": max_price,
    }
    
    return levels

def get_support_resistance(data: pd.DataFrame, window: int = 20) -> dict[str, list[float]]:
    """Finds supports (local minima) and resistances (local maxima) using a rolling window."""
    if "Close" not in data.columns:
        return {"supports": [], "resistances": []}

    close_prices = data["Close"].values
    
    # Using pandas rolling logic for consistency and complying with constraints (no ta-lib)
    # Finding local minima and maxima
    # Note: scipy.signal could be used but the prompt specifies "using pandas".
    # Implementation entirely in Pandas:
    
    series = data["Close"]
    
    # Calculate rolling min and max
    rolling_min = series.rolling(window=window, center=True).min()
    rolling_max = series.rolling(window=window, center=True).max()
    
    # A point is a local min/max if it matches the rolling min/max
    supports_idx = series[series == rolling_min].index
    resistances_idx = series[series == rolling_max].index
    
    # Extract unique values and convert to list
    supports = np.unique(series[supports_idx].values).tolist()
    resistances = np.unique(series[resistances_idx].values).tolist()
    
    return {
        "supports": supports,
        "resistances": resistances
    }
