# Stock Market Dashboard 📊

A production-ready stock market analysis dashboard built with Streamlit and real-time data from Yahoo Finance.

## Features

- 📈 Real-time stock price tracking
- 📊 Technical indicators (Moving Averages, Volatility)
- 💹 Market indices overview (S&P 500, Dow Jones, NASDAQ)
- 🏭 Sector performance analysis
- 📉 Returns and performance metrics
- 📥 Data export functionality

## Live Demo

The app uses Yahoo Finance (yfinance) to fetch real-time market data with no API key required.

## Quick Deploy

### Deploy to Streamlit Cloud (Easiest)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set main file path to `app.py`
7. Click "Deploy"

### Deploy to Render

1. Fork this repository
2. Go to [render.com](https://render.com)
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

## Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd stock-market-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select a Stock**: Choose from popular stocks or enter a custom ticker
2. **Time Period**: Select analysis timeframe (1 month to max history)
3. **Analysis Options**: Toggle moving averages, volume, and returns
4. **Market Overview**: View major indices and sector performance
5. **Export Data**: Download historical data as CSV

## Technical Stack

- **Frontend**: Streamlit
- **Data Source**: Yahoo Finance (yfinance)
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

## Configuration

### Environment Variables (Optional)

No API keys or environment variables required! The app uses free Yahoo Finance data.

### Customization

Edit `app.py` to:
- Add more stock tickers to the popular stocks list
- Modify time periods
- Customize chart colors and styles
- Add additional technical indicators

## Features Breakdown

### Price Analysis
- Real-time candlestick charts
- Moving averages (20, 50, 200-day)
- Volume analysis
- High/low ranges

### Performance Metrics
- Daily, weekly, monthly returns
- Year-to-date performance
- Cumulative returns visualization
- Volatility analysis

### Market Overview
- S&P 500, Dow Jones, NASDAQ indices
- Real-time market sentiment
- Sector ETF performance
- Top/bottom performing sectors

## Data Sources

- **Stock Data**: Yahoo Finance
- **Market Indices**: Yahoo Finance
- **Sector ETFs**: SPDR Sector ETFs (XLK, XLV, XLF, etc.)

## Troubleshooting

### App not loading data
- Check your internet connection
- Verify the ticker symbol is correct
- Try clicking the refresh button (🔄)

### Deployment issues on Render
- Ensure `requirements.txt` is in the root directory
- Verify the start command includes the correct port binding
- Check Render logs for specific error messages

### Deployment issues on Streamlit Cloud
- Make sure `app.py` is in the root directory
- Check that all dependencies are in `requirements.txt`
- Review the app logs in Streamlit Cloud dashboard

## Performance

- Data cached for 5 minutes to reduce API calls
- Asynchronous data loading
- Optimized for mobile and desktop
- Auto-refresh capability

## Limitations

- Yahoo Finance free tier rate limits apply
- Historical data limited by yfinance availability
- Market data delayed by ~15 minutes (varies by exchange)

## Future Enhancements

- [ ] Portfolio tracking
- [ ] Watchlist functionality
- [ ] Price alerts
- [ ] Technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Fundamental analysis
- [ ] News integration
- [ ] Comparison tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed description

## Credits

- Built with [Streamlit](https://streamlit.io)
- Data from [Yahoo Finance](https://finance.yahoo.com)
- Charts powered by [Plotly](https://plotly.com)

---

**Note**: This dashboard is for informational purposes only. Not financial advice. Always do your own research before making investment decisions.
