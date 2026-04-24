import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Veridi Logistics — Delivery Audit",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080C14;
    color: #E8EDF5;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0D1220;
    border-right: 1px solid #1E2840;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0F1829 0%, #111D35 100%);
    border: 1px solid #1E2F50;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
[data-testid="metric-container"] label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B82A8 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E8EDF5 !important;
}

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #4A6080;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.2rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #4D9FFF !important;
    border-bottom: 2px solid #4D9FFF !important;
    background: transparent !important;
}

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4D9FFF;
    margin: 1.6rem 0 1rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1E2840;
}

/* Alert banners */
.alert-critical {
    background: linear-gradient(90deg, rgba(220,53,69,0.15) 0%, rgba(220,53,69,0.05) 100%);
    border-left: 3px solid #DC3545;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #FF6B7A;
}
.alert-warning {
    background: linear-gradient(90deg, rgba(255,165,0,0.15) 0%, rgba(255,165,0,0.05) 100%);
    border-left: 3px solid #FFA500;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #FFB84D;
}
.alert-good {
    background: linear-gradient(90deg, rgba(40,167,69,0.15) 0%, rgba(40,167,69,0.05) 100%);
    border-left: 3px solid #28A745;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #5DD47A;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #1E2840;
    border-radius: 8px;
}

/* Selectbox & multiselect */
[data-testid="stSelectbox"], [data-testid="stMultiSelect"] {
    background-color: #0D1220;
}

/* Divider */
hr { border-color: #1E2840; }

/* Plotly chart container */
.js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
MASTER_URL   = "https://drive.google.com/uc?id=1sZHcutPQvNXXTDS9rRnidTV4eRS52dgU"
MONTHLY_URL  = "https://drive.google.com/uc?id=1oIRA_LUhoPb_USERP_-4nNbgqcyhlMvQ"
STATE_URL    = "https://drive.google.com/uc?id=1PrRmbxPQ0PeZQZ00IxH159cla2m-tlB3"
CATEGORY_URL = "https://drive.google.com/uc?id=1Qraq9hbnbAe2GRNktRr3xN83o52Llbr3"

@st.cache_data(show_spinner=False)
def load_data():
    master_df   = pd.read_csv(MASTER_URL)
    monthly_df  = pd.read_csv(MONTHLY_URL)
    state_df    = pd.read_csv(STATE_URL)
    category_df = pd.read_csv(CATEGORY_URL)
    return master_df, monthly_df, state_df, category_df

with st.spinner("Loading data..."):
    master_df, monthly_df, state_df, category_df = load_data()

# ─────────────────────────────────────────────
#  PLOTLY DARK THEME HELPER
# ─────────────────────────────────────────────
CHART_BG  = "#080C14"
GRID_COLOR = "#1A2540"

def dark(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_BG,
        font=dict(family="DM Sans", color="#B0BDD0", size=12),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#1E2840",
            borderwidth=1
        ),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor="#1E2840"),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor="#1E2840"),
        title_font=dict(family="Syne", size=14, color="#C8D5E8")
    )
    return fig

