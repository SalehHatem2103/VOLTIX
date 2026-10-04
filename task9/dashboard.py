import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ------------------------------------------------------------------ data
SRC = os.environ.get("CUSTOMERS_CSV", r"D:\data analysis\VOLTIX\task9\Customers_cleaned.csv")
df = pd.read_csv(SRC, parse_dates=["PurchaseDate"])
df["Month"] = df["PurchaseDate"].dt.to_period("M").dt.to_timestamp()
df["MonthNum"] = df["PurchaseDate"].dt.month

AGE_ORDER = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ------------------------------------------------------------------ palette
BG, CARD, BORDER = "#03071e", "#370617", "#6a040f"
C1, C2, C3, C4, C5, C6 = "#9d0208", "#d00000", "#dc2f02", "#e85d04", "#f48c06", "#faa307"
GOLD = "#ffba08"
TEXT, MUTED = "#fff3e0", "#f4c98a"
SEQ = [GOLD, C6, C5, C4, C3, C2, C1]

FONT = "Segoe UI, Arial, sans-serif"


def style(fig, title, h=330):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=GOLD)),
        paper_bgcolor=CARD, plot_bgcolor=CARD, height=h,
        font=dict(color=TEXT, family=FONT),
        margin=dict(l=50, r=20, t=55, b=45),
        legend=dict(font=dict(color=TEXT)),
    )
    fig.update_xaxes(gridcolor=BORDER, linecolor=BORDER, zeroline=False)
    fig.update_yaxes(gridcolor=BORDER, linecolor=BORDER, zeroline=False)
    return fig


def empty(title):
    fig = go.Figure()
    fig.add_annotation(text="No data for the selected filters", showarrow=False,
                       font=dict(color=MUTED, size=14))
    return style(fig, title)


# ------------------------------------------------------------------ layout
def kpi(id_, label):
    return html.Div([
        html.Div(label, style={"color": MUTED, "fontSize": "13px", "letterSpacing": "1px",
                               "textTransform": "uppercase"}),
        html.Div(id=id_, style={"color": GOLD, "fontSize": "30px", "fontWeight": "700",
                                "marginTop": "6px"}),
    ], style={"background": CARD, "border": f"1px solid {BORDER}", "borderLeft": f"5px solid {C3}",
              "borderRadius": "10px", "padding": "16px 20px", "flex": "1", "minWidth": "170px"})


def dd(id_, label, options):
    return html.Div([
        html.Label(label, style={"color": MUTED, "fontSize": "12px", "marginBottom": "4px",
                                 "display": "block"}),
        dcc.Dropdown(id=id_, options=[{"label": "All", "value": "All"}] +
                     [{"label": str(o), "value": o} for o in options],
                     value="All", clearable=False, style={"color": "#000"}),
    ], style={"flex": "1", "minWidth": "180px"})


def box(*children):
    return html.Div(list(children), style={"background": CARD, "border": f"1px solid {BORDER}",
                                           "borderRadius": "10px", "padding": "6px", "flex": "1",
                                           "minWidth": "380px"})


app = Dash(__name__)
app.title = "Customer Analysis Dashboard"

app.layout = html.Div(style={"background": BG, "minHeight": "100vh", "padding": "24px",
                             "fontFamily": FONT, "color": TEXT}, children=[
    html.Div([
        html.H1("Customer Data Analysis Dashboard",
                style={"color": GOLD, "margin": "0", "fontSize": "30px"}),
        html.Div("Task 9 | Purchases, Demographics, Categories, Ratings & Trends",
                 style={"color": MUTED, "marginTop": "4px"}),
    ], style={"borderBottom": f"3px solid {C3}", "paddingBottom": "14px", "marginBottom": "18px"}),

    html.Div([
        dd("f-gender", "Gender", sorted(df["Gender"].dropna().unique())),
        dd("f-cat", "Product Category", sorted(df["ProductCategory"].dropna().unique())),
        dd("f-year", "Year", sorted(df["Year"].dropna().astype(int).unique())),
        dd("f-age", "Age Group", AGE_ORDER),
    ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "18px"}),

    html.Div([
        kpi("k-cust", "Total Customers"),
        kpi("k-rev", "Total Revenue"),
        kpi("k-avg", "Avg Purchase"),
        kpi("k-rate", "Avg Rating"),
        kpi("k-top", "Top Category"),
    ], style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "18px"}),

    html.Div([box(dcc.Graph(id="g-trend")), ],
             style={"display": "flex", "gap": "14px", "marginBottom": "14px"}),
    html.Div([box(dcc.Graph(id="g-cat")), box(dcc.Graph(id="g-season"))],
             style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),
    html.Div([box(dcc.Graph(id="g-gender")), box(dcc.Graph(id="g-age"))],
             style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),
    html.Div([box(dcc.Graph(id="g-rating")), box(dcc.Graph(id="g-catrate"))],
             style={"display": "flex", "gap": "14px", "flexWrap": "wrap", "marginBottom": "14px"}),

    html.Div([
        html.H3("Key Insights", style={"color": GOLD, "marginTop": "0"}),
        html.Ul(id="insights", style={"lineHeight": "1.9", "margin": "0", "paddingLeft": "20px"}),
        html.Div("Note: rows with missing Category, Amount, Rating or invalid Date are excluded "
                 "from the related charts only.",
                 style={"color": MUTED, "fontSize": "12px", "marginTop": "12px"}),
    ], style={"background": CARD, "border": f"1px solid {BORDER}", "borderLeft": f"5px solid {C4}",
              "borderRadius": "10px", "padding": "18px 24px"}),
])


