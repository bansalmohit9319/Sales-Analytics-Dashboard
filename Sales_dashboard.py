# =========================================================
# SALES DATA ANALYTICS DASHBOARD (INDUSTRY LEVEL)
# =========================================================

# INSTALL THESE LIBRARIES:
# pip install streamlit pandas plotly

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analytics Dashboard")


# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Sales CSV File",
    type=["csv"]
)


# =========================================================
# IF FILE UPLOADED
# =========================================================

if uploaded_file is not None:

    # =====================================================
    # READ CSV
    # =====================================================

    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Raw Dataset")

    st.dataframe(df)


    # =====================================================
    # DATA CLEANING
    # =====================================================

    df.drop_duplicates(inplace=True)

    df.fillna(0, inplace=True)


    # =====================================================
    # SIDEBAR FILTERS
    # =====================================================

    st.sidebar.header("🔍 Filters")

    # Region Filter
    region = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    # Category Filter
    category = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Region"].isin(region)) &
        (df["Category"].isin(category))
    ]


    # =====================================================
    # KPI SECTION
    # =====================================================

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["Profit"].sum()

    total_orders = filtered_df["Order ID"].nunique()

    average_sales = filtered_df["Sales"].mean()


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.2f}"
    )

    col2.metric(
        "📈 Total Profit",
        f"₹{total_profit:,.2f}"
    )

    col3.metric(
        "🛒 Total Orders",
        total_orders
    )

    col4.metric(
        "📊 Average Sales",
        f"₹{average_sales:,.2f}"
    )


    # =====================================================
    # SALES BY REGION
    # =====================================================

    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


    # =====================================================
    # SALES BY CATEGORY
    # =====================================================

    st.subheader("📦 Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Category Wise Sales"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


    # =====================================================
    # MONTHLY SALES TREND
    # =====================================================

    st.subheader("📅 Monthly Sales Trend")

    filtered_df["Order Date"] = pd.to_datetime(
        filtered_df["Order Date"]
    )

    filtered_df["Month"] = (
        filtered_df["Order Date"]
        .dt.strftime("%Y-%m")
    )

    monthly_sales = (
        filtered_df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


    # =====================================================
    # TOP PRODUCTS
    # =====================================================

    st.subheader("🏆 Top Selling Products")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="Product Name",
        y="Sales",
        title="Top 10 Products"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


    # =====================================================
    # PROFIT ANALYSIS
    # =====================================================

    st.subheader("💹 Profit Analysis")

    fig_profit = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Profit",
        hover_data=["Product Name"],
        title="Sales vs Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


    # =====================================================
    # DOWNLOAD FILTERED DATA
    # =====================================================

    st.subheader("⬇ Download Filtered Data")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )


    # =====================================================
    # SHOW FILTERED DATA
    # =====================================================

    st.subheader("📑 Filtered Dataset")

    st.dataframe(filtered_df)


# =========================================================
# IF NO FILE UPLOADED
# =========================================================

else:

    st.info("📂 Please Upload a CSV File")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.write(
    "Built with Python + Pandas + Plotly + Streamlit"
)