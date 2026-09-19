import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# ---------- Data ----------
df = pd.read_csv("File_3_cleaned.csv")

app = Dash(__name__)
app.title = "Titanic Dashboard"

COLORS = {
    "bg": "#eef6fb",
    "card": "#ffffff",
    "navy": "#023047",
    "muted": "#51677a",
    "accent": "#219ebc",
    "accent_light": "#8ecae6",
    "warning": "#ffb703",
    "danger": "#fb8500",
    "success": "#219ebc",
    "border": "#d6e9f2",
}

TEMPLATE = "plotly_white"
FONT = "Poppins, Segoe UI, Arial, sans-serif"

pclass_options = [{"label": f"Class {p}", "value": p} for p in sorted(df["Pclass"].unique())]
embarked_map = {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}
embarked_options = [{"label": embarked_map.get(e, e), "value": e} for e in sorted(df["Embarked"].dropna().unique())]

# ---------- Custom HTML shell (fonts + small CSS touches) ----------
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; }
            body { margin: 0; font-family: 'Poppins', sans-serif; background-color: """ + COLORS["bg"] + """; }
            .kpi-card:hover, .chart-card:hover { box-shadow: 0 6px 18px rgba(15, 23, 42, 0.12) !important; transform: translateY(-2px); }
            .kpi-card, .chart-card { transition: all 0.18s ease-in-out; }
            .Select-control, .dash-dropdown .Select-control { border-radius: 8px !important; }
            ::-webkit-scrollbar { height: 8px; width: 8px; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 8px; }
            @media (max-width: 900px) {
                .charts-grid { grid-template-columns: 1fr !important; }
                .main-row { flex-direction: column !important; padding: 16px !important; gap: 16px !important; }
                .sidebar { width: 100% !important; }
            }
            @media (max-width: 600px) {
                .header-bar { padding: 16px 18px !important; }
                .header-title { font-size: 18px !important; }
                .header-subtitle { display: none; }
                .kpi-row { gap: 10px !important; }
                .kpi-card { min-width: 100% !important; }
                .chart-card { padding: 8px !important; }
                .main-row { padding: 12px !important; }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ---------- Reusable components ----------
def kpi_card(title, value, accent):
    return html.Div(
        className="kpi-card",
        style={
            "flex": "1", "minWidth": "180px", "backgroundColor": COLORS["card"],
            "borderRadius": "14px", "padding": "18px 20px",
            "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.08)",
            "borderLeft": f"4px solid {accent}",
        },
        children=[
            html.Div(title, style={"fontSize": "13px", "color": COLORS["muted"], "fontWeight": "500"}),
            html.Div(value, style={"fontSize": "24px", "fontWeight": "700", "color": COLORS["navy"]}),
        ],
    )


def chart_card(graph_id):
    return html.Div(
        className="chart-card",
        style={
            "backgroundColor": COLORS["card"], "borderRadius": "14px", "padding": "14px",
            "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.08)",
        },
        children=dcc.Graph(id=graph_id, config={"displaylogo": False, "responsive": True}),
    )


def filter_block(label, dropdown_id, options):
    return html.Div(
        style={"display": "flex", "flexDirection": "column", "gap": "6px", "width": "100%", "marginBottom": "18px"},
        children=[
            html.Label(label, style={"fontSize": "13px", "fontWeight": "600", "color": COLORS["muted"]}),
            dcc.Dropdown(
                id=dropdown_id, options=options,
                value=[o["value"] for o in options], multi=True, clearable=False,
                style={"fontFamily": FONT},
            ),
        ],
    )


# ---------- Layout ----------
app.layout = html.Div(
    style={"fontFamily": FONT, "minHeight": "100vh", "backgroundColor": COLORS["bg"]},
    children=[
        # Header
        html.Div(
            className="header-bar",
            style={
                "backgroundColor": COLORS["navy"], "padding": "22px 32px",
                "display": "flex", "alignItems": "center", "gap": "12px",
            },
            children=[
                html.Span("🚢", style={"fontSize": "26px"}),
                html.Div([
                    html.H1("Titanic Passengers Dashboard", className="header-title", style={
                        "color": "#ffffff", "fontSize": "22px", "margin": 0, "fontWeight": "600",
                    }),
                    html.Div("Passenger survival overview & filters", className="header-subtitle", style={
                        "color": "#94a3b8", "fontSize": "13px", "marginTop": "2px",
                    }),
                ]),
            ],
        ),

        html.Div(
            className="main-row",
            style={"padding": "24px 32px", "display": "flex", "gap": "24px", "alignItems": "flex-start"},
            children=[
                # Sidebar — slicers only
                html.Div(
                    className="sidebar",
                    style={
                        "backgroundColor": COLORS["card"], "borderRadius": "14px", "padding": "20px",
                        "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.08)", "width": "260px",
                        "flexShrink": 0,
                    },
                    children=[
                        html.Div("Filters", style={
                            "fontSize": "15px", "fontWeight": "700", "color": COLORS["navy"],
                            "marginBottom": "16px",
                        }),
                        filter_block("Passenger Class", "pclass-filter", pclass_options),
                        filter_block("Port of Embarkation", "embarked-filter", embarked_options),
                    ],
                ),

                # Main content — KPIs + charts
                html.Div(
                    style={"flex": "1", "minWidth": 0},
                    children=[
                        # KPIs
                        html.Div(
                            id="kpi-row",
                            className="kpi-row",
                            style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "22px"},
                        ),

                        # Charts
                        dcc.Loading(
                            type="circle", color=COLORS["accent"],
                            children=html.Div(
                                className="charts-grid",
                                style={
                                    "display": "grid", "gridTemplateColumns": "1fr 1fr",
                                    "gap": "20px",
                                },
                                children=[
                                    chart_card("survival-by-class"),
                                    chart_card("survival-by-sex"),
                                    chart_card("age-distribution"),
                                    chart_card("fare-vs-age"),
                                ],
                            ),
                        ),

                        html.Div(
                            "Data: Titanic passenger dataset · Built with Dash & Plotly",
                            style={"textAlign": "center", "color": COLORS["muted"], "fontSize": "12px", "marginTop": "24px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ---------- Callback ----------
@app.callback(
    Output("kpi-row", "children"),
    Output("survival-by-class", "figure"),
    Output("survival-by-sex", "figure"),
    Output("age-distribution", "figure"),
    Output("fare-vs-age", "figure"),
    Input("pclass-filter", "value"),
    Input("embarked-filter", "value"),
)
def update_dashboard(pclasses, embarked_ports):
    dff = df[df["Pclass"].isin(pclasses) & df["Embarked"].isin(embarked_ports)]
    total_passengers = len(dff)

    kpis = [
        kpi_card("Total Passengers", total_passengers, COLORS["navy"]),
        kpi_card("Survival Rate", f"{dff['Survived'].mean() * 100:.1f}%" if total_passengers else "0%", COLORS["accent"]),
        kpi_card("Average Age", f"{dff['Age'].mean():.1f}" if total_passengers else "-", COLORS["accent_light"]),
        kpi_card("Average Fare", f"${dff['Fare'].mean():.2f}" if total_passengers else "-", COLORS["warning"]),
    ]

    survival_colors = {0: COLORS["danger"], 1: COLORS["success"]}

    fig1 = px.histogram(
        dff, x="Pclass", color="Survived", barmode="group",
        title="Survival Count by Passenger Class",
        labels={"Pclass": "Passenger Class", "count": "Passengers"},
        color_discrete_map=survival_colors, template=TEMPLATE,
    )

    sex_rate = dff.groupby("Sex")["Survived"].mean().reset_index()
    fig2 = px.bar(
        sex_rate, x="Sex", y="Survived", color="Sex",
        title="Survival Rate by Sex", labels={"Survived": "Survival Rate"},
        color_discrete_sequence=[COLORS["accent"], COLORS["warning"]], template=TEMPLATE,
    )
    fig2.update_yaxes(tickformat=".0%")

    fig3 = px.histogram(
        dff, x="Age", nbins=30, title="Age Distribution",
        color_discrete_sequence=[COLORS["accent"]], template=TEMPLATE,
    )

    fig4 = px.scatter(
        dff, x="Age", y="Fare", color="Survived",
        title="Fare vs Age by Survival", color_discrete_map=survival_colors,
        opacity=0.7, template=TEMPLATE,
    )

    for fig in (fig1, fig2, fig3, fig4):
        fig.update_layout(
            margin=dict(l=40, r=20, t=50, b=40),
            font=dict(family=FONT, color=COLORS["navy"]),
            title_font=dict(size=15, family=FONT),
            legend_title_text="",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

    return kpis, fig1, fig2, fig3, fig4


if __name__ == "__main__":
    app.run(debug=True)