# Color palette
STATUS_COLORS = {
    "On Time":    "#2ECC71",
    "Late":       "#F39C12",
    "Super Late": "#E74C3C"
}

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
        <div style='font-family:Syne;font-size:1.1rem;font-weight:800;color:#4D9FFF;letter-spacing:0.05em'>
            VERIDI LOGISTICS
        </div>
        <div style='font-family:DM Sans;font-size:0.72rem;color:#4A6080;letter-spacing:0.12em;text-transform:uppercase;margin-top:2px'>
            Delivery Performance Audit
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Filters")

    selected_states = st.multiselect(
        "Filter by State",
        options=sorted(master_df["customer_state"].dropna().unique()),
        placeholder="All states"
    )

    selected_statuses = st.multiselect(
        "Delivery Status",
        options=["On Time", "Late", "Super Late"],
        placeholder="All statuses"
    )

    selected_categories = st.multiselect(
        "Product Category",
        options=sorted(master_df["product_category_name_english"].dropna().unique()),
        placeholder="All categories"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-family:DM Sans;font-size:0.72rem;color:#3A4F6A;line-height:1.6'>
        <b style='color:#4A6080'>Dataset:</b> Olist E-Commerce<br>
        <b style='color:#4A6080'>Orders:</b> 96,470 delivered<br>
        <b style='color:#4A6080'>Period:</b> 2016 – 2018<br>
        <b style='color:#4A6080'>Regions:</b> 27 Brazilian states
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = master_df.copy()
if selected_states:
    df = df[df["customer_state"].isin(selected_states)]
if selected_statuses:
    df = df[df["delivery_status"].isin(selected_statuses)]
if selected_categories:
    df = df[df["product_category_name_english"].isin(selected_categories)]

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style='padding: 1.2rem 0 0.5rem 0'>
    <h1 style='font-family:Syne;font-size:2rem;font-weight:800;color:#E8EDF5;margin:0;letter-spacing:-0.02em'>
        📦 Delivery Performance Audit
    </h1>
    <p style='font-family:DM Sans;font-size:0.9rem;color:#4A6080;margin:0.3rem 0 0 0;letter-spacing:0.02em'>
        Last-mile logistics accuracy · Customer sentiment correlation · Regional failure analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────
total        = len(df)
late_count   = df["is_late"].sum() if "is_late" in df.columns else 0
late_pct     = (late_count / total * 100) if total > 0 else 0
avg_delay    = df["days_difference"].mean() if "days_difference" in df.columns else 0
avg_review   = df["review_score"].mean() if "review_score" in df.columns else 0
super_late_n = (df["delivery_status"] == "Super Late").sum() if "delivery_status" in df.columns else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Orders",     f"{total:,}")
k2.metric("Late Rate",        f"{late_pct:.1f}%",   delta=f"{late_pct - 8.1:.1f}% vs avg", delta_color="inverse")
k3.metric("Avg Delay Buffer", f"{avg_delay:.1f} d", help="Positive = arrived early, Negative = arrived late")
k4.metric("Avg Review Score", f"{avg_review:.2f} / 5")
k5.metric("Super Late Orders",f"{super_late_n:,}",  delta_color="inverse")

st.markdown("")

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Overview",
    "🗺️  Geography",
    "📦  Categories",
    "🚨  Anomalies",
    "🔍  Drill-Down"
])

