"""
Executive Dashboard for Cookie Cats A/B Test Analysis
Mobile Game Player Retention & Experiment Analysis
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from utils import load_data, calculate_kpis, perform_ab_test

# Page configuration
st.set_page_config(
    page_title="Cookie Cats A/B Test Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_cached_data(file_path='cookie_cats.csv'):
    """Load and cache the dataset"""
    return load_data(file_path)


def main():
    # Header
    st.markdown('<p class="main-header">🎮 Cookie Cats A/B Test Dashboard</p>', unsafe_allow_html=True)
    st.markdown("**Mobile Game Player Retention & Experiment Analysis**")
    st.markdown("---")
    
    # Sidebar for file upload
    st.sidebar.header("📊 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Cookie Cats dataset (CSV)",
        type=['csv'],
        help="Upload the cookie_cats.csv file. If not provided, sample data will be used."
    )
    
    # Load data
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✅ Loaded {len(df):,} records")
    else:
        df = load_cached_data()
        st.sidebar.info("ℹ️ Using sample data. Upload CSV file to use your own dataset.")
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    ab_results = perform_ab_test(df)
    
    # ==================== KPI SECTION ====================
    st.markdown('<p class="section-header">📈 Key Performance Indicators (KPIs)</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Users",
            value=f"{kpis['total_users']:,}",
            help="Total number of players in the experiment"
        )
    
    with col2:
        st.metric(
            label="Daily Active Users (DAU)",
            value=f"{kpis['dau']:,}",
            help="Number of unique users who played the game"
        )
    
    with col3:
        st.metric(
            label="Day 1 Retention",
            value=f"{kpis['overall_d1_retention']:.1%}",
            help="Percentage of players who returned on day 1"
        )
    
    with col4:
        st.metric(
            label="Day 7 Retention",
            value=f"{kpis['overall_d7_retention']:.1%}",
            help="Percentage of players who returned on day 7"
        )
    
    # KPI Definitions
    with st.expander("📖 KPI Definitions", expanded=False):
        st.markdown("""
        **Daily Active Users (DAU):**
        - The number of unique users who engage with the game on a given day
        - Critical metric for measuring user engagement and game health
        
        **Retention Rates:**
        - **Day 1 Retention (D1):** Percentage of new players who return to the game one day after first install
          - Indicates initial game appeal and onboarding effectiveness
          - Industry benchmark: 40-50% for successful mobile games
        
        - **Day 7 Retention (D7):** Percentage of new players who return seven days after first install
          - Measures long-term engagement and game stickiness
          - Industry benchmark: 15-25% for successful mobile games
        
        **Why These Matter:**
        - Retention is a leading indicator of long-term revenue (LTV)
        - Higher retention = more opportunities for monetization
        - Retention improvements directly impact user lifetime value
        """)
    
    st.markdown("---")
    
    # ==================== A/B TEST ANALYSIS ====================
    st.markdown('<p class="section-header">🧪 A/B Test Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    **Experiment Overview:**
    - **Control Group (Gate 30):** Players encounter a gate at level 30
    - **Treatment Group (Gate 40):** Players encounter a gate at level 40
    - **Hypothesis:** Moving the gate from level 30 to 40 will improve player retention
    """)
    
    # Results summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Day 1 Retention Results")
        
        # Create comparison chart
        fig_d1 = go.Figure()
        
        fig_d1.add_trace(go.Bar(
            name='Gate 30',
            x=['Gate 30'],
            y=[ab_results['gate_30_d1_rate']],
            marker_color='#ff7f0e',
            text=[f"{ab_results['gate_30_d1_rate']:.1%}"],
            textposition='auto',
        ))
        
        fig_d1.add_trace(go.Bar(
            name='Gate 40',
            x=['Gate 40'],
            y=[ab_results['gate_40_d1_rate']],
            marker_color='#2ca02c',
            text=[f"{ab_results['gate_40_d1_rate']:.1%}"],
            textposition='auto',
        ))
        
        fig_d1.update_layout(
            title="Day 1 Retention by Group",
            yaxis_title="Retention Rate",
            yaxis=dict(tickformat='.1%'),
            height=400,
            showlegend=True,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_d1, use_container_width=True)
        
        # Statistical summary
        st.markdown(f"""
        **Results:**
        - Gate 30: **{ab_results['gate_30_d1_rate']:.2%}** ({ab_results['n_gate_30']:,} users)
        - Gate 40: **{ab_results['gate_40_d1_rate']:.2%}** ({ab_results['n_gate_40']:,} users)
        - **Difference:** {ab_results['d1_diff']:+.2%} ({ab_results['d1_lift']:+.1f}% lift)
        - **95% CI:** [{ab_results['d1_ci_lower']:.2%}, {ab_results['d1_ci_upper']:.2%}]
        - **P-value:** {ab_results['d1_p_value']:.4f}
        """)
        
        # Significance indicator
        if ab_results['d1_p_value'] < 0.05:
            st.success(f"✅ **Statistically Significant** (p < 0.05)")
        else:
            st.warning(f"⚠️ **Not Statistically Significant** (p ≥ 0.05)")
    
    with col2:
        st.subheader("📊 Day 7 Retention Results")
        
        # Create comparison chart
        fig_d7 = go.Figure()
        
        fig_d7.add_trace(go.Bar(
            name='Gate 30',
            x=['Gate 30'],
            y=[ab_results['gate_30_d7_rate']],
            marker_color='#ff7f0e',
            text=[f"{ab_results['gate_30_d7_rate']:.1%}"],
            textposition='auto',
        ))
        
        fig_d7.add_trace(go.Bar(
            name='Gate 40',
            x=['Gate 40'],
            y=[ab_results['gate_40_d7_rate']],
            marker_color='#2ca02c',
            text=[f"{ab_results['gate_40_d7_rate']:.1%}"],
            textposition='auto',
        ))
        
        fig_d7.update_layout(
            title="Day 7 Retention by Group",
            yaxis_title="Retention Rate",
            yaxis=dict(tickformat='.1%'),
            height=400,
            showlegend=True,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_d7, use_container_width=True)
        
        # Statistical summary
        st.markdown(f"""
        **Results:**
        - Gate 30: **{ab_results['gate_30_d7_rate']:.2%}** ({ab_results['n_gate_30']:,} users)
        - Gate 40: **{ab_results['gate_40_d7_rate']:.2%}** ({ab_results['n_gate_40']:,} users)
        - **Difference:** {ab_results['d7_diff']:+.2%} ({ab_results['d7_lift']:+.1f}% lift)
        - **95% CI:** [{ab_results['d7_ci_lower']:.2%}, {ab_results['d7_ci_upper']:.2%}]
        - **P-value:** {ab_results['d7_p_value']:.4f}
        """)
        
        # Significance indicator
        if ab_results['d7_p_value'] < 0.05:
            st.success(f"✅ **Statistically Significant** (p < 0.05)")
        else:
            st.warning(f"⚠️ **Not Statistically Significant** (p ≥ 0.05)")
    
    # Combined retention comparison
    st.subheader("📈 Retention Comparison: Gate 30 vs Gate 40")
    
    fig_combined = go.Figure()
    
    fig_combined.add_trace(go.Bar(
        name='Gate 30',
        x=['Day 1', 'Day 7'],
        y=[ab_results['gate_30_d1_rate'], ab_results['gate_30_d7_rate']],
        marker_color='#ff7f0e',
        text=[f"{ab_results['gate_30_d1_rate']:.1%}", f"{ab_results['gate_30_d7_rate']:.1%}"],
        textposition='auto',
    ))
    
    fig_combined.add_trace(go.Bar(
        name='Gate 40',
        x=['Day 1', 'Day 7'],
        y=[ab_results['gate_40_d1_rate'], ab_results['gate_40_d7_rate']],
        marker_color='#2ca02c',
        text=[f"{ab_results['gate_40_d1_rate']:.1%}", f"{ab_results['gate_40_d7_rate']:.1%}"],
        textposition='auto',
    ))
    
    fig_combined.update_layout(
        title="Retention Rates: Gate 30 vs Gate 40",
        yaxis_title="Retention Rate",
        yaxis=dict(tickformat='.1%'),
        height=450,
        barmode='group',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== EXECUTIVE SUMMARY ====================
    st.markdown('<p class="section-header">💼 Executive Summary</p>', unsafe_allow_html=True)
    
    # Determine recommendation
    d1_significant = ab_results['d1_p_value'] < 0.05
    d7_significant = ab_results['d7_p_value'] < 0.05
    d1_positive = ab_results['d1_diff'] > 0
    d7_positive = ab_results['d7_diff'] > 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Key Findings")
        
        findings = []
        
        if d1_significant and d1_positive:
            findings.append(f"✅ **Day 1 Retention:** Gate 40 shows a statistically significant improvement of {ab_results['d1_lift']:.1f}% over Gate 30")
        elif d1_significant and not d1_positive:
            findings.append(f"❌ **Day 1 Retention:** Gate 40 shows a statistically significant decrease of {abs(ab_results['d1_lift']):.1f}% compared to Gate 30")
        else:
            findings.append(f"➡️ **Day 1 Retention:** No statistically significant difference between groups")
        
        if d7_significant and d7_positive:
            findings.append(f"✅ **Day 7 Retention:** Gate 40 shows a statistically significant improvement of {ab_results['d7_lift']:.1f}% over Gate 30")
        elif d7_significant and not d7_positive:
            findings.append(f"❌ **Day 7 Retention:** Gate 40 shows a statistically significant decrease of {abs(ab_results['d7_lift']):.1f}% compared to Gate 30")
        else:
            findings.append(f"➡️ **Day 7 Retention:** No statistically significant difference between groups")
        
        for finding in findings:
            st.markdown(f"- {finding}")
        
        st.markdown("### Business Impact")
        
        # Calculate potential impact
        if d7_significant and d7_positive:
            additional_retained = ab_results['d7_diff'] * ab_results['n_gate_40']
            st.markdown(f"""
            - Moving the gate to level 40 could retain an additional **{additional_retained:,.0f} players** per cohort
            - This represents a **{ab_results['d7_lift']:.1f}% improvement** in long-term engagement
            - Higher retention typically leads to increased lifetime value (LTV) and revenue
            """)
        elif d7_significant and not d7_positive:
            st.markdown(f"""
            - Moving the gate to level 40 would result in **fewer retained players**
            - This could negatively impact long-term revenue and user lifetime value
            """)
        else:
            st.markdown("""
            - The experiment shows no clear winner
            - Consider running a longer experiment or testing alternative hypotheses
            """)
    
    with col2:
        st.markdown("### Recommendation")
        
        if d7_significant and d7_positive:
            st.success("""
            **✅ RECOMMEND:**
            Roll out Gate 40 to all players
            """)
        elif d7_significant and not d7_positive:
            st.error("""
            **❌ DO NOT ROLL OUT:**
            Keep Gate 30
            """)
        else:
            st.info("""
            **⚠️ INCONCLUSIVE:**
            Continue testing or explore alternatives
            """)
    
    st.markdown("---")
    
    # ==================== DATA EXPLORATION ====================
    with st.expander("🔍 Data Exploration", expanded=False):
        st.subheader("Dataset Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Summary**")
            st.dataframe(df.describe(), use_container_width=True)
        
        with col2:
            st.markdown("**Group Distribution**")
            group_counts = df['version'].value_counts()
            fig_dist = px.pie(
                values=group_counts.values,
                names=group_counts.index,
                title="User Distribution by Group"
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        st.markdown("**Sample Data**")
        st.dataframe(df.head(100), use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Dataset",
            data=csv,
            file_name="cookie_cats_data.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()

