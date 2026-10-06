import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Open USD (OUSD) — Bridge Stablecoin",
    page_icon="💵",
    layout="wide",
)

# --- palette (validated dark-mode categorical) ---
S1 = "#3987e5"
S2 = "#d95926"
S3 = "#199e70"
S4 = "#c98500"
SURFACE = "#1a1a19"
GRID = "#333332"
MUTED = "#87867d"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c3c2b7", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    hoverlabel=dict(bgcolor="#2c2c2b", font_color="#ffffff", bordercolor="#333332"),
    hovermode="x unified",
)
DEFAULT_AXIS = dict(gridcolor=GRID, showgrid=True, zeroline=False)

# ── DATA ─────────────────────────────────────────────────────────────────────

FULL_HISTORY_RAW = [
    (1777334400, 12), (1777420800, 600), (1777507200, 600), (1777593600, 600),
    (1777680000, 600), (1777766400, 600), (1777852800, 600), (1777939200, 600),
    (1778025600, 600), (1778112000, 600), (1778198400, 600), (1778284800, 600),
    (1778371200, 600), (1778457600, 600), (1778544000, 600), (1778630400, 600),
    (1778716800, 600), (1778803200, 600), (1778889600, 600), (1778976000, 600),
    (1779062400, 600), (1779148800, 600), (1779235200, 600), (1779321600, 600),
    (1779408000, 605), (1779494400, 605), (1779580800, 605), (1779667200, 605),
    (1779753600, 604), (1779840000, 604), (1779926400, 604), (1780012800, 604),
    (1780099200, 604), (1780185600, 604), (1780272000, 801), (1780358400, 801),
    (1780444800, 801), (1780531200, 801), (1780617600, 801), (1780704000, 801),
    (1780790400, 801), (1780876800, 801), (1780963200, 801), (1781049600, 801),
    (1781136000, 801), (1781222400, 801), (1781308800, 801), (1781395200, 801),
    (1781481600, 801), (1781568000, 801), (1781654400, 801), (1781740800, 801),
    (1781827200, 801), (1781913600, 801), (1782000000, 801), (1782086400, 801),
    (1782172800, 801), (1782259200, 801), (1782345600, 801), (1782432000, 1001),
    (1782518400, 1001), (1782604800, 1001), (1782691200, 1001), (1782777600, 1001),
    (1782864000, 1001), (1782950400, 1001), (1783036800, 1001), (1783123200, 1001),
    (1783209600, 1001), (1783296000, 1001), (1783382400, 1201), (1783468800, 1201),
    (1783555200, 1201), (1783641600, 1201), (1783728000, 1201), (1783814400, 1201),
    (1783900800, 1201), (1783987200, 1201), (1784073600, 1201), (1784160000, 1155.76),
    (1784246400, 1155.76), (1784332800, 1155.76), (1784419200, 1155.76),
    (1784505600, 1154.77), (1784592000, 1154.77), (1784678400, 1154.77),
    (1784764800, 1155.79), (1784851200, 1155.79), (1784937600, 1155.79),
    (1785024000, 1155.79), (1785110400, 1155.79), (1785196800, 1155.79),
    (1785283200, 1155.79), (1785369600, 1155.79), (1785456000, 926.74),
    (1785542400, 926.74), (1785628800, 926.74), (1785715200, 926.74),
    (1785801600, 40645.76), (1785888000, 40645.76), (1785974400, 40645.76),
    (1786060800, 40645.76), (1786147200, 40645.76), (1786233600, 40645.76),
    (1786320000, 40645.76), (1786406400, 40645.76), (1786492800, 40645.76),
    (1786579200, 40645.76), (1786665600, 40645.76), (1786752000, 40645.76),
    (1786838400, 40645.76), (1786924800, 40645.76), (1787011200, 40645.76),
    (1787097600, 40645.76), (1787184000, 40645.76), (1787270400, 30592),
    (1787356800, 30592), (1787443200, 30592), (1787529600, 30592),
    (1787616000, 30628.4), (1787702400, 30629.4), (1787788800, 40692.16),
    (1787875200, 40693.16), (1787961600, 40693.16), (1788048000, 40693.16),
    (1788134400, 40692.16), (1788220800, 40692.16), (1788307200, 40804.16),
    (1788393600, 40819.16), (1788480000, 40824.16), (1788566400, 40824.16),
    (1788652800, 40824.16), (1788739200, 40824.16), (1788825600, 40824.16),
    (1788912000, 40875.16), (1788998400, 40906.46), (1789084800, 40907.46),
    (1789171200, 40907.46), (1789257600, 40907.46), (1789344000, 41371.88),
    (1789430400, 41392.98), (1789516800, 41390.98), (1789603200, 41485.33),
    (1789689600, 41517.5), (1789776000, 41517.5), (1789862400, 41517.5),
    (1789948800, 42556.51), (1790035200, 43032.19), (1790121600, 40006013.09),
    (1790208000, 40006581.36), (1790294400, 40008299.71), (1790380800, 40008304.71),
    (1790467200, 40008304.71), (1790553600, 40009162.5), (1790640000, 454459686.73),
    (1790726400, 490625166.88), (1790812800, 668499579.3), (1790899200, 665214297.22),
    (1790985600, 666274725.39), (1791072000, 666275228.44), (1791158400, 698823817.64),
    (1791244800, 698823910.84),
]

