"""
Stock Market Dashboard - Production Ready
A simple, robust financial dashboard for stock analysis and market trends
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf
import requests
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)


class StockAnalyzer:
    """Stock data fetcher and analyzer using yfinance"""
    
    def __init__(self):
        self.cache_duration = 300  # 5 minutes
    
    @st.cache_data(ttl=300)
    def get_stock_data(_self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Fetch stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            return df
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    @st.cache_data(ttl=300)
    def get_stock_info(_self, symbol: str) -> Optional[Dict]:
        """Get stock information and metrics"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info
        except Exception as e:
            st.error(f"Error fetching info for {symbol}: {e}")
            return None
    
    def calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily and cumulative returns"""
        df['Daily_Return'] = df['Close'].pct_change() * 100
        df['Cumulative_Return'] = (1 + df['Close'].pct_change()).cumprod() - 1
        return df
    
    def calculate_volatility(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """Calculate rolling volatility"""
        df['Volatility'] = df['Daily_Return'].rolling(window=window).std()
        return df
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate moving averages"""
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        return df


class MarketDataFetcher:
    """Fetch market indices and sector data"""
    
    @st.cache_data(ttl=300)
    def get_market_indices(_self) -> Dict[str, float]:
        """Get major market indices"""
        indices = {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'NASDAQ': '^IXIC',
            'Russell 2000': '^RUT'
        }
        
        data = {}
        for name, symbol in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    data[name] = {
                        'value': current,
                        'change': change
                    }
            except:
                data[name] = {'value': 0, 'change': 0}
        
        return data
    
    @st.cache_data(ttl=3600)
    def get_sector_performance(_self) -> pd.DataFrame:
        """Get sector ETF performance"""
        sectors = {
            'Technology': 'XLK',
            'Healthcare': 'XLV',
            'Financials': 'XLF',
            'Energy': 'XLE',
            'Consumer Discretionary': 'XLY',
            'Industrials': 'XLI',
            'Materials': 'XLB',
            'Real Estate': 'XLRE',
            'Utilities': 'XLU',
            'Consumer Staples': 'XLP',
            'Communication': 'XLC'
        }
        
        sector_data = []
        for sector, etf in sectors.items():
            try:
                ticker = yf.Ticker(etf)
                hist = ticker.history(period='1mo')
                if not hist.empty:
                    mtd_return = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / 
                                 hist['Close'].iloc[0]) * 100
                    sector_data.append({
                        'Sector': sector,
                        'ETF': etf,
                        'MTD_Return': mtd_return
                    })
            except:
                continue
        
        return pd.DataFrame(sector_data).sort_values('MTD_Return', ascending=False)


class NewsAnalyzer:
    """Simple news sentiment analyzer"""
    
    @st.cache_data(ttl=1800)
    def get_market_sentiment(_self) -> str:
        """Get overall market sentiment based on index performance"""
        try:
            sp500 = yf.Ticker('^GSPC')
            hist = sp500.history(period='5d')
            
            if hist.empty:
                return "Neutral"
            
            recent_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / 
                           hist['Close'].iloc[0]) * 100
            
            if recent_change > 2:
                return "Very Bullish 🚀"
            elif recent_change > 0.5:
                return "Bullish 📈"
            elif recent_change > -0.5:
                return "Neutral ➡️"
            elif recent_change > -2:
                return "Bearish 📉"
            else:
                return "Very Bearish 🔻"
        except:
            return "Neutral ➡️"


def create_price_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Create interactive price chart with volume"""
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ))
    
    # Add moving averages if available
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['SMA_20'],
            name='SMA 20',
            line=dict(color='orange', width=1)
        ))
    
    if 'SMA_50' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['SMA_50'],
            name='SMA 50',
            line=dict(color='blue', width=1)
        ))
    
    fig.update_layout(
        title=f'{symbol} Price Chart',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        height=500,
        template='plotly_white',
        xaxis_rangeslider_visible=False
    )
    
    return fig


def create_volume_chart(df: pd.DataFrame) -> go.Figure:
    """Create volume chart"""
    colors = ['red' if row['Close'] < row['Open'] else 'green' 
              for _, row in df.iterrows()]
    
    fig = go.Figure(data=[go.Bar(
        x=df.index,
        y=df['Volume'],
        marker_color=colors,
        name='Volume'
    )])
    
    fig.update_layout(
        title='Trading Volume',
        yaxis_title='Volume',
        xaxis_title='Date',
        height=250,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def create_returns_chart(df: pd.DataFrame) -> go.Figure:
    """Create cumulative returns chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Cumulative_Return'] * 100,
        fill='tozeroy',
        name='Cumulative Return',
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        title='Cumulative Returns',
        yaxis_title='Return (%)',
        xaxis_title='Date',
        height=300,
        template='plotly_white'
    )
    
    return fig


