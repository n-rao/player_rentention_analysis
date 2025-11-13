# Cookie Cats A/B Test Dashboard

An executive-friendly interactive dashboard for analyzing mobile game player retention and A/B test experiments.

## Overview

This project demonstrates:
- **KPI Definition**: Daily Active Users (DAU) and retention metrics (D1, D7)
- **A/B Test Analysis**: Statistical analysis of experiment results with significance testing
- **Executive Dashboard**: One-page interactive dashboard built with Streamlit

## Dataset

The dashboard uses the **Cookie Cats** mobile game A/B testing dataset, which contains:
- Player assignments to two game versions (gate at level 30 vs. level 40)
- Day 1 retention (D1) and Day 7 retention (D7) metrics
- User identifiers

### Getting the Dataset

1. Download from Kaggle: [Cookie Cats Dataset](https://www.kaggle.com/datasets/yufengsui/mobile-game-ab-testing-cookie-cats)
2. Place the CSV file in the project directory as `cookie_cats.csv`
3. Or use the sample data generator (automatically used if file not found)

**Expected CSV format:**
```csv
userid,version,retention_1,retention_7
1,gate_30,1,0
2,gate_40,1,1
...
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd player_retention
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard:**
   - The dashboard will open automatically in your browser
   - Default URL: `http://localhost:8501`

3. **Upload your data (optional):**
   - Use the sidebar to upload your own CSV file
   - If no file is uploaded, sample data will be generated automatically

## Dashboard Features

### 📈 Key Performance Indicators (KPIs)
- **Total Users**: Total number of players in the experiment
- **Daily Active Users (DAU)**: Number of unique users
- **Day 1 Retention**: Percentage of players returning after 1 day
- **Day 7 Retention**: Percentage of players returning after 7 days

### 🧪 A/B Test Analysis
- **Visual Comparisons**: Side-by-side bar charts for retention rates
- **Statistical Testing**: Chi-square tests for significance
- **Confidence Intervals**: 95% confidence intervals for differences
- **P-values**: Statistical significance indicators

### 💼 Executive Summary
- **Key Findings**: Summary of significant results
- **Business Impact**: Potential impact on player retention
- **Recommendations**: Data-driven recommendations for rollout

### 🔍 Data Exploration
- Dataset summary statistics
- Group distribution visualization
- Sample data preview
- Data download functionality

## Project Structure

```
player_retention/
├── dashboard.py          # Main Streamlit dashboard
├── utils.py              # Data loading and analysis functions
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── cookie_cats.csv      # Dataset (optional, can be uploaded)
```

## Key Metrics Explained

### Daily Active Users (DAU)
The number of unique users who engage with the game on a given day. This is a critical metric for measuring user engagement and game health.

### Retention Rates

**Day 1 Retention (D1):**
- Percentage of new players who return to the game one day after first install
- Indicates initial game appeal and onboarding effectiveness
- Industry benchmark: 40-50% for successful mobile games

**Day 7 Retention (D7):**
- Percentage of new players who return seven days after first install
- Measures long-term engagement and game stickiness
- Industry benchmark: 15-25% for successful mobile games

### Why Retention Matters
- Retention is a leading indicator of long-term revenue (LTV)
- Higher retention = more opportunities for monetization
- Retention improvements directly impact user lifetime value

## Statistical Analysis

The dashboard performs:
- **Chi-square tests** to determine statistical significance
- **Confidence intervals** (95%) for retention rate differences
- **Lift calculations** to show relative improvements

Results are considered statistically significant if p-value < 0.05.

## Technologies Used

- **Streamlit**: Interactive dashboard framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **SciPy**: Statistical testing
- **NumPy**: Numerical computations

## License

This project is for demonstration purposes. The Cookie Cats dataset is available on Kaggle.

## Author

Created as a demonstration of KPI definition, A/B test analysis, and executive dashboard creation for mobile game analytics.

# player_rentention_analysis
