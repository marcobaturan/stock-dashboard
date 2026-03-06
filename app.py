import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data.fetcher import fetch_stock_data, load_example_csv
from analysis.indicators import get_moving_averages, get_fibonacci, get_support_resistance
from analysis.summary import get_ai_summary

st.set_page_config(
    page_title="Stock Technical Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mandatory Disclaimer as per PROJECT.md
st.warning(
    "**DISCLAIMER:** This tool performs descriptive technical analysis only. "
    "It does not predict prices or future market behaviour. It does not constitute financial advice. "
    "For educational purposes only."
)

st.title("📈 Stock Technical Analysis Dashboard")

with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Ticker Symbol", value="AAPL", max_chars=10).upper()
    
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox("Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    with col2:
        interval = st.selectbox("Interval", options=["1d", "1wk", "1mo"], index=0)
    
    if st.button("Fetch Data", type="primary", width="stretch"):
        st.session_state["use_demo"] = False
        st.session_state["fetch_trigger"] = True
        
    st.markdown("---")
    st.write("Alternatively, load static example data:")
    if st.button("Load Demo Data (AAPL)", width="stretch"):
        st.session_state["use_demo"] = True
        st.session_state["fetch_trigger"] = True

# Data loading logic
if st.session_state.get("fetch_trigger"):
    with st.spinner("Loading data..."):
        if st.session_state.get("use_demo"):
            df = load_example_csv("data/example/AAPL_example.csv")
            data_source = "Demo Dataset (AAPL)"
        else:
            df = fetch_stock_data(ticker=ticker, period=period, interval=interval)
            data_source = f"{ticker} via yfinance"

        if df is None or df.empty:
            st.error("Failed to fetch data or data is empty. Please check the ticker symbol or try the demo.")
        else:
            st.success(f"Data loaded successfully: {data_source}")
            
            # --- Technical Indicators Calculation ---
            mas = get_moving_averages(df)
            fib = get_fibonacci(df)
            sr = get_support_resistance(df, window=20)
            
            # --- Chart Rendering ---
            st.subheader(f"Price Chart & Indicators: {data_source}")
            
            # Create subplots showing Price (row 1) and Volume (row 2)
            fig = make_subplots(
                rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=(f'Historical Price ({period})', 'Volume'), 
                row_width=[0.2, 0.7]
            )

            # 1. Candlestick
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'],
                name='Price'
            ), row=1, col=1)

            # 2. Moving Averages
            colors = {"MA20": "blue", "MA50": "orange", "MA200": "red"}
            for ma_name, ma_series in mas.items():
                fig.add_trace(go.Scatter(
                    x=df.index, y=ma_series,
                    mode='lines', name=ma_name,
                    line=dict(color=colors.get(ma_name), width=1.5)
                ), row=1, col=1)
                
            # 3. Fibonacci Levels
            fib_colors = ['rgba(255, 0, 0, 0.5)', 'rgba(255, 165, 0, 0.5)', 'rgba(255, 255, 0, 0.5)',
                        'rgba(0, 128, 0, 0.5)', 'rgba(0, 0, 255, 0.5)', 'rgba(75, 0, 130, 0.5)', 'rgba(238, 130, 238, 0.5)']
            for (level_name, price), color in zip(fib.items(), fib_colors):
                fig.add_hline(y=price, line_dash="dash", line_color=color, 
                              annotation_text=f"Fib {level_name}", annotation_position="top right", row=1, col=1)

            # 4. Volume Bar Chart
            volume_colors = ['green' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'red' for i in range(len(df))]
            fig.add_trace(go.Bar(
                x=df.index, y=df['Volume'],
                marker_color=volume_colors, name="Volume"
            ), row=2, col=1)

            # Layout updates
            fig.update_layout(
                xaxis_rangeslider_visible=False,
                height=800,
                margin=dict(l=0, r=0, t=30, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig) 
            
            # --- AI Summary ---
            st.markdown("---")
            st.subheader("🤖 AI Technical Summary")
            
            with st.expander("Generate AI Analysis Report"):
                # Compiling a prompt describing the indicators mathematically
                analysis_prompt = (
                    f"Analyze the technical indicators for {data_source}.\n"
                    f"Current Price: {df['Close'].iloc[-1]:.2f}\n"
                    f"MA20: {mas['MA20'].iloc[-1]:.2f}, MA50: {mas['MA50'].iloc[-1]:.2f}, MA200: {mas['MA200'].iloc[-1]:.2f}\n"
                    f"Fibonacci Support (0.0): {fib['0.0']:.2f}, Fibonacci Resistance (1.0): {fib['1.0']:.2f}\n"
                    f"Write a short, professional trading summary based strictly on these indicators."
                )
                
                if st.button("Generate Summary"):
                    with st.spinner("Contacting Groq AI..."):
                        summary = get_ai_summary(analysis_prompt)
                        if summary:
                            st.write(summary)
                        else:
                            st.error("Failed to generate summary. Please check the console logs.")
else:
    st.info("Please select a ticker and click 'Fetch Data' or 'Load Demo Data' to begin.")
