# 📊 XYZ Financial Analysis

## 🌟 Overview
Streamlit-based financial analysis dashboard for the **Data Visualization and Training** course. Analyze crypto and Borsa Istanbul stocks with:

- 📈 Price trend analysis
- 📊 Volume analysis  
- 🔍 Custom date range selection
- 💹 Key metrics (Last Price, High, Low, Average)

## 🚀 Features
| Feature | Description |
|---------|-------------|
| **Crypto** | BTC-USD, ETH-USD, XRP-USD, DOT-USD, DOGE-USD, AVAX-USD, BNB-USD |
| **Stocks** | ASELSAN (ASELS.IS), THY (THYAO.IS), GARANTI (GARAN.IS), AKBNK (AKBNK.IS), BJK (BJKAS.IS) |
| **Time Range** | Flexible 1-360 days selection |
| **Metrics** | Last price, period high/low, average |
| **Charts** | Price & volume line charts, raw data table |

## 📦 Installation

```bash
# Install dependencies
pip install streamlit yfinance pandas pillow

# Run the app
streamlit run task_1.py
```

## 🛠️ Usage

1. **Sidebar**: Select asset class (Crypto / Stock)
2. **Choose asset** (e.g., BTC or ASELSAN)
3. **Set date range**
4. **View results**:
   - Metric cards
   - Price chart
   - Volume chart
   - Raw data table

## 📁 Project Structure
```
├── task_1.py          # Main Streamlit app
├── finance.png        # Sidebar logo
├── README.md          # This file
└── Untitled-1.ipynb   # Jupyter notebook (optional)
```

## 🔧 For Developers
- **Logo**: `finance.png` auto-loads in sidebar
- **Data Source**: Yahoo Finance API (`yfinance`)
- **Currency**: Crypto=$, BIST=₺ (TRY)
- **Error Handling**: Empty data & invalid date range validation

## 📈 Screenshots
![Finance App](finance.png)

## 🚀 Quick Start
```bash
streamlit run task_1.py --server.port 8501
```

Access at **http://localhost:8501**!

## 📝 Contributing
Welcome pull requests! Add new assets, metrics, or charts.

---

⭐ **Data Visualization and Training** project | Built with ❤️ using Streamlit