df_full = pd.DataFrame(FULL_HISTORY_RAW, columns=["ts", "aum"])
df_full["date"] = pd.to_datetime(df_full["ts"], unit="s")

COMP_RAW = [
    ("open_usd", 698823911), ("usdb", 397020747), ("cash", 255213215),
    ("usd_sui", 159701486), ("path_usd", 131410265), ("squsd", 105481716),
    ("musd", 65532094), ("usdcbl", 57176284), ("mgusd", 50357793),
    ("usds_arq", 44405175),
]
df_comp = pd.DataFrame(COMP_RAW, columns=["stablecoin", "aum"])

# ── HELPERS ──────────────────────────────────────────────────────────────────

def fmt_usd(v):
    if abs(v) >= 1e9:
        return f"${v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:.1f}K"
    return f"${v:,.0f}"

# ── HEADER ───────────────────────────────────────────────────────────────────

st.markdown("# Open USD (OUSD) — Bridge Stablecoin")
st.caption(
    "Source: Bridge issuance data · "
    "Updated Oct 6, 2026"
)

# ── STAT CARDS ───────────────────────────────────────────────────────────────

latest_aum = df_full["aum"].iloc[-1]
seven_days_ago = df_full[df_full["date"] <= df_full["date"].iloc[-1] - pd.Timedelta(days=7)]["aum"].iloc[-1]
growth_7d = latest_aum - seven_days_ago

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current AUM", fmt_usd(latest_aum))
c2.metric("7-Day Growth", fmt_usd(growth_7d), delta=f"{growth_7d/seven_days_ago*100:,.0f}%")
c3.metric("Bridge Rank", "#1", delta="of 31 stablecoins", delta_color="off")
c4.metric("Peak Daily Inflow", "+$414M", delta="Sep 28 single-day", delta_color="off")

# milestones
st.markdown(
    "**Milestones:**  "
    "`Apr 26` First issuance (\\$12) · "
    "`Jun 2` \\$800 · "
    "`Aug 8` \\$40K plateau · "
    "`Sep 24` \\$40M mint · "
    "`Sep 30` \\$454M spike · "
    "`Oct 5` **\\$699M** current"
)

st.divider()

# ── AUM FULL HISTORY (LOG) ───────────────────────────────────────────────────

st.subheader("AUM Over Time (log scale)")
st.caption("Log scale because AUM spans 6 orders of magnitude ($12 → $699M)")

fig_log = go.Figure()
fig_log.add_trace(go.Scatter(
    x=df_full["date"], y=df_full["aum"],
    mode="lines", fill="tozeroy",
    line=dict(color=S1, width=2),
    fillcolor="rgba(57,135,229,0.1)",
    hovertemplate="%{x|%b %d}<br><b>$%{y:,.0f}</b><extra></extra>",
))
fig_log.update_layout(
    **PLOT_LAYOUT,
    xaxis=DEFAULT_AXIS,
    yaxis=dict(type="log", gridcolor=GRID, showgrid=True, zeroline=False,
               tickvals=[100, 1000, 10000, 100000, 1e6, 1e7, 1e8, 1e9],
               ticktext=["$100", "$1K", "$10K", "$100K", "$1M", "$10M", "$100M", "$1B"]),
    height=360,
)
# annotations for key moments
for label, ts, aum in [("$12", 1777334400, 12), ("$40M", 1790121600, 40006013), ("$699M", 1791244800, 698823911)]:
    fig_log.add_annotation(
        x=datetime.utcfromtimestamp(ts), y=aum,
        text=f"<b>{label}</b>", showarrow=True,
        arrowhead=0, arrowcolor=MUTED, arrowwidth=1,
        ax=0, ay=-30, font=dict(color="#ffffff", size=11),
        bgcolor="#2c2c2b", bordercolor=GRID, borderpad=3,
    )
st.plotly_chart(fig_log, use_container_width=True)

# ── LAST 30 DAYS + DAILY CHANGE ─────────────────────────────────────────────

col_l, col_r = st.columns(2)

