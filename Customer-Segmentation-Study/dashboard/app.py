import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Segmentation Study",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("data/processed/customer_segments.csv")

# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="main-title">📊 Customer Segmentation Study</div>',
    unsafe_allow_html=True
)
st.markdown(
    "### RFM-Based Customer Segmentation Dashboard"
)

st.write(
    "This dashboard analyzes customers using Recency, Frequency, "
    "and Monetary (RFM) analysis."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

segments = ["All"] + sorted(df["Segment"].unique().tolist())

selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    segments
)

# Apply filter
if selected_segment == "All":
    filtered_df = df
else:
    filtered_df = df[df["Segment"] == selected_segment]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 Total Customers",
        value=f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        label="💰 Average Spending",
        value=f"₹{filtered_df['Monetary'].mean():,.0f}"
    )

with col3:
    st.metric(
        label="🔄 Average Frequency",
        value=f"{filtered_df['Frequency'].mean():.1f}"
    )

with col4:
    st.metric(
        label="⏳ Average Recency",
        value=f"{filtered_df['Recency'].mean():.0f} days"
    )
# -----------------------------
# Customer Segment Distribution
# -----------------------------
st.subheader("👥 Customer Segment Distribution")

segment_count = (
    filtered_df["Segment"]
    .value_counts()
    .reset_index()
)

segment_count.columns = ["Segment", "Customers"]

fig1 = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    title="Customer Distribution by Segment",
    hole=0.35
)

st.plotly_chart(fig1, width="stretch")

# -----------------------------
# Average Spending by Segment
# -----------------------------
st.subheader("💰 Average Spending by Segment")

average_spending = (
    filtered_df.groupby("Segment")["Monetary"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    average_spending,
    x="Monetary",
    y="Segment",
    orientation="h",
    title="Average Spending by Customer Segment",
    text_auto=".2s"
)

fig2.update_layout(
    xaxis_title="Average Spending",
    yaxis_title="Customer Segment"
)

st.plotly_chart(fig2, width="stretch")

# -----------------------------
# RFM Analysis
# -----------------------------
st.subheader("📈 RFM Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    fig3 = px.histogram(
        filtered_df,
        x="Recency",
        title="⏳ Recency Distribution",
        nbins=20
    )
    st.plotly_chart(fig3, width="stretch", key="recency_chart")

with col2:
    fig4 = px.histogram(
        filtered_df,
        x="Frequency",
        title="🔄 Frequency Distribution",
        nbins=20
    )
    st.plotly_chart(fig4, width="stretch", key="frequency_chart")

with col3:
    fig5 = px.histogram(
        filtered_df,
        x="Monetary",
        title="💰 Monetary Distribution",
        nbins=20
    )
    st.plotly_chart(fig5, width="stretch", key="monetary_chart")
# -----------------------------
# RFM Score Analysis
# -----------------------------
st.subheader("⭐ RFM Score Analysis")

score_columns = ["R_Score", "F_Score", "M_Score"]

score_average = (
    filtered_df[score_columns]
    .mean()
    .reset_index()
)

score_average.columns = ["RFM Component", "Average Score"]

fig6 = px.bar(
    score_average,
    x="RFM Component",
    y="Average Score",
    title="Average RFM Component Scores",
    text_auto=".2f"
)

st.plotly_chart(fig3, width="stretch")
# -----------------------------
# Customer Data Table
# -----------------------------
st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)
    # Download Filtered Data
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Customer Data",
    data=csv,
    file_name="customer_data_filtered.csv",
    mime="text/csv"
)
# -----------------------------

# Business Insights
st.subheader("💡 Business Insights")

if selected_segment == "All":

    total_customers = len(df)
    champions = len(df[df["Segment"] == "Champions"])
    loyal = len(df[df["Segment"] == "Loyal Customers"])
    potential = len(df[df["Segment"] == "Potential Loyalists"])
    at_risk = len(df[df["Segment"] == "At Risk"])
    lost = len(df[df["Segment"] == "Lost Customers"])

    st.markdown("### 📊 Customer Segment Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"🏆 **Champions:** {champions} customers\n\n"
            "These are highly valuable customers. "
            "Focus on retention, loyalty rewards and premium offers."
        )

        st.success(
            f"❤️ **Loyal Customers:** {loyal} customers\n\n"
            "These customers show strong engagement. "
            "Use upselling and cross-selling strategies."
        )

        st.info(
            f"🌱 **Potential Loyalists:** {potential} customers\n\n"
            "These customers have growth potential. "
            "Encourage repeat purchases with personalized offers."
        )

    with col2:
        st.warning(
            f"⚠️ **At Risk:** {at_risk} customers\n\n"
            "These customers may be losing engagement. "
            "Use targeted re-engagement campaigns."
        )

        st.error(
            f"🔴 **Lost Customers:** {lost} customers\n\n"
            "These customers have low engagement. "
            "Consider win-back campaigns and special offers."
        )

    st.markdown("### 🎯 Recommended Business Actions")

    st.write(
        "• Retain Champions with loyalty programs and exclusive rewards."
    )
    st.write(
        "• Upsell and cross-sell products to Loyal Customers."
    )
    st.write(
        "• Convert Potential Loyalists into Loyal Customers through personalized campaigns."
    )
    st.write(
        "• Re-engage At Risk customers before they become inactive."
    )
    st.write(
        "• Use win-back offers to target Lost Customers."
    )

else:

    st.markdown(
        f"### 🔎 Selected Segment: **{selected_segment}**"
    )

    st.metric(
        "Customers in Segment",
        f"{len(filtered_df):,}"
    )

    st.metric(
        "Average Spending",
        f"₹{filtered_df['Monetary'].mean():,.0f}"
    )

    st.write(
        "Use the RFM metrics and customer data above to understand "
        "the behavior of this customer segment."
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "Customer Segmentation Study | RFM Analysis | "
    "Python • Pandas • Streamlit • Plotly"
)