def create_sector_chart(sector_df: pd.DataFrame) -> go.Figure:
    """Create sector performance chart"""
    colors = ['green' if x > 0 else 'red' for x in sector_df['MTD_Return']]
    
    fig = go.Figure(data=[go.Bar(
        x=sector_df['MTD_Return'],
        y=sector_df['Sector'],
        orientation='h',
        marker_color=colors,
        text=sector_df['MTD_Return'].round(2),
        textposition='auto',
    )])
    
    fig.update_layout(
        title='Sector Performance (MTD %)',
        xaxis_title='Return (%)',
        yaxis_title='Sector',
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def main():
    """Main application"""
    
    # Initialize analyzers
    stock_analyzer = StockAnalyzer()
    market_fetcher = MarketDataFetcher()
    news_analyzer = NewsAnalyzer()
    
    # Header
    st.title("📊 Stock Market Dashboard")
    st.markdown("*Real-time stock analysis and market insights*")
    
    # Sidebar
    st.sidebar.header("🎯 Configuration")
    
    # Stock selection
    popular_stocks = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-B',
        'JPM', 'V', 'WMT', 'DIS', 'NFLX', 'PYPL', 'INTC', 'AMD'
    ]
    
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        selected_stock = st.selectbox(
            "Select Stock",
            options=popular_stocks,
            index=0
        )
    with col2:
        if st.button("🔄"):
            st.cache_data.clear()
            st.rerun()
    
    # Custom stock input
    custom_stock = st.sidebar.text_input(
        "Or enter custom ticker:",
        placeholder="e.g., AAPL"
    ).upper()
    
    if custom_stock:
        selected_stock = custom_stock
    
    # Time period selection
    period = st.sidebar.selectbox(
        "Time Period",
        options=['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'],
        index=3
    )
    
    # Analysis options
    st.sidebar.markdown("---")
    show_ma = st.sidebar.checkbox("Show Moving Averages", value=True)
    show_volume = st.sidebar.checkbox("Show Volume", value=True)
    show_returns = st.sidebar.checkbox("Show Returns Analysis", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📚 About
    This dashboard provides real-time stock market analysis using Yahoo Finance data.
    
    **Features:**
    - Real-time price data
    - Technical indicators
    - Market indices
    - Sector performance
    
    **Data updates every 5 minutes**
    """)
    
    # Main content
    try:
        # Fetch stock data
        with st.spinner(f'Fetching data for {selected_stock}...'):
            df = stock_analyzer.get_stock_data(selected_stock, period)
            stock_info = stock_analyzer.get_stock_info(selected_stock)
        
        if df is None or df.empty:
            st.error(f"❌ Could not fetch data for {selected_stock}. Please check the ticker symbol.")
            return
        
        # Calculate metrics
        df = stock_analyzer.calculate_returns(df)
        df = stock_analyzer.calculate_volatility(df)
        if show_ma:
            df = stock_analyzer.calculate_moving_averages(df)
        
        # Stock Information Header
        if stock_info:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                current_price = df['Close'].iloc[-1]
                previous_price = df['Close'].iloc[-2]
                price_change = current_price - previous_price
                price_change_pct = (price_change / previous_price) * 100
                
                st.metric(
                    label="Current Price",
                    value=f"${current_price:.2f}",
                    delta=f"{price_change_pct:+.2f}%"
                )
            
            with col2:
                day_high = df['High'].iloc[-1]
                day_low = df['Low'].iloc[-1]
                st.metric(
                    label="Day Range",
                    value=f"${day_low:.2f} - ${day_high:.2f}"
                )
            
            with col3:
                volume = df['Volume'].iloc[-1]
                st.metric(
                    label="Volume",
                    value=f"{volume/1e6:.2f}M"
                )
            
            with col4:
                market_cap = stock_info.get('marketCap', 0)
                if market_cap:
                    st.metric(
                        label="Market Cap",
                        value=f"${market_cap/1e9:.2f}B"
                    )
                else:
                    st.metric(label="Market Cap", value="N/A")
            
            with col5:
                pe_ratio = stock_info.get('trailingPE', 0)
                if pe_ratio:
                    st.metric(
                        label="P/E Ratio",
                        value=f"{pe_ratio:.2f}"
                    )
                else:
                    st.metric(label="P/E Ratio", value="N/A")
        
        # Price Chart
        st.plotly_chart(create_price_chart(df, selected_stock), use_container_width=True)
        
        # Volume Chart
        if show_volume:
            st.plotly_chart(create_volume_chart(df), use_container_width=True)
        
        # Additional Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if show_returns:
                st.plotly_chart(create_returns_chart(df), use_container_width=True)
            
            # Performance Metrics
            st.subheader("📈 Performance Metrics")
            
            metrics_df = pd.DataFrame({
                'Period': ['1 Week', '1 Month', '3 Months', 'YTD', '1 Year'],
                'Return (%)': [
                    ((df['Close'].iloc[-1] - df['Close'].iloc[-5]) / df['Close'].iloc[-5] * 100) if len(df) > 5 else np.nan,
                    ((df['Close'].iloc[-1] - df['Close'].iloc[-21]) / df['Close'].iloc[-21] * 100) if len(df) > 21 else np.nan,
                    ((df['Close'].iloc[-1] - df['Close'].iloc[-63]) / df['Close'].iloc[-63] * 100) if len(df) > 63 else np.nan,
                    ((df['Close'].iloc[-1] - df[df.index.year == datetime.now().year]['Close'].iloc[0]) / 
                     df[df.index.year == datetime.now().year]['Close'].iloc[0] * 100) if len(df[df.index.year == datetime.now().year]) > 0 else np.nan,
                    ((df['Close'].iloc[-1] - df['Close'].iloc[-252]) / df['Close'].iloc[-252] * 100) if len(df) > 252 else np.nan,
                ]
            })
            
            # Color code returns
            def color_returns(val):
                if pd.isna(val):
                    return ''
                color = 'green' if val > 0 else 'red'
                return f'color: {color}'
            
            st.dataframe(
                metrics_df.style.applymap(color_returns, subset=['Return (%)']),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            # Volatility Chart
            st.subheader("📊 Volatility Analysis")
            
            vol_fig = go.Figure()
            vol_fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Volatility'],
                fill='tozeroy',
                name='20-Day Volatility',
                line=dict(color='#ff7f0e')
            ))
            
            vol_fig.update_layout(
                yaxis_title='Volatility (%)',
                xaxis_title='Date',
                height=300,
                template='plotly_white',
                showlegend=False
            )
            
            st.plotly_chart(vol_fig, use_container_width=True)
            
            # Statistical Summary
            st.subheader("📊 Statistical Summary")
            
            stats_df = pd.DataFrame({
                'Metric': ['Average Price', 'Std Deviation', 'Max Price', 'Min Price', 'Avg Volume'],
                'Value': [
                    f"${df['Close'].mean():.2f}",
                    f"${df['Close'].std():.2f}",
                    f"${df['High'].max():.2f}",
                    f"${df['Low'].min():.2f}",
                    f"{df['Volume'].mean()/1e6:.2f}M"
                ]
            })
            
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Market Overview Section
        st.markdown("---")
        st.header("🌍 Market Overview")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Major Indices")
            
            indices = market_fetcher.get_market_indices()
            
            for name, data in indices.items():
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.metric(
                        label=name,
                        value=f"{data['value']:.2f}",
                        delta=f"{data['change']:+.2f}%"
                    )
        
        with col2:
            st.subheader("Market Sentiment")
            
            sentiment = news_analyzer.get_market_sentiment()
            
            st.markdown(f"### {sentiment}")
            st.markdown("*Based on recent S&P 500 performance*")
            
            # Add simple sentiment gauge
            sentiment_score = 0
            if "Very Bullish" in sentiment:
                sentiment_score = 100
            elif "Bullish" in sentiment:
                sentiment_score = 75
            elif "Neutral" in sentiment:
                sentiment_score = 50
            elif "Bearish" in sentiment:
                sentiment_score = 25
            else:
                sentiment_score = 0
            
            st.progress(sentiment_score / 100)
        
        # Sector Performance
        st.markdown("---")
        st.header("🏭 Sector Performance")
        
        sector_df = market_fetcher.get_sector_performance()
        
        if not sector_df.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.plotly_chart(create_sector_chart(sector_df), use_container_width=True)
            
            with col2:
                st.subheader("Top Performers")
                top_sectors = sector_df.head(3)
                for _, row in top_sectors.iterrows():
                    st.metric(
                        label=row['Sector'],
                        value=row['ETF'],
                        delta=f"{row['MTD_Return']:+.2f}%"
                    )
                
                st.subheader("Bottom Performers")
                bottom_sectors = sector_df.tail(3)
                for _, row in bottom_sectors.iterrows():
                    st.metric(
                        label=row['Sector'],
                        value=row['ETF'],
                        delta=f"{row['MTD_Return']:+.2f}%"
                    )
        
        # Data Export
        st.markdown("---")
        with st.expander("📥 Export Data"):
            st.subheader("Download Historical Data")
            
            csv = df.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_stock}_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            st.dataframe(df.tail(20), use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please try refreshing the page or selecting a different stock.")


if __name__ == "__main__":
    main()
