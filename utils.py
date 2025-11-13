"""
Utility functions for data loading and processing
"""
import pandas as pd
import numpy as np
from scipy import stats


def load_data(file_path='cookie_cats.csv'):
    """
    Load the Cookie Cats A/B testing dataset.
    
    Expected columns:
    - userid: unique player identifier
    - version: A/B test group (gate_30 or gate_40)
    - retention_1: Day 1 retention (0 or 1)
    - retention_7: Day 7 retention (0 or 1)
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with the loaded data
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # Generate sample data if file doesn't exist
        print(f"File {file_path} not found. Generating sample data...")
        return generate_sample_data()


def generate_sample_data(n_users=90189):
    """
    Generate sample Cookie Cats A/B testing data.
    This is a fallback if the actual dataset is not available.
    
    Args:
        n_users: Number of users to generate
        
    Returns:
        DataFrame with sample data
    """
    np.random.seed(42)
    
    # Split users between gate_30 and gate_40
    n_gate_30 = n_users // 2
    n_gate_40 = n_users - n_gate_30
    
    # Generate data for gate_30 group
    # Based on typical Cookie Cats results: ~44% D1 retention, ~19% D7 retention
    gate_30_d1 = np.random.binomial(1, 0.44, n_gate_30)
    gate_30_d7 = np.random.binomial(1, 0.19, n_gate_30)
    
    # Generate data for gate_40 group
    # Slightly higher retention: ~47% D1 retention, ~20% D7 retention
    gate_40_d1 = np.random.binomial(1, 0.47, n_gate_40)
    gate_40_d7 = np.random.binomial(1, 0.20, n_gate_40)
    
    # Combine data
    data = {
        'userid': range(1, n_users + 1),
        'version': ['gate_30'] * n_gate_30 + ['gate_40'] * n_gate_40,
        'retention_1': np.concatenate([gate_30_d1, gate_40_d1]),
        'retention_7': np.concatenate([gate_30_d7, gate_40_d7])
    }
    
    df = pd.DataFrame(data)
    return df


def calculate_kpis(df):
    """
    Calculate key performance indicators from the dataset.
    
    Args:
        df: DataFrame with user data
        
    Returns:
        Dictionary with KPI metrics
    """
    total_users = len(df)
    
    # Calculate DAU (assuming each user is a daily active user)
    dau = total_users
    
    # Calculate retention rates
    d1_retention = df['retention_1'].mean()
    d7_retention = df['retention_7'].mean()
    
    # Calculate retention by version
    retention_by_version = df.groupby('version').agg({
        'retention_1': 'mean',
        'retention_7': 'mean',
        'userid': 'count'
    }).rename(columns={'userid': 'total_users'})
    
    return {
        'total_users': total_users,
        'dau': dau,
        'overall_d1_retention': d1_retention,
        'overall_d7_retention': d7_retention,
        'retention_by_version': retention_by_version
    }


def perform_ab_test(df):
    """
    Perform statistical analysis of A/B test results.
    
    Args:
        df: DataFrame with user data
        
    Returns:
        Dictionary with A/B test results and statistics
    """
    # Split data by version
    gate_30 = df[df['version'] == 'gate_30']
    gate_40 = df[df['version'] == 'gate_40']
    
    # Calculate retention rates for each group
    gate_30_d1_rate = gate_30['retention_1'].mean()
    gate_30_d7_rate = gate_30['retention_7'].mean()
    gate_40_d1_rate = gate_40['retention_1'].mean()
    gate_40_d7_rate = gate_40['retention_7'].mean()
    
    # Calculate absolute differences
    d1_diff = gate_40_d1_rate - gate_30_d1_rate
    d7_diff = gate_40_d7_rate - gate_30_d7_rate
    
    # Calculate relative differences (lift)
    d1_lift = (d1_diff / gate_30_d1_rate) * 100 if gate_30_d1_rate > 0 else 0
    d7_lift = (d7_diff / gate_30_d7_rate) * 100 if gate_30_d7_rate > 0 else 0
    
    # Perform chi-square tests for statistical significance
    # D1 retention test
    d1_contingency = pd.crosstab(df['version'], df['retention_1'])
    chi2_d1, p_value_d1 = stats.chi2_contingency(d1_contingency)[:2]
    
    # D7 retention test
    d7_contingency = pd.crosstab(df['version'], df['retention_7'])
    chi2_d7, p_value_d7 = stats.chi2_contingency(d7_contingency)[:2]
    
    # Calculate confidence intervals for difference (using normal approximation)
    n_30 = len(gate_30)
    n_40 = len(gate_40)
    
    # D1 confidence interval
    se_d1 = np.sqrt(
        (gate_30_d1_rate * (1 - gate_30_d1_rate) / n_30) +
        (gate_40_d1_rate * (1 - gate_40_d1_rate) / n_40)
    )
    ci_d1_lower = d1_diff - 1.96 * se_d1
    ci_d1_upper = d1_diff + 1.96 * se_d1
    
    # D7 confidence interval
    se_d7 = np.sqrt(
        (gate_30_d7_rate * (1 - gate_30_d7_rate) / n_30) +
        (gate_40_d7_rate * (1 - gate_40_d7_rate) / n_40)
    )
    ci_d7_lower = d7_diff - 1.96 * se_d7
    ci_d7_upper = d7_diff + 1.96 * se_d7
    
    return {
        'gate_30_d1_rate': gate_30_d1_rate,
        'gate_30_d7_rate': gate_30_d7_rate,
        'gate_40_d1_rate': gate_40_d1_rate,
        'gate_40_d7_rate': gate_40_d7_rate,
        'd1_diff': d1_diff,
        'd7_diff': d7_diff,
        'd1_lift': d1_lift,
        'd7_lift': d7_lift,
        'd1_p_value': p_value_d1,
        'd7_p_value': p_value_d7,
        'd1_ci_lower': ci_d1_lower,
        'd1_ci_upper': ci_d1_upper,
        'd7_ci_lower': ci_d7_lower,
        'd7_ci_upper': ci_d7_upper,
        'n_gate_30': n_30,
        'n_gate_40': n_40
    }