with col_l:
    st.subheader("AUM — Last 30 Days (linear)")
    df_30 = df_full[df_full["date"] >= df_full["date"].iloc[-1] - pd.Timedelta(days=30)].copy()
    fig_linear = go.Figure()
    fig_linear.add_trace(go.Scatter(
        x=df_30["date"], y=df_30["aum"],
        mode="lines", fill="tozeroy",
        line=dict(color=S1, width=2),
        fillcolor="rgba(57,135,229,0.1)",
        hovertemplate="%{x|%b %d}<br><b>$%{y:,.0f}</b><extra></extra>",
    ))
    fig_linear.update_layout(**PLOT_LAYOUT, height=320,
                             xaxis=DEFAULT_AXIS, yaxis=DEFAULT_AXIS)
    st.plotly_chart(fig_linear, use_container_width=True)

with col_r:
    st.subheader("Daily AUM Change")
    df_change = df_30.copy()
    df_change["daily_change"] = df_change["aum"].diff()
    df_change = df_change.dropna()
    colors = [S3 if v >= 0 else S2 for v in df_change["daily_change"]]
    fig_change = go.Figure()
    fig_change.add_trace(go.Bar(
        x=df_change["date"], y=df_change["daily_change"],
        marker_color=colors,
        hovertemplate="%{x|%b %d}<br><b>%{y:+,.0f}</b><extra></extra>",
    ))
    fig_change.update_layout(**PLOT_LAYOUT, height=320,
                             xaxis=DEFAULT_AXIS,
                             yaxis=dict(gridcolor=GRID, showgrid=True, zeroline=True,
                                        zerolinecolor=GRID))
    st.plotly_chart(fig_change, use_container_width=True)

# ── COMPARISON + GROWTH PHASES ───────────────────────────────────────────────

col_l2, col_r2 = st.columns(2)

with col_l2:
    st.subheader("Bridge Stablecoin Comparison")
    st.caption("Latest AUM across all Bridge-issued stablecoins")
    df_comp_sorted = df_comp.sort_values("aum", ascending=True)
    bar_colors = [S1 if s == "open_usd" else MUTED for s in df_comp_sorted["stablecoin"]]
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        y=df_comp_sorted["stablecoin"],
        x=df_comp_sorted["aum"],
        orientation="h",
        marker_color=bar_colors,
        text=[fmt_usd(v) for v in df_comp_sorted["aum"]],
        textposition="outside",
        textfont=dict(color="#c3c2b7", size=11),
        hovertemplate="%{y}<br><b>$%{x:,.0f}</b><extra></extra>",
    ))
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c3c2b7", size=12),
        hoverlabel=dict(bgcolor="#2c2c2b", font_color="#ffffff", bordercolor="#333332"),
        hovermode="x unified", height=380,
        xaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False, showticklabels=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False),
        margin=dict(l=10, r=80, t=10, b=10),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

with col_r2:
    st.subheader("Growth Phases")
    phases = pd.DataFrame([
        {"phase": "Phase 1: Seed (Apr–Jun)", "aum": 1200},
        {"phase": "Phase 2: Early Adoption (Jun–Sep 21)", "aum": 41000},
        {"phase": "Phase 3: First Major Mint (Sep 22–27)", "aum": 40006013},
        {"phase": "Phase 4: Hypergrowth (Sep 28–now)", "aum": 698823911},
    ])
    phase_colors = [MUTED, S3, S2, S1]
    fig_phases = go.Figure()
    fig_phases.add_trace(go.Bar(
        y=phases["phase"],
        x=phases["aum"],
        orientation="h",
        marker_color=phase_colors,
        text=[fmt_usd(v) for v in phases["aum"]],
        textposition="outside",
        textfont=dict(color="#c3c2b7", size=12),
        hovertemplate="%{y}<br><b>$%{x:,.0f}</b><extra></extra>",
    ))
    fig_phases.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c3c2b7", size=12),
        hoverlabel=dict(bgcolor="#2c2c2b", font_color="#ffffff", bordercolor="#333332"),
        hovermode="x unified", height=280,
        xaxis=dict(type="log", gridcolor=GRID, showgrid=True, zeroline=False, showticklabels=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", showgrid=False, autorange="reversed"),
        margin=dict(l=10, r=80, t=10, b=10),
    )
    st.plotly_chart(fig_phases, use_container_width=True)

    st.markdown("""
    | Phase | Period | Peak AUM | Catalyst |
    |-------|--------|----------|----------|
    | 1 | Apr–Jun | $1.2K | Seed / testing |
    | 2 | Jun–Sep 21 | $41K | Early merchant adoption |
    | 3 | Sep 22–27 | $40M | First major mint |
    | 4 | Sep 28+ | **$699M** | Hypergrowth |
    """)

st.divider()
st.caption("Data: Bridge issuance metrics · Dashboard built Oct 6, 2026")
