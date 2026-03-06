import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame | None:
    """Fetches historical OHLCV data for a given ticker via yfinance."""
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        if data.empty:
            return None
        
        # yfinance now returns MultiIndex columns, we need to flatten them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel('Ticker')
            
        # Cleanup: remove rows with null values in Close
        data = data.dropna(subset=["Close"])
        return data
    except Exception:
        return None

def load_example_csv(filepath: str) -> pd.DataFrame | None:
    """Loads an example CSV as an alternative to fetching from yfinance."""
    try:
        data = pd.read_csv(filepath, index_col=0, parse_dates=True)
        return data
    except Exception:
        return None
