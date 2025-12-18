# Nifty 500 Momentum Scout

A Python-based momentum trading system that combines **static technical indicators** with **LLM-powered news sentiment analysis** to identify high-conviction breakout opportunities in Nifty 500 stocks, with a focus on mid and small-cap stocks.

## 🎯 Overview

This project addresses a key limitation of traditional momentum trading: **static indicators often generate false signals in mid and small-cap stocks** due to higher volatility, lower liquidity, and operator-driven activity. By integrating news sentiment analysis, this system validates momentum signals with fundamental catalysts, significantly reducing false positives and improving signal reliability.

### Key Features

- **Multi-Strategy Momentum Filtering**: Four distinct strategies targeting different momentum regimes
- **LLM-Powered News Analysis**: Automated sentiment analysis of news articles using OpenAI
- **Automated Data Collection**: Fetches stock data (yfinance) and news (RSS feeds)
- **Performance Evaluation**: Built-in evaluation framework for backtesting and validation
- **Modular Architecture**: Clean separation between data collection, analysis, and evaluation layers

## 🧠 Core Concept

Traditional momentum indicators (RSI, MACD, ADX, etc.) identify *that* a stock is moving, but not *why*. This project adds a **news sentiment layer** to:

1. **Validate Momentum**: Price rises backed by positive news are more sustainable
2. **Identify Catalyst-Backed Breakouts**: News-driven moves often lead to multi-week trends
3. **Filter "Fake" Moves**: Eliminate speculative or manipulated price action
4. **Understand Sector Context**: Capture sector-level re-ratings and themes

## 📊 Momentum Strategies

The system implements four complementary momentum filtering strategies:

### 1. **Explosive Breakout**
Captures sudden, high-energy price expansion with:
- Relative Volume (RVOL) → Abnormal participation
- Rate of Change (ROC) → Rapid price movement
- RSI → Prevents overstretched entries

**Use Case**: Short-term momentum plays, news-driven breakouts

### 2. **Golden Momentum**
Identifies structural long-term winners with:
- 12-Month Momentum (excluding last month) → Persistence filter
- 200-day SMA → Long-term trend confirmation

**Use Case**: Position trades, institutional accumulation plays

### 3. **Reversal Hunter**
Detects early trend reversals using:
- MACD crossovers → Cycle shifts
- RSI recovery zones → Oversold bounces
- Volume confirmation → Conviction signals

**Use Case**: Mean reversion trades, bottoming patterns

### 4. **TrendSurfer**
Follows established trends with:
- ADX → Trend strength measurement
- Price above key SMAs → Trend direction
- Volume profile → Institutional participation

