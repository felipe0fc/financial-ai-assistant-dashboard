# 🏦 Annimati Financial Dashboard

**Integrated Financial Analysis System with AI Assistant**

A comprehensive financial dashboard system that combines data extraction, visualization, and AI-powered analysis for REXP and DIPD companies. Built with Python, Plotly Dash, and Anthropic's Claude AI.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Dashboard](https://img.shields.io/badge/dashboard-Plotly%20Dash-brightgreen.svg)](https://plotly.com/dash/)
[![AI](https://img.shields.io/badge/AI-Anthropic%20Claude-orange.svg)](https://anthropic.com)

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Pipeline](#-data-pipeline)
- [AI Assistant](#-ai-assistant)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 **Core Capabilities**
- **📊 Interactive Dashboard**: Real-time financial data visualization
- **🤖 AI Financial Assistant**: Natural language queries with context-aware responses
- **📈 Comparative Analysis**: Side-by-side performance comparison between REXP and DIPD
- **🔄 Automated Data Extraction**: PDF parsing and data processing pipeline
- **💡 Smart Insights**: Trend identification and pattern analysis

### 🖥️ **Interface Modes**
- **Web Dashboard**: Modern, responsive web interface with interactive charts
- **CLI Assistant**: Terminal-based AI assistant for quick queries
- **Dual Layout**: Side-by-side dashboard and chat integration

### 📈 **Financial Metrics**
- Revenue trends and growth analysis
- Profitability margins (Gross, Operating, Net)
- Cost structure analysis
- Quarterly and annual performance tracking
- Historical trend comparison

## 🏗️ Project Structure

```
ANNIMATI/
├── app.py                        # Main application entry point
├── setup.py                      # Installation script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .env (create this)            # Environment variables 
│
├── data/
│   ├── processed/
│   │   └── financial_data.csv     # Processed financial data
│   └── raw/
│       ├── REXP/                  # REXP PDF files
│       └── DIPD/                  # DIPD PDF files
│
├── src/
│   ├── extraction/
│   │   ├── pipeline.py            # Data extraction pipeline
│   │   └── constants.py           # Extraction constants
│   │
│   └── chat/
│       └── integrated_dash.py     # Dashboard and AI system
│
└── venv/                          # Virtual environment
```

## 🚀 Installation

### Prerequisites
- **Python 3.8+** installed on your system
- **Anthropic API Key** for AI functionality
- **Raw financial data** (PDF files) in appropriate directories

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/your-username/annimati
cd annimati

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Option 1: Using pip
pip install -r requirements.txt

# Option 2: Using setup.py
pip install -e .

# Option 3: Install specific extras
pip install -e .[dev]  # Include development tools
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Required: Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Custom configurations
DATA_PATH=./data/processed/financial_data.csv
MAX_CONTEXT_ROWS=30
DEBUG_MODE=False
```

### API Key Setup
1. **Get Anthropic API Key**:
   - Visit [Anthropic Console](https://console.anthropic.com)
   - Create account and generate API key
   - Add credits to your account
   - Input your API KEY to .env file

## 📱 Usage

### Quick Start
```bash
# Launch application (web dashboard by default)
python app.py

# Launch CLI assistant
python app.py --cli

# Launch web dashboard explicitly
python app.py --web

# Force data re-extraction
python app.py --force
```

### First Run Workflow
1. **Data Validation**: App checks for existing processed data
2. **Pipeline Execution**: Prompts to run extraction if needed
3. **Structure Validation**: Verifies data integrity
4. **Application Launch**: Starts chosen interface mode

### Web Dashboard
```bash
python app.py --web
```
- **URL**: http://localhost:8050
- **Features**: Interactive charts, AI chat, real-time filtering
- **Controls**: Company selector, metric chooser, time range filters

### CLI Assistant
```bash
python app.py --cli
```
- **Interface**: Terminal-based interaction
- **Features**: Natural language queries, quick insights
- **Commands**: Type questions, 'help' for examples, 'quit' to exit

## 🔄 Data Pipeline

### Extraction Process
1. **PDF Reading**: Extracts P&L statements from quarterly reports
2. **Data Parsing**: Uses LLM to structure financial data
3. **Validation**: Ensures data consistency and completeness
4. **Processing**: Calculates additional metrics and ratios
5. **Export**: Saves to CSV for dashboard consumption

### Supported File Formats
- **Input**: PDF quarterly reports (P&L statements)
- **Output**: CSV with standardized financial metrics
- **Companies**: REXP and DIPD

### Data Schema
```csv
Simbol,file_name,Revenue,Cost of Goods Sold (COGS),Gross Profit,Operating Expenses,Operating Income,Net Income,Report Date
REXP,31032022.pdf,50000000,30000000,20000000,15000000,5000000,4000000,2022-03-31
```

## 🤖 AI Assistant

### Natural Language Queries
The AI assistant supports various types of financial questions:

#### **Trend Analysis**
```
"What is the revenue trend for REXP over the last 4 quarters?"
"Show me the profitability evolution for both companies"
"Identify seasonal patterns in the financial data"
```

#### **Comparative Analysis**
```
"Compare the performance between REXP and DIPD"
"Which company has better profit margins?"
"Analyze cost structure differences between the companies"
```

#### **Financial Calculations**
```
"Calculate the revenue growth rate for DIPD year-over-year"
"What was the highest revenue quarter for each company?"
"Show me the operating margin trends"
```

#### **Risk Assessment**
```
"What are the key financial risks I should be aware of?"
"Which company is more financially stable?"
"Identify any anomalies in the financial data"
```

### Context Window Management
- **Smart Sampling**: Balances recent and historical data
- **Token Optimization**: Efficient use of LLM context limits
- **Data Prioritization**: Focuses on most relevant financial metrics

## 📊 API Reference

### Core Classes

#### `LLMExtractionPipeline`
```python
from src.extraction.pipeline import LLMExtractionPipeline

pipeline = LLMExtractionPipeline(data_path="./data/raw/")
pipeline.run()  # Extract and process data
```

#### `IntegratedFinancialDashboard`
```python
from src.chat.integrated_dash import IntegratedFinancialDashboard

dashboard = IntegratedFinancialDashboard(
    data_path="./data/processed/financial_data.csv",
    max_context_rows=30
)
dashboard.run_dashboard(port=8050)
```

#### `StandaloneQuerySystem`
```python
from src.chat.integrated_dash import StandaloneQuerySystem

cli_system = StandaloneQuerySystem(
    data_path="./data/processed/financial_data.csv"
)
cli_system.run_cli_session()
```

### Configuration Options
```python
# Dashboard customization
dashboard = IntegratedFinancialDashboard(
    data_path="custom_path.csv",        # Data file location
    max_context_rows=50,                # AI context size
)

# Launch options
dashboard.run_dashboard(
    debug=True,                         # Enable debug mode
    port=8080,                          # Custom port
)
```

## 🎯 Examples

### Example 1: Basic Usage
```bash
# 1. Setup project
python app.py

# 2. When prompted, choose Y to extract data
# 3. Web dashboard opens at localhost:8050
# 4. Ask: "Compare revenue trends between REXP and DIPD"
```

### Example 2: CLI Workflow
```bash
# Launch CLI mode
python app.py --cli

# Sample interaction:
> What is the revenue trend for both companies?

AI: Based on the financial data, here's the revenue analysis:

**REXP Revenue Trend:**
- Highly volatile with peaks reaching R$80M in Q1 2023
- Recent decline to R$22M in Q4 2024
- Shows cyclical patterns with significant fluctuations

**DIPD Revenue Trend:**
- More stable performance, ranging R$5M - R$73M
- Consistent growth trajectory with fewer volatility spikes
- Better predictability for forecasting

**Key Insight:** DIPD demonstrates more sustainable revenue patterns...
```

### Example 3: Dashboard Features
1. **Select Companies**: Choose REXP, DIPD, or both
2. **Choose Metrics**: Revenue, Gross Profit, Operating Income, Net Income
3. **Interactive Charts**: Hover for details, zoom, pan
4. **AI Chat**: Ask questions in natural language
5. **Real-time Updates**: Charts update based on selections

## 🔧 Troubleshooting

### Common Issues

#### **Import Errors**
```bash
# Error: Module not found
# Solution: Ensure all dependencies installed
pip install -r requirements.txt

# Error: anthropic module not found
# Solution: Install anthropic package
pip install anthropic>=0.3.0
```

#### **API Key Issues**
```bash
# Error: Invalid API key
# Solution: Check .env file and API key validity
cat .env  # Verify ANTHROPIC_API_KEY exists
```

#### **Data Extraction Failures**
```bash
# Error: PDF parsing failed
# Solution: Verify PDF files exist and are readable
ls data/raw/REXP/  # Check REXP files
ls data/raw/DIPD/  # Check DIPD files

# Error: Pipeline execution failed
# Solution: Run pipeline manually for debugging
python src/extraction/pipeline.py
```

#### **Dashboard Issues**
```bash
# Error: Port already in use
# Solution: Use different port
python app.py --web  # Will prompt for different port

# Error: Charts not loading
# Solution: Clear browser cache or try incognito mode
```

### Performance Optimization

#### **Large Datasets**
```python
# Reduce context window for better performance
dashboard = IntegratedFinancialDashboard(max_context_rows=20)
```

#### **Memory Usage**
```bash
# Monitor memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

### Debug Mode
```bash
# Enable debug logging
DEBUG_MODE=True python app.py --web
```

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -e .[dev]
```

### Code Style
- **Type Hints**: Required for public functions
- **Docstrings**: Google-style documentation

### Pull Request Process
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🐛 Bug Reports

When reporting bugs, please include:
- **Python version** (`python --version`)
- **Operating system** and version
- **Complete error traceback**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude AI capabilities
- **Plotly** for interactive visualization framework
- **Dash** for web application framework
- **PDFplumber** for PDF parsing functionality

## 📞 Support

- **Documentation**: Check this README and inline docstrings
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support

---

**Built with ❤️ and 🧠 by Felipe Ferreira de Carvalho**

*Transforming financial data into actionable insights through AI-powered analysis*