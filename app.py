import streamlit as st
import pandas as pd

# Streamlit requires set_page_config to be called before any other Streamlit commands
st.set_page_config(page_title="B2B Sales Pipeline Dashboard", layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("master_sales_pipeline.csv", parse_dates=['engage_date', 'close_date'])
    return df

df = load_data()

st.title("📊 B2B Sales Pipeline Dashboard")
st.caption("Fictitious computer hardware company – built by Amr 😎")

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

years = df['year'].dropna().unique()
years = sorted(years)

selected_year = st.sidebar.multiselect("Year", years, default=years)
selected_manager = st.sidebar.multiselect("Manager", df['manager'].unique())
selected_sector = st.sidebar.multiselect("Sector", df['sector'].dropna().unique())

# apply filters
filtered_df = df.copy()

if selected_year:
    filtered_df = filtered_df[filtered_df['year'].isin(selected_year)]

if selected_manager:
    filtered_df = filtered_df[filtered_df['manager'].isin(selected_manager)]

if selected_sector:
    filtered_df = filtered_df[filtered_df['sector'].isin(selected_sector)]

# ---------- TOP KPIs ----------
total_deals = len(filtered_df)
win_rate = filtered_df['win_flag'].mean()
total_won_revenue = filtered_df['won_revenue'].sum()
open_deals = (filtered_df['deal_stage'] == 'Open').sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deals", f"{total_deals}")
col2.metric("Win Rate", f"{win_rate:.0%}")
col3.metric("Won Revenue", f"${total_won_revenue:,.0f}")
col4.metric("Open Deals", f"{open_deals}")




st.markdown("---")
col1,col2=st.columns(2)
# ---------- TEAM PERFORMANCE ----------
with col1:
    st.subheader("👥 Team Performance (by Manager)")

    manager_stats = (
        filtered_df
        .groupby('manager')
        .agg(
            deals=('opportunity_id', 'count'),
            win_rate=('win_flag', 'mean'),
            revenue=('won_revenue', 'sum')
        )
        .sort_values('win_rate', ascending=False)
    )

    st.dataframe(manager_stats)
with col2:
    st.subheader("👥 Team Win Rate (Bar Chart)")

    manager_chart_data = manager_stats.reset_index()

    st.bar_chart(
        data=manager_chart_data,
        x="manager",
        y="win_rate",
    )

        
# ---------- PRODUCT PERFORMANCE ----------=========================
with col1:
    
    sector_stats = (
        filtered_df
        .groupby('sector')['win_flag']
        .mean()
        .sort_values(ascending=False)
    )

    st.subheader("🏭 Sector Win Rate")
    st.dataframe(sector_stats)

with col2:
#       # ---------- PRODUCT PERFORMANCE ----------
    st.subheader("🧩 Product Performance")

    product_stats = (
        filtered_df
        .groupby('product')
        .agg(
            deals=('opportunity_id', 'count'),
            win_rate=('win_flag', 'mean'),
            revenue=('won_revenue', 'sum')
        )
        .sort_values('win_rate', ascending=False)
    )

    st.dataframe(product_stats)     
 
col1,col2=st.columns(2)
# with col1:



quarterly = (
    filtered_df
    .groupby(['year', 'quarter'])['opportunity_id']
    .count()
    .reset_index()
    .sort_values(['year', 'quarter'])
)

quarterly['year_quarter'] = quarterly['year'].astype(str) + " Q" + quarterly['quarter'].astype(str)

st.subheader("📈 Quarterly Deal Volume")

st.line_chart(
    data=quarterly,
    x="year_quarter",
    y="opportunity_id",
)

        
# with col2:
#    # ---------- QUARTERLY TREND ----------
#     st.subheader("📈 Quarterly Deal Volume")

#     quarterly = (
#         filtered_df
#         .groupby(['year', 'quarter'])['opportunity_id']
#         .count()
#         .reset_index()
#         .sort_values(['year', 'quarter'])
#     )
#     st.line_chart(
#         data=quarterly,
#         x="quarter",
#         y="opportunity_id",
#     )
    