# ══════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Delivery Status Breakdown</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        # Donut chart — delivery status distribution
        status_counts = df["delivery_status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        status_counts["color"] = status_counts["status"].map(STATUS_COLORS)

        fig = go.Figure(go.Pie(
            labels=status_counts["status"],
            values=status_counts["count"],
            hole=0.65,
            marker=dict(colors=status_counts["color"].tolist(),
                        line=dict(color=CHART_BG, width=3)),
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12),
            hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>"
        ))
        fig.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:10px'>orders</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Syne", size=18, color="#E8EDF5"),
            align="center"
        )
        fig.update_layout(title="Order Status Distribution", showlegend=True,
                          legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(dark(fig, 380), use_container_width=True)

    with col_b:
        # Bar chart — avg review by delivery status
        status_review = df.groupby("delivery_status")["review_score"].mean().reindex(
            ["On Time", "Late", "Super Late"]).reset_index()
        status_review.columns = ["status", "avg_score"]

        fig = go.Figure(go.Bar(
            x=status_review["status"],
            y=status_review["avg_score"],
            marker=dict(
                color=[STATUS_COLORS.get(s, "#4D9FFF") for s in status_review["status"]],
                line=dict(color=CHART_BG, width=1)
            ),
            text=status_review["avg_score"].round(2),
            textposition="outside",
            textfont=dict(family="Syne", size=14, color="#E8EDF5"),
            hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.2f}<extra></extra>"
        ))
        fig.update_layout(
            title="Avg Review Score by Delivery Status",
            yaxis=dict(range=[1, 5.2], title="Avg Review Score"),
            xaxis_title=""
        )
        st.plotly_chart(dark(fig, 380), use_container_width=True)

    st.markdown('<div class="section-title">Delay vs Customer Satisfaction</div>', unsafe_allow_html=True)

    # Line chart — delay days vs avg review score (binned)
    df_plot = df.copy()
    df_plot["delay_bin"] = pd.cut(df_plot["days_difference"],
                                   bins=range(-60, 50, 5),
                                   labels=[f"{i}" for i in range(-60, 45, 5)])
    delay_review = df_plot.groupby("delay_bin", observed=True).agg(
        avg_score=("review_score", "mean"),
        count=("order_id", "count")
    ).reset_index()
    delay_review = delay_review[delay_review["count"] >= 20]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=delay_review["delay_bin"].astype(str),
        y=delay_review["avg_score"],
        mode="lines+markers",
        line=dict(color="#4D9FFF", width=2.5),
        marker=dict(size=6, color="#4D9FFF",
                    line=dict(color=CHART_BG, width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(77,159,255,0.08)",
        name="Avg Review Score",
        hovertemplate="Delay bin: %{x} days<br>Avg Score: %{y:.2f}<extra></extra>"
    ))
    # Find index position of "0" bin in x-axis labels for categorical axis
    x_labels = delay_review["delay_bin"].astype(str).tolist()
    zero_idx = x_labels.index("0") if "0" in x_labels else None
    if zero_idx is not None:
        fig.add_shape(
            type="line",
            x0=zero_idx, x1=zero_idx,
            y0=1, y1=5,
            xref="x", yref="y",
            line=dict(color="#F39C12", width=1.5, dash="dash")
        )
        fig.add_annotation(
            x=zero_idx, y=4.8,
            text="On-Time Threshold",
            showarrow=False,
            font=dict(color="#F39C12", size=11),
            xref="x", yref="y"
        )
    fig.update_layout(
        title="Delivery Delay (Days) vs Average Review Score",
        xaxis_title="Days Difference (Positive = Early, Negative = Late)",
        yaxis_title="Avg Review Score",
        yaxis=dict(range=[1, 5])
    )
    st.plotly_chart(dark(fig, 380), use_container_width=True)

    # Insight banner
    on_time_score = status_review[status_review["status"] == "On Time"]["avg_score"].values
    super_late_score = status_review[status_review["status"] == "Super Late"]["avg_score"].values
    if len(on_time_score) and len(super_late_score):
        drop = on_time_score[0] - super_late_score[0]
        st.markdown(f"""
        <div class="alert-critical">
            ⚡ <b>Key Finding:</b> Super Late deliveries score {super_late_score[0]:.2f}/5 vs {on_time_score[0]:.2f}/5 for On Time orders —
            a <b>{drop:.2f} point drop</b> in satisfaction. Late logistics is the primary driver of negative reviews.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — GEOGRAPHY
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">State-Level Late Delivery Rate</div>', unsafe_allow_html=True)

    state_sorted = state_df.sort_values("late_pct", ascending=True)

    fig = go.Figure(go.Bar(
        x=state_sorted["late_pct"],
        y=state_sorted["customer_state"],
        orientation="h",
        marker=dict(
            color=state_sorted["late_pct"],
            colorscale=[[0, "#1A3A5C"], [0.5, "#F39C12"], [1, "#DC3545"]],
            showscale=True,
            colorbar=dict(title=dict(text="Late %", font=dict(color="#6B82A8")), tickfont=dict(color="#6B82A8"))
        ),
        text=state_sorted["late_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(size=10),
        customdata=state_sorted[["avg_review_score", "total_orders", "avg_delay_days"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Late Rate: %{x:.1f}%<br>"
            "Avg Review: %{customdata[0]:.2f}<br>"
            "Total Orders: %{customdata[1]:,}<br>"
            "Avg Delay Buffer: %{customdata[2]:.1f} days<extra></extra>"
        )
    ))
    fig.add_vline(x=state_df["late_pct"].mean(), line_dash="dash",
                  line_color="#4D9FFF", line_width=1.5,
                  annotation=dict(
                      text=f"National avg: {state_df['late_pct'].mean():.1f}%",
                      font=dict(color="#4D9FFF", size=11)
                  ))
    fig.update_layout(title="Late Delivery Rate by Brazilian State", xaxis_title="Late %")
    st.plotly_chart(dark(fig, 620), use_container_width=True)

    st.markdown('<div class="section-title">Business Impact — Volume vs Late Rate</div>', unsafe_allow_html=True)

    fig = px.scatter(
        state_df,
        x="total_orders",
        y="late_pct",
        size="total_orders",
        color="late_pct",
        color_continuous_scale=[[0, "#1A5C3A"], [0.5, "#F39C12"], [1, "#DC3545"]],
        hover_name="customer_state",
        text="customer_state",
        size_max=60,
        custom_data=["avg_review_score", "late_orders"]
    )
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=9, color="#B0BDD0"),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Total Orders: %{x:,}<br>"
            "Late Rate: %{y:.1f}%<br>"
            "Late Orders: %{customdata[1]:,}<br>"
            "Avg Review: %{customdata[0]:.2f}<extra></extra>"
        )
    )
    fig.update_layout(
        title="Order Volume vs Late Delivery Rate (Bubble = Volume)",
        xaxis_title="Total Orders",
        yaxis_title="Late Rate (%)",
        coloraxis_showscale=False
    )

    # Add quadrant annotations
    mid_x = state_df["total_orders"].median()
    mid_y = state_df["late_pct"].median()
    fig.add_annotation(x=state_df["total_orders"].max()*0.7, y=state_df["late_pct"].max()*0.9,
                       text="🔴 High Volume + High Late<br>(Priority Fix)", showarrow=False,
                       font=dict(color="#E74C3C", size=10), bgcolor="rgba(231,76,60,0.1)",
                       bordercolor="#E74C3C", borderwidth=1, borderpad=6)
    fig.add_annotation(x=state_df["total_orders"].max()*0.7, y=state_df["late_pct"].min()*1.5,
                       text="🟢 High Volume + Low Late<br>(Best Practice)", showarrow=False,
                       font=dict(color="#2ECC71", size=10), bgcolor="rgba(46,204,113,0.1)",
                       bordercolor="#2ECC71", borderwidth=1, borderpad=6)

    st.plotly_chart(dark(fig, 500), use_container_width=True)

    # Geographic insight
    worst = state_df.nlargest(3, "late_pct")["customer_state"].tolist()
    st.markdown(f"""
    <div class="alert-warning">
        🗺️ <b>Regional Finding:</b> The Northeast states ({', '.join(worst)}) consistently show the highest late rates —
        all above 15%. However, remote northern states (AC, RO, AM) paradoxically show low late rates
        because Veridi over-pads delivery estimates for remote areas.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 3 — CATEGORIES
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Late Rate by Product Category</div>', unsafe_allow_html=True)

    n_categories = st.slider("Show top N worst categories", min_value=10, max_value=52, value=20, step=5)
    top_cats = category_df.nlargest(n_categories, "late_pct")

    fig = go.Figure(go.Bar(
        x=top_cats["late_pct"],
        y=top_cats["product_category_name_english"],
        orientation="h",
        marker=dict(
            color=top_cats["late_pct"],
            colorscale=[[0, "#1A3A5C"], [0.5, "#F39C12"], [1, "#DC3545"]],
            showscale=False
        ),
        text=top_cats["late_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
        textfont=dict(size=10),
        customdata=top_cats[["avg_review_score", "total_orders"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Late Rate: %{x:.1f}%<br>"
            "Avg Review: %{customdata[0]:.2f}<br>"
            "Total Orders: %{customdata[1]:,}<extra></extra>"
        )
    ))
    fig.add_vline(x=category_df["late_pct"].mean(), line_dash="dash",
                  line_color="#4D9FFF", line_width=1.5,
                  annotation=dict(
                      text=f"Avg: {category_df['late_pct'].mean():.1f}%",
                      font=dict(color="#4D9FFF", size=11)
                  ))
    fig.update_layout(title=f"Top {n_categories} Worst-Performing Product Categories")
    st.plotly_chart(dark(fig, max(400, n_categories * 22)), use_container_width=True)

    st.markdown('<div class="section-title">Category — Late Rate vs Review Score</div>', unsafe_allow_html=True)

    fig = px.scatter(
        category_df,
        x="late_pct",
        y="avg_review_score",
        size="total_orders",
        color="late_pct",
        color_continuous_scale=[[0, "#1A5C3A"], [0.5, "#F39C12"], [1, "#DC3545"]],
        hover_name="product_category_name_english",
        size_max=40,
        custom_data=["total_orders"]
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Late Rate: %{x:.1f}%<br>"
            "Avg Review: %{y:.2f}<br>"
            "Orders: %{customdata[0]:,}<extra></extra>"
        )
    )
    fig.update_layout(
        title="Category Late Rate vs Avg Review Score (Bubble = Volume)",
        xaxis_title="Late Rate (%)",
        yaxis_title="Avg Review Score",
        coloraxis_showscale=False
    )
    st.plotly_chart(dark(fig, 450), use_container_width=True)

    st.markdown("""
    <div class="alert-warning">
        📦 <b>Category Finding:</b> <b>Audio</b> (13.0%) and <b>Fashion Underwear/Beach</b> (12.8%) have the worst late rates.
        <b>Office Furniture</b> (9.3%) has one of the lowest review scores (3.65) — furniture buyers are the
        least forgiving customers when deliveries are late.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 4 — ANOMALIES
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Systemic Anomaly Detection — March 2018 Crisis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-critical">
        🚨 <b>Critical Finding:</b> A systemic logistics failure hit <b>15 out of 16 major states simultaneously in March 2018</b>.
        Late rates spiked 3–4 standard deviations above normal before collapsing back in April 2018 —
        suggesting a specific operational event (carrier strike, system outage, or warehouse failure).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Heatmap using z-scores
    sufficient_states = monthly_df.groupby("customer_state")["late_pct"].count()
    sufficient_states = sufficient_states[sufficient_states >= 15].index.tolist()
    monthly_filtered = monthly_df[monthly_df["customer_state"].isin(sufficient_states)].copy()

    heatmap_pivot = monthly_filtered.pivot_table(
        index="customer_state",
        columns="order_month_str",
        values="z_score",
        aggfunc="mean"
    )
    heatmap_pivot = heatmap_pivot.loc[
        heatmap_pivot.max(axis=1).sort_values(ascending=False).index
    ]

    fig = go.Figure(go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns.tolist(),
        y=heatmap_pivot.index.tolist(),
        colorscale=[
            [0,    "#1A5C3A"],
            [0.35, "#2ECC71"],
            [0.5,  "#F5F0DC"],
            [0.65, "#F39C12"],
            [1,    "#DC3545"]
        ],
        zmid=0,
        zmin=-2,
        zmax=4,
        colorbar=dict(
            title=dict(text="Z-Score", font=dict(color="#6B82A8")),
            tickfont=dict(color="#6B82A8")
        ),
        hovertemplate="State: %{y}<br>Month: %{x}<br>Z-Score: %{z:.2f}<extra></extra>"
    ))
    fig.update_layout(
        title="Delivery Anomaly Heatmap — Z-Score by State & Month<br><sup>Red = Abnormally High Late Rate | Green = Better Than Normal</sup>",
        xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=10))
    )
    st.plotly_chart(dark(fig, 520), use_container_width=True)

    st.markdown('<div class="section-title">Monthly Trend — State Deep Dive</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 3])
    with col_left:
        state_choice = st.selectbox(
            "Select State",
            options=sorted(monthly_filtered["customer_state"].unique()),
            index=list(sorted(monthly_filtered["customer_state"].unique())).index("SP")
            if "SP" in monthly_filtered["customer_state"].unique() else 0
        )
        compare_states = st.multiselect(
            "Compare with",
            options=[s for s in sorted(monthly_filtered["customer_state"].unique()) if s != state_choice],
            default=["RJ", "MG"] if all(x in monthly_filtered["customer_state"].unique() for x in ["RJ", "MG"]) else []
        )

    with col_right:
        trend_states = [state_choice] + compare_states
        palette = ["#4D9FFF", "#F39C12", "#2ECC71", "#E74C3C", "#9B59B6", "#1ABC9C"]

        fig = go.Figure()
        for i, state in enumerate(trend_states):
            trend = monthly_filtered[monthly_filtered["customer_state"] == state]
            fig.add_trace(go.Scatter(
                x=trend["order_month_str"],
                y=trend["late_pct"],
                mode="lines+markers",
                name=state,
                line=dict(color=palette[i % len(palette)], width=2),
                marker=dict(size=5),
                hovertemplate=f"<b>{state}</b><br>Month: %{{x}}<br>Late Rate: %{{y:.1f}}%<extra></extra>"
            ))

        # Mean line for primary state
        primary_mean = monthly_filtered[monthly_filtered["customer_state"] == state_choice]["late_pct"].mean()
        fig.add_hline(y=primary_mean, line_dash="dot", line_color=palette[0],
                      line_width=1, opacity=0.5,
                      annotation=dict(
                          text=f"{state_choice} avg: {primary_mean:.1f}%",
                          font=dict(color=palette[0], size=10)
                      ))

        # March 2018 anomaly marker — use shape+annotation (categorical x-axis)
        x_labels = monthly_filtered[monthly_filtered["customer_state"] == state_choice]["order_month_str"].tolist()
        if "2018-03" in x_labels:
            march_idx = x_labels.index("2018-03")
            fig.add_shape(
                type="line",
                x0=march_idx, x1=march_idx,
                y0=0, y1=1,
                xref="x", yref="paper",
                line=dict(color="#DC3545", width=2, dash="dash")
            )
            fig.add_annotation(
                x=march_idx, y=1.05,
                text="March 2018",
                showarrow=False,
                font=dict(color="#DC3545", size=11),
                xref="x", yref="paper"
            )

        fig.update_layout(
            title=f"Monthly Late Rate Trend — {', '.join(trend_states)}",
            xaxis=dict(tickangle=-45, tickfont=dict(size=9)),
            yaxis_title="Late Rate (%)",
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(dark(fig, 400), use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 5 — DRILL-DOWN
# ══════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Order-Level Exploration</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        drill_state = st.selectbox(
            "Select State to Inspect",
            options=sorted(master_df["customer_state"].unique())
        )
    with col2:
        drill_status = st.selectbox(
            "Filter by Delivery Status",
            options=["All", "On Time", "Late", "Super Late"]
        )

    drill_df = master_df[master_df["customer_state"] == drill_state].copy()
    if drill_status != "All":
        drill_df = drill_df[drill_df["delivery_status"] == drill_status]

    # Mini KPIs for selected state
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Orders in State",    f"{len(drill_df):,}")
    m2.metric("Late Rate",          f"{drill_df['is_late'].mean()*100:.1f}%")
    m3.metric("Avg Review Score",   f"{drill_df['review_score'].mean():.2f}")
    m4.metric("Avg Delay Buffer",   f"{drill_df['days_difference'].mean():.1f} days")

    st.markdown("")

    # Review score distribution for selected state
    col_a, col_b = st.columns(2)
    with col_a:
        review_dist = drill_df["review_score"].value_counts().sort_index().reset_index()
        review_dist.columns = ["score", "count"]
        score_colors = {1: "#DC3545", 2: "#E67E22", 3: "#F39C12", 4: "#2ECC71", 5: "#27AE60"}
        fig = go.Figure(go.Bar(
            x=review_dist["score"],
            y=review_dist["count"],
            marker_color=[score_colors.get(s, "#4D9FFF") for s in review_dist["score"]],
            text=review_dist["count"],
            textposition="outside"
        ))
        fig.update_layout(title=f"Review Score Distribution — {drill_state}",
                          xaxis_title="Review Score", yaxis_title="Orders")
        st.plotly_chart(dark(fig, 320), use_container_width=True)

    with col_b:
        cat_drill = drill_df.groupby("product_category_name_english").agg(
            count=("order_id", "count"),
            late_pct=("is_late", "mean")
        ).reset_index().nlargest(10, "count")
        cat_drill["late_pct"] = cat_drill["late_pct"] * 100

        fig = go.Figure(go.Bar(
            x=cat_drill["count"],
            y=cat_drill["product_category_name_english"],
            orientation="h",
            marker_color="#4D9FFF",
            text=cat_drill["count"],
            textposition="outside"
        ))
        fig.update_layout(title=f"Top 10 Categories — {drill_state}",
                          xaxis_title="Orders")
        st.plotly_chart(dark(fig, 320), use_container_width=True)

    # Raw table
    st.markdown('<div class="section-title">Raw Order Records</div>', unsafe_allow_html=True)

    display_cols = [
        "order_id", "customer_state", "delivery_status",
        "days_difference", "review_score", "product_category_name_english"
    ]
    available_cols = [c for c in display_cols if c in drill_df.columns]

    st.dataframe(
        drill_df[available_cols].head(100).style.map(
            lambda v: "color: #E74C3C" if v == "Super Late"
            else "color: #F39C12" if v == "Late"
            else "color: #2ECC71" if v == "On Time" else "",
            subset=["delivery_status"] if "delivery_status" in available_cols else []
        ),
        use_container_width=True,
        height=350
    )

    st.caption(f"Showing first 100 of {len(drill_df):,} records for {drill_state} ({drill_status})")

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-family:DM Sans;font-size:0.75rem;color:#2A3A55;padding:1rem 0'>
    Veridi Logistics — Delivery Performance Audit &nbsp;|&nbsp;
    Data: Olist Brazilian E-Commerce Dataset &nbsp;|&nbsp;
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)