**Use Case**: Trend continuation, momentum riding

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Data Collection Layer                       │
│  ┌──────────────────┐         ┌─────────────────────┐      │
│  │ Stock Collector  │         │  News Collector     │      │
│  │  (yfinance)      │         │  (RSS Feeds)        │      │
│  └──────────────────┘         └─────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Static Analysis Layer                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Momentum Indicator Calculation & Strategy Filtering │  │
│  │  (RSI, MACD, ROC, ADX, SMA, Volume, etc.)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   LLM Analysis Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  News Sentiment Analysis (OpenAI)                     │  │
│  │  - Catalyst identification                            │  │
│  │  - Sentiment scoring                                  │  │
│  │  - Momentum validation                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Evaluation Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Performance Analysis & Backtesting                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
nifty_500_momentum/
├── modules/                    # Core library package
│   └── src/
│       └── nifty_500_momentum/
│           ├── analysts/       # LLM-based analysis modules
│           ├── data/           # Data collection and management
│           ├── evals/          # Evaluation and backtesting
│           ├── llm/            # LLM integration (OpenAI)
│           └── static/         # Static momentum indicators
├── scripts/                    # Executable workflows
│   ├── nifty_500_collector.py # Collect stock price data
│   ├── shortlist.py           # Apply momentum strategies
│   ├── news_collector.py      # Fetch news articles
│   ├── analysis.py            # Run LLM analysis
│   ├── eval_fin_performance.py # Financial performance eval
│   └── eval_laaj.py           # LAAJ evaluation
├── data/                       # Data storage
│   ├── data/                  # Run-specific data
│   ├── logs/                  # LLM and system logs
│   └── runs/                  # Run metadata
├── docs/                       # Documentation
│   ├── motivation.md
│   ├── momentum_filtering_strategies.md
│   └── static_momentum_indicators.md
└── secrets/                    # API keys and credentials
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (for news sentiment analysis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/a-anurag1024/nifty_500_momentum.git
   cd nifty_500_momentum
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.in
   ```

3. **Set up environment variables**
   
   Create a `.env` file or set the LLM interactions environment variables:
   ```bash
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4.1-mini
   OPENAI_API_KEY=<your_api_key>
   LLM_LOG_DIR=data/logs/llm_logs.jsonl
   ```

### Basic Workflow

#### 1. Collect Stock Data
```bash
python scripts/nifty_500_collector.py
```
- Fetches historical price data for Nifty 500 stocks
- Configurable period (default: 2 years)
- Stores data in parquet format

#### 2. Apply Momentum Strategies
```bash
python scripts/shortlist.py
```
- Calculates momentum indicators
- Applies filtering strategies
- Generates shortlist of candidates
- Strategies: `EXPLOSIVE_BREAKOUT`, `GOLDEN_MOMENTUM`, `REVERSAL_HUNTER`, `TRENDSURFER`, `ANY`

#### 3. Collect News for Shortlisted Stocks
```bash
python scripts/news_collector.py
```
- Fetches recent news articles for shortlisted stocks
- Uses RSS feeds (Google News, etc.)
- Caches results to avoid redundant API calls

#### 4. Run LLM Analysis
```bash
python scripts/analysis.py
```
- Analyzes news sentiment using OpenAI
- Validates momentum signals with news catalysts
- Generates detailed reports

#### 5. Evaluate Performance
```bash
python scripts/eval_fin_performance.py
python scripts/eval_laaj.py
```
- Backtests strategy performance
- Generates evaluation reports

## ⚙️ Configuration

### Data Collection Settings

Edit the configuration in each script:

```python
# DataConfig options
DATA_CONFIG = DataConfig(
    data_dir="data",              # Base directory
    stock_api_sleep=5.0,          # API rate limiting
    news_api_sleep=5.0,
    cache_expiry_hours=24,        # News cache expiry
    stock_file_ext=".parquet",
    news_file_ext=".json"
)
```

### Strategy Selection

In `scripts/shortlist.py`:
```python
from nifty_500_momentum.static.shortlister import Strategies

STRATEGY = Strategies.EXPLOSIVE_BREAKOUT  # Or ANY, GOLDEN_MOMENTUM, etc.
```

### Run Management

Each run is identified by a `RUN_ID`:
```python
RUN_ID = "run_1"  # Change for different experiments
```

## 📈 Use Cases

1. **Momentum Screener**: Daily/weekly stock screening for breakout candidates
2. **News Validation**: Verify technical signals with fundamental catalysts
3. **Research Platform**: Analyze relationship between momentum and news sentiment
4. **Backtesting**: Test strategy performance across different market conditions
5. **Portfolio Construction**: Build momentum-based portfolios with catalyst backing

## 🔬 Indicators Used

### Trend Indicators
- **SMA** (Simple Moving Average): 50, 200-day
- **EMA** (Exponential Moving Average): Fast trend detection
- **ADX** (Average Directional Index): Trend strength

### Momentum Oscillators
- **RSI** (Relative Strength Index): Overbought/oversold conditions
- **MACD** (Moving Average Convergence Divergence): Trend changes
- **ROC** (Rate of Change): Pure price momentum

### Volume Indicators
- **Relative Volume (RVOL)**: Abnormal participation detection
- **Volume Profile**: Institutional activity confirmation

### Composite Metrics
- **12-Month Momentum**: Long-term persistence filter

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **[motivation.md](docs/motivation.md)**: Why momentum alone fails and how news helps
- **[momentum_filtering_strategies.md](docs/momentum_filtering_strategies.md)**: Detailed strategy explanations
- **[static_momentum_indicators.md](docs/static_momentum_indicators.md)**: Theory behind each indicator

## 🛠️ Development

### Module Installation (Editable Mode)
```bash
pip install -e modules/
```

### Project Structure
The core library is in `modules/src/nifty_500_momentum/`:
- Modify strategy logic in `static/`
- Extend LLM analysis in `analysts/`
- Add new data sources in `data/collectors/`

## 📊 Output Files

Results are stored in `data/data/<run_id>/`:

```
run_1/
├── tickers.json                    # All tickers
├── shortlist_*.json               # Strategy-specific shortlists
├── report_run_1_*.json            # Analysis reports
├── stocks/                        # Price data (parquet)
└── news/                          # News articles (JSON)
```

### Sample Run Results

See [sample analysis](sample_results/sample_run_analysis.md) for a sample run results including:
- [shortlist_any.json](sample_results/shortlist_any.json) - Technical Shortlist details
- [report_run_1_any.json](sample_results/report_run_1_any.json) - LLM analysis report
- [run_1_any_fin_performance_report.json](sample_results/run_1_any_fin_performance_report.json) - Financial performance evaluation
- [run_1_any_laaj_report.json](sample_results/run_1_any_laaj_report.json) - LAAJ (LLM as a Judge) evaluation results

## ⚠️ Limitations & Risks

1. **Market Risk**: Past momentum does not guarantee future performance
2. **Mid/Small Cap Volatility**: Higher risk due to liquidity constraints
3. **News Lag**: News may lag price action in fast-moving markets
4. **LLM Costs**: OpenAI API usage incurs costs
5. **Data Quality**: Depends on yfinance and RSS feed reliability

## 🤝 Contributing

This is a proof-of-concept project. Contributions, suggestions, and feedback are welcome!

## 📝 License

This project is for educational and research purposes.

## 👤 Author

**Aditya Anurag Dash**  
Email: a.anurag1024@gmail.com

## 🙏 Acknowledgments

- yfinance for stock data
- OpenAI for LLM capabilities
- feedparser for RSS feed parsing

---

**Disclaimer**: This project is for research and educational purposes only. Not financial advice. Always conduct your own research and consult with a financial advisor before making investment decisions.
