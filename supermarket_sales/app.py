# -*- coding: utf-8 -*-
"""
app.py  –  Supermarket Sales Analytics · Streamlit Dashboard
=============================================================
Run with:
    streamlit run supermarket_sales/app.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# PALETTE
# ──────────────────────────────────────────────
PALETTE = ["#3b82d4", "#7c5cd8", "#10b981", "#f59e0b", "#ef4444", "#6366f1"]

# ──────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "supermarket_sales.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    df["Date"]    = pd.to_datetime(df["Date"])
    df["Sales"]   = (df["Quantity"] * df["Unit price"]).round(2)
    df["Month"]   = df["Date"].dt.month_name()
    df["Weekday"] = df["Date"].dt.day_name()
    return df

df_full = load_data()

MONTH_ORDER   = ["January", "February", "March"]
WEEKDAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

BRANCH_CITY = {"A": "Yangon", "B": "Naypyitaw", "C": "Mandalay"}

# ──────────────────────────────────────────────
# SIDEBAR  –  FILTERS
# ──────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/shopping-cart.png",
        width=56,
    )
    st.title("Supermarket Sales")
    st.caption("Analytics Dashboard")
    st.divider()

    st.subheader("🔽 Filters")

    branch_options = sorted(df_full["Branch"].unique())
    sel_branches = st.multiselect(
        "Branch",
        options=branch_options,
        default=branch_options,
        format_func=lambda b: f"Branch {b} – {BRANCH_CITY[b]}",
    )

    payment_options = sorted(df_full["Payment"].unique())
    sel_payments = st.multiselect(
        "Payment Method",
        options=payment_options,
        default=payment_options,
    )

    cust_options = sorted(df_full["Customer type"].unique())
    sel_custs = st.multiselect(
        "Customer Type",
        options=cust_options,
        default=cust_options,
    )

    gender_options = sorted(df_full["Gender"].unique())
    sel_genders = st.multiselect(
        "Gender",
        options=gender_options,
        default=gender_options,
    )

    product_options = sorted(df_full["Product line"].unique())
    sel_products = st.multiselect(
        "Product Line",
        options=product_options,
        default=product_options,
    )

    st.divider()
    st.caption("500 synthetic transactions · Jan – Mar 2019")

# ──────────────────────────────────────────────
# APPLY FILTERS
# ──────────────────────────────────────────────
df = df_full[
    df_full["Branch"].isin(sel_branches) &
    df_full["Payment"].isin(sel_payments) &
    df_full["Customer type"].isin(sel_custs) &
    df_full["Gender"].isin(sel_genders) &
    df_full["Product line"].isin(sel_products)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("## 🛒 Supermarket Sales Analytics")
st.markdown(
    f"Showing **{len(df):,}** of {len(df_full):,} transactions · "
    f"Branches: **{', '.join(sel_branches)}** · "
    f"Payment: **{', '.join(sel_payments)}**"
)
st.divider()

# ──────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

total_sales  = df["Sales"].sum()
total_txns   = len(df)
avg_sale     = df["Sales"].mean()
avg_rating   = df["Rating"].mean()
top_branch   = df.groupby("Branch")["Sales"].sum().idxmax()
top_product  = df.groupby("Product line")["Sales"].sum().idxmax()

k1.metric("💰 Total Sales",       f"₹{total_sales:,.0f}")
k2.metric("🧾 Transactions",      f"{total_txns:,}")
k3.metric("📊 Avg Sale",          f"₹{avg_sale:,.2f}")
k4.metric("⭐ Avg Rating",        f"{avg_rating:.2f} / 10")
k5.metric("🏆 Top Branch",        f"Branch {top_branch}")
k6.metric("🥇 Top Product Line",  top_product)

st.divider()

# ──────────────────────────────────────────────
# ROW 1:  Branch Sales  |  Product Line Sales
# ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    branch_sales = (
        df.groupby("Branch")["Sales"].sum().reset_index()
           .sort_values("Sales", ascending=False)
    )
    branch_sales["Label"] = branch_sales["Branch"].map(
        lambda b: f"Branch {b} ({BRANCH_CITY[b]})"
    )
    fig = px.bar(
        branch_sales, x="Label", y="Sales",
        color="Label", color_discrete_sequence=PALETTE,
        text_auto=",.0f",
        title="💼 Total Sales by Branch",
        labels={"Label": "Branch", "Sales": "Sales (₹)"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_tickprefix="₹", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    prod_sales = (
        df.groupby("Product line")["Sales"].sum().reset_index()
           .sort_values("Sales")
    )
    fig = px.bar(
        prod_sales, x="Sales", y="Product line",
        orientation="h", color="Product line",
        color_discrete_sequence=PALETTE,
        text_auto=",.0f",
        title="📦 Sales by Product Line",
        labels={"Product line": "", "Sales": "Sales (₹)"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_tickprefix="₹", xaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# ROW 2:  Monthly Trend  |  Payment Pie
# ──────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    monthly = (
        df.groupby("Month")["Sales"].sum()
          .reindex([m for m in MONTH_ORDER if m in df["Month"].unique()])
          .reset_index()
    )
    fig = px.line(
        monthly, x="Month", y="Sales",
        markers=True,
        title="📈 Monthly Sales Trend",
        labels={"Sales": "Sales (₹)", "Month": ""},
        color_discrete_sequence=[PALETTE[0]],
        text="Sales",
    )
    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="top center",
        line_width=2.5,
        marker_size=9,
    )
    fig.update_layout(yaxis_tickprefix="₹", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    pay_count = df.groupby("Payment")["Invoice ID"].count().reset_index()
    pay_count.columns = ["Payment", "Count"]
    fig = px.pie(
        pay_count, names="Payment", values="Count",
        color_discrete_sequence=PALETTE,
        title="💳 Payment Method Distribution",
        hole=0.35,
    )
    fig.update_traces(textinfo="label+percent", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# ROW 3:  Avg Rating by Product  |  Sales by Cust Type & Gender
# ──────────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    avg_rat = (
        df.groupby("Product line")["Rating"].mean().reset_index()
          .sort_values("Rating", ascending=False)
    )
    avg_rat["Rating"] = avg_rat["Rating"].round(2)
    fig = px.bar(
        avg_rat, x="Product line", y="Rating",
        color="Product line", color_discrete_sequence=PALETTE,
        text="Rating",
        title="⭐ Avg Customer Rating by Product Line",
        labels={"Product line": "", "Rating": "Avg Rating (1–10)"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 11])
    st.plotly_chart(fig, use_container_width=True)

with col6:
    cg = (
        df.groupby(["Customer type", "Gender"])["Sales"].sum().reset_index()
    )
    fig = px.bar(
        cg, x="Customer type", y="Sales", color="Gender",
        barmode="group",
        color_discrete_sequence=PALETTE[:2],
        text_auto=",.0f",
        title="👥 Sales by Customer Type & Gender",
        labels={"Customer type": "", "Sales": "Sales (₹)"},
    )
    fig.update_layout(yaxis_tickprefix="₹", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# ROW 4:  Heatmap (full width)
# ──────────────────────────────────────────────
st.markdown("#### 🔥 Sales Heatmap — Branch × Product Line")
heat = (
    df.groupby(["Branch", "Product line"])["Sales"]
      .sum().unstack("Product line").fillna(0).round(0)
)
fig = px.imshow(
    heat,
    text_auto=",.0f",
    color_continuous_scale="Blues",
    title="",
    labels={"color": "Sales (₹)"},
    aspect="auto",
)
fig.update_xaxes(tickangle=-25)
st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# ROW 5:  Rating Boxplot  |  Weekday Avg Sale
# ──────────────────────────────────────────────
col7, col8 = st.columns(2)

with col7:
    fig = px.box(
        df, x="Branch", y="Rating",
        color="Branch", color_discrete_sequence=PALETTE,
        title="📊 Rating Distribution by Branch",
        labels={"Rating": "Rating (1–10)", "Branch": ""},
        points="outliers",
    )
    fig.update_layout(showlegend=False, yaxis_range=[0, 11])
    st.plotly_chart(fig, use_container_width=True)

with col8:
    weekday_avg = (
        df.groupby("Weekday")["Sales"].mean()
          .reindex([w for w in WEEKDAY_ORDER if w in df["Weekday"].unique()])
          .reset_index()
    )
    weekday_avg["Sales"] = weekday_avg["Sales"].round(2)
    fig = px.bar(
        weekday_avg, x="Weekday", y="Sales",
        color_discrete_sequence=[PALETTE[4]],
        text="Sales",
        title="📅 Avg Sale per Transaction by Weekday",
        labels={"Sales": "Avg Sales (₹)", "Weekday": ""},
    )
    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig.update_layout(yaxis_tickprefix="₹", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# ROW 6:  Quantity Pie  |  Member vs Normal avg spend
# ──────────────────────────────────────────────
col9, col10 = st.columns(2)

with col9:
    qty_prod = df.groupby("Product line")["Quantity"].sum().reset_index()
    fig = px.pie(
        qty_prod, names="Product line", values="Quantity",
        color_discrete_sequence=PALETTE,
        title="🛍️ Quantity Sold by Product Line",
        hole=0.3,
    )
    fig.update_traces(textinfo="label+percent", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col10:
    cust_avg = (
        df.groupby("Customer type")["Sales"].mean().reset_index()
    )
    cust_avg.columns = ["Customer Type", "Avg Sale"]
    cust_avg["Avg Sale"] = cust_avg["Avg Sale"].round(2)
    fig = px.bar(
        cust_avg, x="Customer Type", y="Avg Sale",
        color="Customer Type", color_discrete_sequence=[PALETTE[0], PALETTE[1]],
        text="Avg Sale",
        title="🎟️ Avg Sale Value: Member vs Normal",
        labels={"Avg Sale": "Avg Sale (₹)", "Customer Type": ""},
    )
    fig.update_traces(texttemplate="₹%{text:,.2f}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_tickprefix="₹", yaxis_tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# BUSINESS INSIGHTS
# ──────────────────────────────────────────────
st.divider()
st.markdown("### 💡 Business Insights")

top_br_city = BRANCH_CITY.get(top_branch, "")
top_payment = df.groupby("Payment")["Invoice ID"].count().idxmax()
pay_txns    = df.groupby("Payment")["Invoice ID"].count().max()
best_month  = (
    df.groupby("Month")["Sales"].sum()
      .reindex([m for m in MONTH_ORDER if m in df["Month"].unique()])
      .idxmax()
)
mem_avg  = df[df["Customer type"] == "Member"]["Sales"].mean() if "Member" in df["Customer type"].values else 0
norm_avg = df[df["Customer type"] == "Normal"]["Sales"].mean() if "Normal" in df["Customer type"].values else 0

i1, i2, i3 = st.columns(3)
with i1:
    st.info(
        f"**🏆 Top Branch:** Branch {top_branch} ({top_br_city})\n\n"
        f"Revenue: **₹{df.groupby('Branch')['Sales'].sum()[top_branch]:,.2f}**\n\n"
        f"Study what drives its performance and replicate across other branches."
    )
with i2:
    st.info(
        f"**📦 Top Product Line:** {top_product}\n\n"
        f"Revenue: **₹{df.groupby('Product line')['Sales'].sum()[top_product]:,.2f}**\n\n"
        f"Stock more of this category and run targeted promotions."
    )
with i3:
    st.info(
        f"**💳 Top Payment:** {top_payment} ({pay_txns} transactions)\n\n"
        f"Offer cashback or loyalty rewards on {top_payment} to retain high-frequency users."
    )

j1, j2, j3 = st.columns(3)
with j1:
    st.success(
        f"**📈 Best Month:** {best_month}\n\n"
        f"Revenue: **₹{df.groupby('Month')['Sales'].sum().get(best_month, 0):,.2f}**\n\n"
        f"Plan peak-season stock-up and deals around this month."
    )
with j2:
    direction = "Members" if mem_avg >= norm_avg else "Normal customers"
    diff = abs(mem_avg - norm_avg)
    st.success(
        f"**👥 Spend Gap:** {direction} spend more\n\n"
        f"Member avg: **₹{mem_avg:,.2f}** · Normal avg: **₹{norm_avg:,.2f}**\n\n"
        f"Difference of ₹{diff:,.2f} — consider membership incentives."
    )
with j3:
    st.success(
        f"**⭐ Avg Rating:** {avg_rating:.2f} / 10\n\n"
        f"Ratings below 6 signal service gaps. "
        f"Improve customer experience to push above 7."
    )

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.divider()
st.caption("Supermarket Sales Analytics · Built with Streamlit & Plotly · IBM Bob")