# ------------------------------------------------------------------ callback
@app.callback(
    [Output("k-cust", "children"), Output("k-rev", "children"), Output("k-avg", "children"),
     Output("k-rate", "children"), Output("k-top", "children"),
     Output("g-trend", "figure"), Output("g-cat", "figure"), Output("g-season", "figure"),
     Output("g-gender", "figure"), Output("g-age", "figure"), Output("g-rating", "figure"),
     Output("g-catrate", "figure"), Output("insights", "children")],
    [Input("f-gender", "value"), Input("f-cat", "value"),
     Input("f-year", "value"), Input("f-age", "value")],
)
def update(gender, cat, year, age):
    d = df.copy()
    if gender != "All":
        d = d[d["Gender"] == gender]
    if cat != "All":
        d = d[d["ProductCategory"] == cat]
    if year != "All":
        d = d[d["Year"] == year]
    if age != "All":
        d = d[d["AgeGroup"] == age]

    # ---- KPIs
    revenue = d["PurchaseAmount"].sum()
    avg_amt = d["PurchaseAmount"].mean()
    avg_rate = d["Rating"].mean()
    by_cat = d.dropna(subset=["ProductCategory", "PurchaseAmount"]) \
              .groupby("ProductCategory")["PurchaseAmount"].sum().sort_values(ascending=False)
    top_cat = by_cat.index[0] if len(by_cat) else "-"
    k = [f"{d['CustomerID'].nunique():,}", f"${revenue:,.0f}",
         f"${avg_amt:,.2f}" if pd.notna(avg_amt) else "-",
         f"{avg_rate:.2f} / 5" if pd.notna(avg_rate) else "-", top_cat]

    # ---- 1. monthly trend
    t = d.dropna(subset=["Month", "PurchaseAmount"]).groupby("Month")["PurchaseAmount"].sum()
    if len(t):
        fig_t = go.Figure(go.Scatter(x=t.index, y=t.values, mode="lines+markers",
                                     line=dict(color=C5, width=3), marker=dict(color=GOLD, size=7),
                                     fill="tozeroy", fillcolor="rgba(220,47,2,0.18)"))
        fig_t.update_yaxes(title="Revenue ($)")
        style(fig_t, "Monthly Revenue Trend", 340)
    else:
        fig_t = empty("Monthly Revenue Trend")

    # ---- 2. revenue by category
    if len(by_cat):
        fig_c = go.Figure(go.Bar(x=by_cat.index, y=by_cat.values, marker_color=SEQ[:len(by_cat)],
                                 text=[f"${v:,.0f}" for v in by_cat.values], textposition="outside"))
        fig_c.update_yaxes(title="Revenue ($)")
        style(fig_c, "Revenue by Product Category")
    else:
        fig_c = empty("Revenue by Product Category")

    # ---- 3. seasonality (calendar month)
    s = d.dropna(subset=["MonthNum", "PurchaseAmount"]).groupby("MonthNum")["PurchaseAmount"].sum() \
         .reindex(range(1, 13))
    if s.notna().any():
        peak = s.idxmax()
        fig_s = go.Figure(go.Bar(x=MONTH_NAMES, y=s.values,
                                 marker_color=[GOLD if m == peak else C3 for m in range(1, 13)]))
        fig_s.update_yaxes(title="Revenue ($)")
        style(fig_s, "Seasonality - Revenue by Calendar Month")
    else:
        fig_s = empty("Seasonality - Revenue by Calendar Month")

    # ---- 4. gender donut
    g = d["Gender"].value_counts()
    if len(g):
        fig_g = go.Figure(go.Pie(labels=g.index, values=g.values, hole=0.55,
                                 marker=dict(colors=[C3, GOLD, C5], line=dict(color=BG, width=2)),
                                 textinfo="label+percent"))
        style(fig_g, "Customers by Gender")
    else:
        fig_g = empty("Customers by Gender")

    # ---- 5. age group: customers + avg purchase
    a = d.groupby("AgeGroup").agg(n=("CustomerID", "count"), avg=("PurchaseAmount", "mean")) \
         .reindex(AGE_ORDER).dropna(subset=["n"])
    if len(a):
        fig_a = go.Figure()
        fig_a.add_bar(x=a.index, y=a["n"], name="Customers", marker_color=C4)
        fig_a.add_trace(go.Scatter(x=a.index, y=a["avg"], name="Avg Purchase ($)", yaxis="y2",
                                   mode="lines+markers", line=dict(color=GOLD, width=3),
                                   marker=dict(size=8)))
        fig_a.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False,
                                        title="Avg Purchase ($)", rangemode="tozero"),
                            legend=dict(orientation="h", y=1.12, x=0))
        fig_a.update_yaxes(title="Customers", selector=dict(overlaying=None))
        style(fig_a, "Age Group - Customers & Avg Purchase")
    else:
        fig_a = empty("Age Group - Customers & Avg Purchase")

    # ---- 6. rating distribution
    r = d["Rating"].dropna().astype(int).value_counts().reindex(range(1, 6), fill_value=0)
    if r.sum():
        fig_r = go.Figure(go.Bar(x=[f"{i} star" for i in r.index], y=r.values,
                                 marker_color=[C1, C2, C4, C5, GOLD],
                                 text=r.values, textposition="outside"))
        fig_r.update_yaxes(title="Count")
        style(fig_r, "Rating Distribution")
    else:
        fig_r = empty("Rating Distribution")

    # ---- 7. avg rating by category
    cr = d.dropna(subset=["ProductCategory", "Rating"]).groupby("ProductCategory")["Rating"] \
          .mean().sort_values()
    if len(cr):
        fig_cr = go.Figure(go.Bar(x=cr.values, y=cr.index, orientation="h",
                                  marker_color=SEQ[:len(cr)][::-1],
                                  text=[f"{v:.2f}" for v in cr.values], textposition="outside"))
        fig_cr.update_xaxes(range=[0, 5], title="Avg Rating")
        style(fig_cr, "Average Rating by Category")
    else:
        fig_cr = empty("Average Rating by Category")

    # ---- insights (react to the filters)
    ins = []
    if len(by_cat) > 1:
        share = by_cat.iloc[0] / by_cat.sum() * 100
        ins.append(f"{by_cat.index[0]} is the top category with ${by_cat.iloc[0]:,.0f} "
                   f"({share:.1f}% of categorised revenue); {by_cat.index[-1]} is the lowest.")
    if len(a):
        ins.append(f"The {a['n'].idxmax()} age group has the most customers ({int(a['n'].max())}); "
                   f"{a['avg'].idxmax()} has the highest average purchase (${a['avg'].max():,.0f}).")
    if len(g) > 1:
        ins.append(f"{g.index[0]} customers are {g.iloc[0] / g.sum() * 100:.1f}% of the selection.")
    if s.notna().any():
        ins.append(f"Revenue peaks in {MONTH_NAMES[int(s.idxmax()) - 1]} and is weakest in "
                   f"{MONTH_NAMES[int(s.idxmin()) - 1]}.")
    if r.sum():
        pos = r.loc[4:].sum() / r.sum() * 100
        ins.append(f"Only {pos:.1f}% of ratings are 4-5 stars; ratings are spread almost evenly "
                   f"across 1-5 (avg {avg_rate:.2f}).")
    if not ins:
        ins = ["No data for the selected filters."]
    return (*k, fig_t, fig_c, fig_s, fig_g, fig_a, fig_r, fig_cr, [html.Li(i) for i in ins])


if __name__ == "__main__":
    app.run(debug=False)
