import pytest
import pandas as pd
import numpy as np
from analysis.indicators import get_moving_averages, get_fibonacci, get_support_resistance

@pytest.fixture
def dummy_data():
    """Generates 100 days of dummy sequential data to test math."""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    df = pd.DataFrame({
        "Open": np.linspace(10, 110, 100),
        "High": np.linspace(12, 112, 100),
        "Low": np.linspace(8, 108, 100),
        "Close": np.linspace(11, 111, 100),
        "Volume": np.random.randint(1000, 5000, 100)
    }, index=dates)
    return df

def test_get_moving_averages(dummy_data):
    mas = get_moving_averages(dummy_data)
    
    assert isinstance(mas, dict)
    assert "MA20" in mas
    assert "MA50" in mas
    assert "MA200" in mas
    
    # Check that it returns series with correct length
    assert len(mas["MA20"]) == 100
    
    # MA20 should have 19 NaNs at start
    assert mas["MA20"].isna().sum() == 19
    # MA50 should have 49 NaNs at start
    assert mas["MA50"].isna().sum() == 49
    # MA200 should have 99 NaNs since we only have 100 periods
    assert mas["MA200"].isna().sum() == 100

def test_get_fibonacci(dummy_data):
    levels = get_fibonacci(dummy_data)
    
    assert isinstance(levels, dict)
    required_levels = ["0.0", "0.236", "0.382", "0.5", "0.618", "0.786", "1.0"]
    for level in required_levels:
        assert level in levels

    # Based on dummy data, Min Low = 8.0, Max High = 112.0
    # Difference = 104.0
    assert levels["0.0"] == 8.0
    assert levels["1.0"] == 112.0
    assert pytest.approx(levels["0.5"]) == 60.0 # 8 + (104 * 0.5)

def test_get_support_resistance(dummy_data):
    # For a purely linear trend, resistance points should be empty or just the edges
    # Let's create a sine wave data frame to test clusters properly.
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    sine_df = pd.DataFrame({
        "Close": np.sin(np.linspace(0, 4*np.pi, 100)) * 10 + 50
    }, index=dates)
    
    sr = get_support_resistance(sine_df, window=5)
    
    assert isinstance(sr, dict)
    assert "supports" in sr
    assert "resistances" in sr
    assert isinstance(sr["supports"], list)
    assert isinstance(sr["resistances"], list)
    
    # We should detect supports near 40 and resistances near 60
    assert any(39 < s < 41 for s in sr["supports"])
    assert any(59 < r < 61 for r in sr["resistances"])
