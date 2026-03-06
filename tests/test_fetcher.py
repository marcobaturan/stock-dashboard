import pytest
import pandas as pd
from data.fetcher import fetch_stock_data, load_example_csv

def test_fetch_stock_data_success():
    # Test valid ticker
    df = fetch_stock_data("AAPL", period="5d", interval="1d")
    
    # Assert successful fetch returns a dataframe
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    
    # Assert required columns are present
    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    for col in required_columns:
        assert col in df.columns
        
    # Assert rows exist
    assert len(df) > 0

def test_fetch_stock_data_invalid_ticker():
    # Test invalid ticker
    df = fetch_stock_data("INVALID_TICKER_NAME", period="1d", interval="1d")
    
    # yfinance often returns empty dataframes for invalid tickers, which our wrapper handles
    assert df is None

def test_load_example_csv_success(tmp_path):
    # Setup dummy CSV for testing
    demo_file = tmp_path / "demo.csv"
    demo_data = "Date,Open,High,Low,Close,Adj Close,Volume\n2023-01-01,100,105,95,102,102,1000\n"
    demo_file.write_text(demo_data)
    
    # Test loading
    df = load_example_csv(str(demo_file))
    
    # Assert successful load
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    
    # Check index is datetime
    assert isinstance(df.index, pd.DatetimeIndex)

def test_load_example_csv_invalid_path():
    # Test invalid file path
    df = load_example_csv("non_existent_file.csv")
    
    # Should return None on exception
    assert df is None
