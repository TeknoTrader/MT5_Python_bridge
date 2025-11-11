# 📈 MT5 Trading Bridge - Streamlit Web Interface

A **web-based trading interface** built with **Streamlit** and **Python**, designed to connect directly to MetaTrader 5 platform for seamless trading operations with advanced position management and filtering capabilities.

This tool enables traders to execute trades, monitor positions, and manage their MT5 account through an intuitive web interface with real-time updates and intelligent filtering.

I developed it in order to let other people understand better how to create a proper dashboard and, obviouly, how to use the MQL5 API to see account informations and trade.

## 🌐 Deployment Note

**⚠️ IMPORTANT**: This application requires **MetaTrader 5** which is **Windows-only** software. Therefore:
- ❌ **Cannot be hosted on Streamlit Cloud** (uses Linux servers)
- ✅ **Can be hosted locally** on Windows machines
- ✅ **Can be deployed on Windows VPS** (Contabo, Hostinger, Azure)
- ✅ **Can be shared via ngrok** for remote access

See [Installation & Deployment](#-installation--deployment) section for detailed setup instructions.

---

## 🧩 Features

### 💹 Real-Time Trading Interface
Execute trades directly from your browser:
- **Buy/Sell orders** with one-click execution
- **Stop Loss & Take Profit** configuration in pips
- **Custom lot sizing** with decimal precision
- **Symbol selection** for any MT5 instrument
- **Magic number** for order identification
- **Custom comments** for trade labeling

**Key Capabilities:**
- Direct MT5 API integration via MetaTrader5 library
- Real-time price updates
- Order validation and error handling
- Immediate execution feedback
- Multi-symbol support

---

### 🔍 Advanced Position Filtering
Intelligent position management system:
- **Filter by comment** to show only specific trades
- **View all positions** or filter by app-created trades
- **Real-time profit tracking** with color-coded indicators
- **Detailed position information**:
  - Entry price and current price
  - Volume (lot size)
  - Stop Loss and Take Profit levels
  - Profit/Loss in account currency
  - Trade type (Buy/Sell)

**Filtering Benefits:**
- Isolate trades created by this app
- Manage multiple strategies separately
- Track performance by trade category
- Avoid accidental closure of other positions

---

### ⚡ Auto-Refresh & Manual Updates
Stay synchronized with your trading account:
- **Auto-refresh mode** with customizable intervals (1-30 seconds)
- **Manual refresh button** for on-demand updates
- **Live position count** display
- **Total profit calculation** for filtered positions
- **Real-time balance** and equity monitoring

---

### 🎯 Bulk Position Management
Efficient portfolio management:
- **Close all filtered positions** with one click
- **Individual position closure** from expanded details
- **Success/failure tracking** for bulk operations
- **Confirmation feedback** with visual indicators
- **Automatic page refresh** after operations

---

### 🔐 Secure Account Connection
Safe and encrypted connection to MT5:
- **Account number** input
- **Password protection** (masked input)
- **Server selection** for broker compatibility
- **Connection status indicator** (🟢/🔴)
- **Account info display** (Balance, Equity, Currency)
- **Easy connect/disconnect** controls

---

## 📦 Installation & Deployment

### Prerequisites
- **Windows OS** (Windows 10/11 or Windows Server)
- **MetaTrader 5** installed and configured
- **Python 3.8 or higher**
- **pip package manager**

---

### 🖥️ Local Installation

#### 1. Clone the repository
```bash
git clone https://github.com/TeknoTrader/MT5-Trading-Bridge.git
cd MT5-Trading-Bridge
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run the application
```bash
streamlit run MQL5_bridge.py
```

#### 4. Open your browser
The app will automatically open at `http://localhost:8501`

---

### 🌐 Remote Access with ngrok (FREE)

To access your app from anywhere:

#### 1. Download ngrok
Visit: [https://ngrok.com/download](https://ngrok.com/download)

#### 2. Start your Streamlit app
```bash
streamlit run MQL5_bridge.py
```

#### 3. In another terminal, expose the app
```bash
ngrok http 8501
```

#### 4. Share the ngrok URL
Ngrok will provide a public URL like: `https://abc123.ngrok-free.app`

**Advantages:**
- ✅ Completely FREE
- ✅ Access from mobile/tablet
- ✅ Share with team members
- ✅ No complex network configuration

**Limitations:**
- ❌ PC must stay on
- ❌ URL changes on restart (free plan)
- ❌ 40 requests/minute limit (free plan)

---

### ☁️ Windows VPS Deployment

For 24/7 availability, deploy on a Windows VPS:

**Examples of valid Providers** (in my opinion):

| Provider | Price | RAM | Notes |
|----------|-------|-----|-------|
| **Contabo** | ~€5/month | 4GB | Best value |
| **Hostinger VPS** | ~€8/month | 2GB | Good support |
| **Kamatera** | 30 days FREE | 2GB | Trial period |
| **Azure** | Pay-as-you-go | Custom | Enterprise option |

**Setup Steps:**
1. Purchase Windows VPS
2. Install MetaTrader 5
3. Install Python 3.8+
4. Clone repository and install requirements
5. Run Streamlit app
6. Configure firewall for port 8501
7. (Optional) Use reverse proxy for HTTPS

---

## 🚀 Usage

### Initial Setup

1. **Launch the application**
   ```bash
   streamlit run MQL5_bridge.py
   ```

2. **Configure MT5 connection** (in sidebar):
   - Enter your MT5 account number
   - Input password (securely masked)
   - Specify broker server name
   - Click "🔌 Connetti a MT4"

3. **Verify connection**:
   - Check for green "🟢 Connesso" indicator
   - Review displayed balance and equity

---

### Executing Trades

1. **Select trading symbol** (e.g., EURUSD, GBPUSD)
2. **Set position size** in lots (e.g., 0.1)
3. **Configure risk parameters**:
   - Stop Loss in pips (0 = no SL)
   - Take Profit in pips (0 = no TP)
4. **Add comment** for trade identification
5. **Click BUY or SELL** button
6. **Confirm execution** via success message

---

### Managing Positions

#### View All Positions
- Default view shows all open positions
- Unchecked filter displays complete portfolio

#### Filter Specific Trades
1. Enable "Mostra solo posizioni con commento specifico"
2. Enter comment to filter (e.g., "Streamlit Trade")
3. View only matching positions

#### Close Individual Position
1. Expand position details
2. Review profit/loss
3. Click "❌ Chiudi Posizione #[ticket]"
4. Confirm closure

#### Close Multiple Positions
1. Filter desired positions
2. Click "⚠️ CHIUDI TUTTE LE [N] POSIZIONI"
3. Wait for bulk closure completion
4. Review success/failure counts

---

### Auto-Refresh Configuration

**Enable Auto-Refresh:**
1. Check "🔄 Aggiornamento Automatico"
2. Select refresh interval (1-30 seconds)
3. Monitor real-time updates

**Recommended Settings:**
- **Day trading**: 1-3 seconds
- **Swing trading**: 5-10 seconds
- **Position monitoring**: 30 seconds

---

## 📁 Project Structure

```
MT5-Trading-Bridge/
├── MQL5_bridge.py         # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔧 Technical Details

**Built with:**
- **Streamlit**: Modern web framework for data applications
- **MetaTrader5**: Official Python API for MT5 connectivity
- **Pandas**: Data manipulation and position tracking
- **Python datetime**: Time handling for orders

**API Integration:**
- Direct connection to MT5 terminal via local API
- Real-time market data retrieval
- Order execution with deviation tolerance
- Position tracking and management
- Account information queries

**Order Parameters:**
- **Action**: `TRADE_ACTION_DEAL` for instant execution
- **Filling Type**: `ORDER_FILLING_IOC` (Immediate or Cancel)
- **Time in Force**: `ORDER_TIME_GTC` (Good Till Cancelled)
- **Magic Number**: 234000 (default identifier)
- **Deviation**: 20 points (slippage tolerance)

---

## 💼 Use Cases

This tool is perfect for:
- **Retail Traders** executing manual trades via web interface
- **Algorithm Developers** testing order execution logic
- **Remote Traders** accessing MT5 from mobile devices
- **Portfolio Managers** monitoring multiple positions
- **Strategy Testers** managing trades with custom labels
- **Trading Teams** sharing live trading interface

---

## ⚠️ Risk Disclaimer & Important Notes

**CRITICAL WARNINGS:**

### Trading Risks
- ⚠️ **This is LIVE TRADING software** - real money at risk
- ⚠️ **All trades are immediately executed** on your MT5 account
- ⚠️ **No undo function** - closed positions cannot be reopened
- ⚠️ **Market risk** - losses can exceed initial investment (with leverage)
- ⚠️ **Technology risk** - connection issues may prevent order management

### Security Considerations
- 🔐 **Never share your ngrok URL** publicly
- 🔐 **Use strong passwords** for MT5 accounts
- 🔐 **Secure your Windows machine** if hosting
- 🔐 **Enable MT5 IP filtering** when possible
- 🔐 **Monitor login attempts** to your VPS

### Best Practices
1. **Test on demo account first** before using real money
2. **Always set Stop Loss** to limit potential losses
3. **Start with small position sizes** (0.01 lots)
4. **Monitor your trades regularly** - don't rely solely on auto-refresh
5. **Keep MT5 terminal open** while app is running
6. **Use proper risk management** (1-2% per trade maximum)
7. **Verify broker compatibility** before deployment

**The author assumes NO liability for trading losses incurred through use of this software.**

---

## 🐛 Troubleshooting

### Connection Issues

**Problem**: "❌ Inizializzazione MT5 fallita"
- **Solution**: Ensure MT5 terminal is running and logged in
- Check that Python and MT5 are same architecture (both 32-bit or 64-bit)

**Problem**: "❌ Login fallito"
- **Solution**: Verify account number, password, and server name
- Check MT5 terminal can connect to broker server
- Confirm account allows API connections (check broker settings)

### Order Execution Errors

**Problem**: "❌ Simbolo [SYMBOL] non trovato"
- **Solution**: Check symbol name spelling (e.g., EURUSD not EUR/USD)
- Ensure symbol is available in MT5 Market Watch
- Right-click Market Watch → Show All to enable symbol

**Problem**: Order fails with retcode error
- **Solution**: Check available margin for position size
- Verify market is open (avoid weekends/holidays)
- Reduce position size if insufficient margin
- Check broker's minimum lot size requirements

### Position Management Issues

**Problem**: Positions not appearing in filtered view
- **Solution**: Verify comment matches exactly (case-sensitive)
- Check "Filter enabled" checkbox is checked
- Click manual refresh button

**Problem**: Cannot close position
- **Solution**: Ensure market is open for that symbol
- Check MT5 terminal connection is active
- Verify position still exists (not closed elsewhere)

---

## 🔄 Updates & Version History

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ Basic buy/sell functionality
- ✅ Position filtering by comment
- ✅ Auto-refresh capability
- ✅ Bulk position closure
- ✅ Real-time profit tracking

### Planned Features (Roadmap)
- [ ] Pending order placement (Limit, Stop)
- [ ] Position modification (edit SL/TP)
- [ ] Trade history analysis
- [ ] Performance statistics dashboard
- [ ] Multi-account support
- [ ] Email/Telegram notifications
- [ ] Risk calculator integration
- [ ] Chart visualization with trades
- [ ] Custom trading templates
- [ ] Trade journal functionality

---

## 💬 Feedback & Contributions

If you find this tool useful or have suggestions:
- Open an **[Issue](../../issues)** for bug reports
- Submit a **Pull Request** for improvements
- Share your use cases and feedback
- Star ⭐ the repository if helpful

**Contribution Guidelines:**
- Follow existing code style
- Test thoroughly on demo account
- Document new features
- Add error handling for edge cases

---

## 📜 License

Distributed under the **MIT License** — free to use, modify, and distribute with proper attribution.

---

## 👤 Author

**Nicola Chimenti**  
Business Analyst & MQL Developer

🎓 Degree in Digital Economics  
💼 Specialist in Trading Software Development & Automation  
📊 Focus: Algorithmic Trading, Data Analysis, Strategy Development

### 📫 Contact & Resources

🔗 **Professional Profiles:**
- [LinkedIn](https://www.linkedin.com/in/nicolachimenti?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
- [MQL5 Profile](https://www.mql5.com/it/users/teknotrader) (Trading Software Portfolio)
- [Fiverr Profile](https://www.fiverr.com/sellers/teknonicola/) (Client Reviews)
- [GitHub](https://github.com/TeknoTrader) (Open Source Projects)

📧 **Email**: nicola.chimenti.work@gmail.com

🛒 **Free MT4/MT5 Tools**: [MQL5 Market](https://www.mql5.com/it/users/teknotrader/seller#!category=2)

---

## 🙏 Acknowledgments

This project was developed to bridge the gap between MetaTrader 5's powerful trading capabilities and modern web interfaces, making trading more accessible and manageable.

**Special Thanks:**
- MetaQuotes for the MetaTrader5 Python API
- Streamlit team for excellent documentation
- Trading community for feedback and testing

---

## ❓ FAQ

**Q: Does this work with MT4?**  
A: The library is called MetaTrader5 but it can connect to both MT4 and MT5 platforms. Just ensure you have the Python API enabled.

**Q: Can I use this on Mac or Linux?**  
A: No, MetaTrader 5 is Windows-only. You would need a Windows VM or VPS.

**Q: Is my trading data secure?**  
A: All connections are local to your machine. If using ngrok, traffic is tunneled securely. Never share your ngrok URL publicly.

**Q: Can I automate trading strategies with this?**  
A: This tool is designed for manual trading via web interface. For automation, consider developing an Expert Advisor (EA) in MQL5.

**Q: Does it work with all brokers?**  
A: Yes, as long as your broker supports MetaTrader 5 and allows API connections. Check with your broker if unsure.

**Q: What happens if my internet disconnects?**  
A: Open positions remain in MT5. The web interface will show connection errors until internet is restored.

**Q: Can multiple users access the same app?**  
A: Yes with ngrok or VPS deployment, but all users will control the SAME MT5 account. Use with caution.

**Q: How do I enable MT5 API access?**  
A: In MT5 terminal: Tools → Options → Expert Advisors → Check "Allow automated trading"

---

## 📚 Additional Resources

### Learning Materials
- [MetaTrader 5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MQL5 Trading Forum](https://www.mql5.com/en/forum)

### Related Projects
- [SEASONALITY Analysis Tool](https://github.com/TeknoTrader/SEASONALITY) - Market pattern analysis
- [Organization Tools](https://github.com/TeknoTrader/OrganizationTools) - Task management

### Broker Resources
- Check if your broker supports MT5 API
- Review broker's automation policy
- Verify minimum lot sizes and spreads

---

⭐ **If you find this tool helpful, please star the repository to help others discover it!**

---

**VAT Code**: 02674000464  
**© 2024 Nicola Chimenti. All rights reserved.**

---

## 🔒 Security Best Practices

When deploying this application:

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data (future enhancement)
3. **Limit ngrok URL sharing** to trusted individuals only
4. **Enable MT5 IP whitelisting** when available
5. **Use VPN** when accessing remotely
6. **Monitor MT5 logs** for suspicious activity
7. **Set account permissions** to read-only when possible (viewing only)
8. **Regularly update** Python packages for security patches

```bash
# Update all packages
pip install --upgrade -r requirements.txt
```

---

**Happy Trading! 📈💹**

Remember: Successful trading requires discipline, risk management, and continuous learning. This tool is just one part of your trading toolkit.
