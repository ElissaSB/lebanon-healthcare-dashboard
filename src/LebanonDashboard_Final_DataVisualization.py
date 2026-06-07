"""
Lebanon & Region Dashboard — Python/Dash version
Run: pip install dash plotly && python path\to\LebanonDashboard_Final_DataVisualization.py
Then open http://127.0.0.1:8050 in your browser.
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys

# ── Data ─────────────────────────────────────────────────────────────────────

YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
         2020, 2021, 2022, 2023, 2024]

COUNTRIES = ["Lebanon", "Egypt", "France", "Syria", "Turkiye"]

COLORS = {
    "Lebanon": "#1558A8",
    "Egypt":   "#C85200",
    "France":  "#1B7A47",
    "Syria":   "#6B3FA0",
    "Turkiye": "#C0392B",
}

D = {
    "Lebanon": {
        "pop":       [4.23,4.34,4.45,4.55,4.65,5.85,6.0,6.04,6.07,6.09,5.47,5.5,5.49,5.47,5.35],
        "lifeExp":   [77.9,78.1,78.3,78.5,78.7,78.6,78.7,78.8,79.0,79.1,78.5,77.8,78.2,77.9,77.1],
        "gdpPC":     [8027,8747,9079,9308,8877,8146,8178,8049,7647,6843,4141,3098,2504,3041,3150],
        "healthGDP": [7.1,7.3,7.5,7.8,7.9,8.0,8.2,8.1,8.5,9.0,8.5,8.3,8.1,8.0,8.0],
        "oop":       [40.0,38.5,37.0,36.5,35.8,34.2,33.8,34.5,35.6,38.0,42.0,48.0,52.0,49.0,35.7],
        "healthPC":  [570,607,682,725,701,651,669,653,650,616,352,257,203,243,246],
        "infantMort":[9.8,9.3,8.9,8.6,8.2,7.9,7.5,7.2,6.9,6.7,7.2,7.4,7.2,6.9,6.8],
        "fertility": [1.55,1.52,1.51,1.51,1.55,1.73,1.8,1.72,1.68,1.62,1.55,1.51,1.48,1.46,1.44],
        "medianAge": [28.5,29.0,29.5,30.0,30.5,29.8,30.2,30.6,31.0,31.4,32.0,32.5,33.0,33.4,33.8],
        "cpi":       [88,95,98,100,101,100,100,101,103,140,800,5200,21000,38000,42000],
        "govtHlth":  [8.5,8.3,8.0,7.8,7.5,7.2,7.0,7.1,7.3,6.8,5.9,5.2,4.8,4.5,4.2],
        "netMig":    [-0.5,15.0,20.0,25.0,22.0,15.0,10.0,8.0,5.0,-8.0,-15.0,-20.0,-18.0,-15.0,-12.5],
        "mLifeExp":  [75.5,75.7,75.9,76.1,76.3,76.2,76.3,76.4,76.6,76.7,76.1,75.5,75.9,75.5,74.8],
        "fLifeExp":  [80.3,80.5,80.7,80.9,81.1,81.0,81.1,81.2,81.4,81.5,80.9,80.1,80.5,80.3,79.4],
        "birthRate": [14.5,14.1,13.7,13.4,13.1,12.8,12.5,12.2,11.9,11.6,11.2,10.9,10.6,10.4,10.2],
        "deathRate": [5.0,5.0,5.1,5.2,5.2,5.3,5.3,5.4,5.5,5.8,6.5,7.0,6.5,6.2,6.0],
    },
    "Egypt": {
        "pop":       [89.2,91.1,93.2,95.3,97.5,99.6,101.6,103.7,105.7,107.6,109.3,111.0,112.6,114.5,116.5],
        "lifeExp":   [69.1,69.2,69.5,69.6,69.9,70.1,70.4,70.7,71.0,71.2,69.8,69.0,71.0,71.6,71.8],
        "gdpPC":     [2455,2591,2996,3026,3133,3307,3271,2395,2485,2963,3511,3827,4233,3457,3338],
        "healthGDP": [4.15,4.36,4.46,4.67,4.77,5.06,5.07,5.35,4.75,4.6,4.15,4.61,4.72,4.88,4.88],
        "oop":       [62.6,60.5,60.9,57.9,55.1,58.8,59.0,56.4,62.6,62.5,59.3,54.9,53.7,57.2,57.2],
        "healthPC":  [102,113,134,141,150,167,166,128,118,136,146,176,200,169,169],
        "infantMort":[23.3,22.4,21.4,20.6,19.8,19.1,18.4,17.7,17.1,16.5,15.9,15.4,14.9,14.6,13.2],
        "fertility": [3.3,3.31,3.4,3.49,3.49,3.5,3.35,3.31,3.02,2.87,2.85,2.75,2.75,2.75,2.74],
        "medianAge": [22.2,22.4,22.5,22.7,22.8,22.9,23.0,23.0,23.2,23.3,23.5,23.6,23.8,24.0,24.3],
        "govtHlth":  [4.36,4.83,4.39,4.16,4.16,5.06,5.06,5.42,4.72,4.82,5.16,6.8,6.76,6.93,6.93],
        "netMig":    [-2.2,1.4,-0.03,1.4,-1.0,-1.9,-0.7,-0.8,0.2,0.1,0.1,0.1,0.1,2.7,1.1],
        "mLifeExp":  [66.7,66.8,67.1,67.3,67.6,67.8,68.2,68.5,68.8,69.0,67.7,67.2,68.8,69.5,69.7],
        "fLifeExp":  [71.5,71.7,71.9,72.1,72.3,72.5,72.8,73.0,73.2,73.4,72.0,70.8,73.2,73.8,74.0],
        "birthRate": [27.5,27.5,28.1,28.6,28.6,28.5,27.0,26.7,25.8,24.5,23.8,23.0,22.5,22.0,21.5],
        "deathRate": [6.1,6.0,6.0,6.0,5.9,5.9,5.8,5.7,5.6,5.6,5.8,5.8,5.8,5.7,5.7],
        "cpi":       [100,102,104,107,110,113,116,120,124,128,132,136,140,145,150],
    },
    "France": {
        "pop":       [65.0,65.3,65.7,66.0,66.3,66.5,66.7,66.9,67.1,67.2,67.4,67.5,67.6,67.8,67.9],
        "lifeExp":   [81.4,81.8,81.7,82.0,82.4,82.1,82.4,82.4,82.7,82.8,82.3,82.3,82.6,82.9,83.0],
        "gdpPC":     [40695,43930,40864,42669,43148,36702,37024,38687,41767,40494,37599,43519,40886,44000,45000],
        "healthGDP": [11.2,11.2,11.3,11.4,11.6,11.5,11.6,11.4,11.1,11.1,12.2,12.2,12.1,11.9,11.9],
        "oop":       [11.4,11.5,11.3,10.2,11.1,11.0,10.7,10.6,10.5,10.6,10.4,10.3,10.2,10.1,10.1],
        "healthPC":  [4568,4910,4633,4855,4996,4221,4284,4429,4636,4600,4500,4700,4800,4900,4900],
        "infantMort":[3.6,3.4,3.5,3.6,3.5,3.6,3.6,3.8,3.8,3.8,4.2,4.0,4.0,4.0,3.9],
        "fertility": [2.02,2.0,1.99,1.97,1.97,1.93,1.89,1.86,1.83,1.8,1.77,1.71,1.63,1.58,1.55],
        "medianAge": [39.0,39.3,39.5,39.8,40.0,40.3,40.5,40.7,41.0,41.2,41.5,41.8,42.0,42.3,42.6],
        "govtHlth":  [13.7,13.8,13.8,14.0,14.1,14.5,15.2,15.2,14.8,14.7,16.0,16.0,15.8,15.5,15.5],
        "netMig":    [0.83,1.1,1.6,1.8,0.81,-0.01,0.24,1.58,1.5,1.5,1.4,1.3,1.2,1.1,1.0],
        "mLifeExp":  [78.0,78.4,78.5,78.7,79.2,78.9,79.3,79.4,79.5,79.5,79.2,79.2,79.4,79.6,79.8],
        "fLifeExp":  [84.7,85.0,84.9,85.1,85.5,85.2,85.4,85.3,85.5,85.7,85.4,85.4,85.7,85.9,86.1],
        "birthRate": [12.7,12.6,12.7,12.1,12.0,11.9,11.9,11.8,11.5,11.4,11.2,11.0,10.8,10.6,10.5],
        "deathRate": [8.5,8.6,8.7,8.8,8.9,8.9,8.9,9.0,9.0,9.1,10.0,9.2,9.2,9.1,9.0],
        "cpi":       [100,102,103,105,106,107,108,110,112,114,116,119,123,126,128],
    },
    "Syria": {
        "pop":       [21.5,18.8,17.5,17.0,17.5,18.0,19.2,19.2,19.6,20.4,21.0,21.6,22.5,23.6,24.7],
        "lifeExp":   [73.8,68.5,64.0,62.0,63.5,63.5,65.2,65.7,67.4,71.0,71.9,72.4,72.8,72.1,72.6],
        "gdpPC":     [2807,1834,1650,1200,1050,800,656,852,1098,1110,572,664,1052,1100,1150],
        "healthGDP": [3.1,4.5,4.8,4.6,4.5,4.2,3.9,3.9,3.9,4.0,3.7,3.5,3.4,2.7,2.7],
        "oop":       [54.0,55.0,58.0,59.0,55.0,52.0,45.0,43.8,43.1,41.7,48.3,59.5,59.9,72.4,72.4],
        "healthPC":  [87,83,79,70,63,56,26,33,43,44,21,23,36,30,30],
        "infantMort":[20.4,20.0,19.6,19.3,18.9,18.5,20.4,20.7,20.6,17.7,16.7,16.2,16.2,16.7,15.5],
        "fertility": [3.1,3.0,2.95,2.9,2.85,2.9,3.0,3.0,2.93,2.88,2.84,2.8,2.75,2.71,2.7],
        "medianAge": [18.0,17.5,17.2,17.0,17.2,17.5,18.4,18.6,19.1,19.8,20.4,21.0,21.6,22.2,22.8],
        "govtHlth":  [6.0,8.0,9.0,9.1,9.0,8.8,8.3,8.9,8.5,9.1,10.0,7.7,7.9,7.7,7.7],
        "netMig":    [-2.0,-35.0,-45.0,-50.0,-40.0,-25.0,-6.5,-15.0,26.3,24.6,12.8,9.8,32.7,32.1,22.2],
        "mLifeExp":  [70.2,64.0,57.5,55.0,57.5,57.5,59.5,60.3,63.0,67.8,69.2,70.2,70.4,69.8,70.2],
        "fLifeExp":  [77.4,73.0,70.5,69.0,69.5,69.5,71.9,71.9,72.2,74.3,74.8,74.6,75.2,74.4,74.9],
        "birthRate": [30.0,28.0,25.0,23.0,24.0,24.0,25.0,25.0,24.0,23.0,22.5,22.0,21.5,21.0,20.5],
        "deathRate": [6.0,8.0,10.0,12.0,10.0,9.0,8.0,8.0,7.5,7.0,6.8,6.5,6.5,6.5,6.5],
        "cpi":       [100,105,115,130,145,160,175,185,195,210,240,280,340,400,460],
    },
    "Turkiye": {
        "pop":       [73.1,74.2,75.2,76.1,77.2,78.2,79.3,80.3,81.4,82.6,83.4,84.1,85.0,85.3,85.5],
        "lifeExp":   [75.0,74.8,75.6,76.2,76.5,76.5,76.6,77.0,77.5,77.7,76.5,75.7,77.6,77.2,77.4],
        "gdpPC":     [10699,11374,11777,12636,12209,11065,10984,10756,9684,9395,8798,9982,10898,13375,15893],
        "healthGDP": [5.02,4.65,4.44,4.37,4.33,4.12,4.28,4.18,4.12,4.36,4.62,4.56,3.7,4.28,4.28],
        "oop":       [16.9,15.9,15.9,16.9,17.7,16.9,16.5,17.4,17.5,17.0,16.4,16.3,19.5,19.0,19.0],
        "healthPC":  [537,529,523,552,528,456,471,450,399,410,406,455,404,572,572],
        "infantMort":[15.3,14.3,13.5,12.7,12.0,11.4,10.8,10.3,9.8,9.4,9.0,8.5,8.2,9.2,9.6],
        "fertility": [2.08,2.05,2.11,2.11,2.19,2.16,2.12,2.08,2.0,1.89,1.77,1.71,1.63,1.63,1.62],
        "medianAge": [28.1,28.5,28.8,29.1,29.4,29.6,29.9,30.2,30.5,30.8,31.2,31.7,32.1,32.5,33.0],
        "govtHlth":  [11.0,11.2,10.3,10.2,10.3,9.9,9.9,10.0,9.3,9.5,10.5,11.5,10.2,9.8,9.8],
        "netMig":    [0.76,0.93,3.44,5.74,13.24,13.29,4.31,7.94,2.22,-0.18,0.44,0.23,-3.46,-3.65,-3.16],
        "mLifeExp":  [71.9,71.8,72.5,73.1,73.4,73.5,73.5,74.0,74.4,74.7,73.4,72.7,74.7,74.5,74.6],
        "fLifeExp":  [78.2,78.1,78.8,79.4,79.6,79.7,79.9,80.3,80.6,80.9,79.9,79.0,80.7,79.9,80.3],
        "birthRate": [17.5,17.2,17.3,17.2,17.4,17.2,17.0,16.8,16.5,16.2,15.8,15.4,15.0,14.8,14.5],
        "deathRate": [5.5,5.4,5.3,5.3,5.2,5.2,5.1,5.1,5.0,5.0,6.0,5.3,5.5,5.4,5.3],
        "cpi":       [100,106,110,116,122,130,140,153,168,188,212,248,310,390,480],
    },
}

METRIC_LABELS = {
    "healthGDP":  "Health Exp % GDP",
    "oop":        "Out-of-Pocket %",
    "healthPC":   "Health Exp / Capita (USD)",
    "gdpPC":      "GDP per Capita (USD)",
    "lifeExp":    "Life Expectancy",
    "infantMort": "Infant Mortality",
    "fertility":  "Fertility Rate",
    "medianAge":  "Median Age",
    "govtHlth":   "Govt Health Spending %",
    "birthRate":  "Birth Rate",
    "deathRate":  "Death Rate",
    "pop":        "Population (M)",
    "netMig":     "Net Migration Rate",
    "cpi":        "Medical CPI",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def hex_to_rgba(h, a):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

def fmt_gdp(n):
    return f"${n/1000:.1f}K" if n >= 10000 else f"${round(n):,}"

def fmt_pct(n):
    return f"{n:.1f}%"

BASE_LAYOUT = dict(
    paper_bgcolor="#fff",
    plot_bgcolor="#fff",
    font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
    margin=dict(l=58, r=25, t=24, b=48),
    hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                    font=dict(color="#fff", size=12)),
    legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)",
                font=dict(size=11)),
    xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
               tickfont=dict(color="#566B80")),
    yaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
               tickfont=dict(color="#566B80")),
)

def base(**overrides):
    import copy
    b = copy.deepcopy(BASE_LAYOUT)
    b.update(overrides)
    return b

def vline(yi):
    return dict(type="line", xref="x", yref="paper",
                x0=YEARS[yi], x1=YEARS[yi], y0=0, y1=1,
                line=dict(color="rgba(30,42,58,.30)", width=1.2, dash="dot"))

def crisis(yi):
    return dict(type="rect", xref="x", yref="paper",
                x0=2019, x1=YEARS[yi], y0=0, y1=1,
                fillcolor="rgba(21,88,168,.05)",
                line=dict(width=0), layer="below")

def norm_vals(vals, invert=False):
    mn, mx = min(vals), max(vals)
    span = mx - mn or 1
    result = [(v - mn) / span * 100 for v in vals]
    return [100 - n for n in result] if invert else result

def norm_country(c, field, yi, invert=False):
    vals = [D[cc][field][yi] for cc in COUNTRIES]
    mn, mx = min(vals), max(vals)
    span = mx - mn or 1
    n = (D[c][field][yi] - mn) / span * 100
    return 100 - n if invert else n

def prev_delta(c, field, yi):
    if yi == 0:
        return ""
    a, b_ = D[c][field][yi], D[c][field][yi - 1]
    d = a - b_
    pc = abs(d / b_ * 100) if b_ else 0
    arrow = "▲" if d >= 0 else "▼"
    cls = "green" if d >= 0 else "red"
    return (arrow, f"{pc:.1f}%", cls)

# ── App Layout ────────────────────────────────────────────────────────────────

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Lebanon & Region Dashboard"

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * { outline: none !important; }
            *:focus { outline: none !important; }
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
'''

TABS = [
    ("p1", "Regional Overview"),
    ("p2", "Lebanon in Crisis"),
    ("p3", "Healthcare Expenditure"),
    ("p4", "Demographics"),
    ("p5", "Economy & Affordability"),
    ("p6", "Indicator Comparison"),
]

def pill_button(c, active=False):
    color = COLORS[c]
    style = {
        "border": f"1.5px solid {color}",
        "padding": "5px 11px",
        "borderRadius": "999px",
        "fontSize": "11px",
        "fontWeight": "800",
        "background": color if active else "white",
        "color": "white" if active else color,
        "cursor": "pointer",
        "fontFamily": "Inter, Arial, sans-serif",
    }
    return html.Button(c, id=f"pill_{c}", n_clicks=0, style=style)

app.layout = html.Div(style={"margin": 0, "background": "#fff",
                              "color": "#1E2A3A",
                              "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif"}, children=[

    # ── Top bar ──
    html.Div(style={"position": "sticky", "top": 0, "zIndex": 50,
                    "background": "rgba(255,255,255,.98)",
                    "borderBottom": "1px solid #C8D6E5"}, children=[
        html.Div(style={"display": "flex", "alignItems": "flex-end", "gap": 14,
                        "padding": "14px 30px 6px"}, children=[
            html.H1([html.Span("Lebanon", style={"color": "#1558A8"}), " & Region"],
                    style={"fontSize": 17, "margin": 0, "fontWeight": 850, "letterSpacing": "-.5px"}),

        ]),
        html.Div(style={"display": "flex", "gap": 10, "padding": "0 30px", "overflowX": "auto"}, children=[
            html.Button(label, id=f"tab_{pid}", n_clicks=0,
                        style={"border": 0, "background": "transparent",
                               "color": "#1E2A3A" if i == 0 else "#4A6478",
                               "fontWeight": 650, "fontSize": 12,
                               "padding": "11px 14px 12px",
                               "borderBottom": f"3px solid {'#1558A8' if i == 0 else 'transparent'}",
                               "cursor": "pointer", "whiteSpace": "nowrap",
                               "fontFamily": "Inter, Arial, sans-serif"})
            for i, (pid, label) in enumerate(TABS)
        ]),
    ]),

    # ── Controls bar ──
    html.Div(style={"position": "sticky", "top": 72, "zIndex": 45,
                    "background": "rgba(255,255,255,.98)",
                    "borderBottom": "1px solid #C8D6E5",
                    "padding": "7px 30px"}, children=[
        html.Div(style={"background": "white", "border": "1px solid #C8D6E5",
                        "borderRadius": 14,
                        "boxShadow": "0 4px 14px rgba(30,42,58,.06)",
                        "padding": "8px 18px",
                        "display": "grid",
                        "gridTemplateColumns": "1.25fr .9fr",
                        "gap": 16, "alignItems": "center"}, children=[
            html.Div([
                html.Div("Year",
                         style={"fontSize": 9, "textTransform": "uppercase",
                                "letterSpacing": ".16em", "fontWeight": 850,
                                "color": "#4A6478", "marginBottom": 6}),
                dcc.Slider(
                    id="year-slider",
                    min=0,
                    max=len(YEARS) - 1,
                    step=1,
                    value=14,
                    marks={i: str(y) for i, y in enumerate(YEARS)},
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ]),
            html.Div(id="pills-area", children=[
                html.Div("Country",
                         id="pills-label",
                         style={"fontSize": 9, "textTransform": "uppercase",
                                "letterSpacing": ".16em", "fontWeight": 850,
                                "color": "#4A6478", "marginBottom": 4}),
                html.Div(id="pills-container",
                         style={"display": "flex", "gap": 7, "flexWrap": "wrap"},
                         children=[pill_button(c, c == "Lebanon") for c in COUNTRIES]),
            ]),
        ]),
    ]),

    # ── Hidden stores ──
    dcc.Store(id="store-yi", data=14),
    dcc.Store(id="store-kpi-country", data="Lebanon"),
    dcc.Store(id="store-active-tab", data="p1"),
    dcc.Store(id="store-hm-countries", data=list(COUNTRIES)),

    # ── Main content ──
    html.Main(style={"maxWidth": 1450, "margin": "0 auto", "padding": "22px 30px 48px"}, children=[

        # KPI rows (shared)
        html.Div(id="kpis-area"),

        # Page content
        html.Div(id="page-content"),


    ]),
])

# ── CSS injection via a clientside callback alternative: inline style helpers

CARD_STYLE = {
    "background": "white",
    "border": "1px solid #C8D6E5",
    "borderRadius": 18,
    "padding": "20px 22px",
    "boxShadow": "0 7px 24px rgba(30,42,58,.05)",
    "overflow": "hidden",
}

def card(children, **style_overrides):
    s = {**CARD_STYLE, **style_overrides}
    return html.Div(children, style=s)

def grid(*children, cols="1fr 1fr", gap=16, mb=16):
    return html.Div(list(children), style={
        "display": "grid",
        "gridTemplateColumns": cols,
        "gap": gap,
        "marginBottom": mb,
    })

def chart_div(chart_id, h=332):
    is_map = "map" in str(chart_id).lower()
    return dcc.Graph(
        id=chart_id,
        config={
            "displayModeBar": is_map,
            "scrollZoom": True,
            "responsive": True,
        },
        style={"height": h}
    )

def page_head(title, desc):
    return html.Div([
        html.H2(title, style={"fontSize": 23, "margin": 0, "fontWeight": 850,
                               "letterSpacing": "-.6px", "color": "#1E2A3A"}),
    ], style={"borderLeft": "5px solid #1558A8", "paddingLeft": 14, "margin": "4px 0 18px"})


# ── Page builders ──────────────────────────────────────────────────────────────

def build_page1():
    return html.Div([
        page_head("Regional Overview",
                  "Comparative analysis across health spending, income levels, life expectancy, and financial burden on households."),
        html.Div(id="kpis1", style={"display": "grid", "gridTemplateColumns": "repeat(4,1fr)",
                                     "gap": 14, "marginBottom": 16}),
        grid(
            card([html.H3("Health Expenditure as a Share of GDP", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each country displayed in its own panel, preserving individual trends without visual overlap.",
                         style={"display": "none"}),
                  chart_div("p1_facet", 332)]),
            card([html.H3("Regional Performance Comparison", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("All indicators normalized to a common scale of 0 to 100.",
                         style={"display": "none"}),
                  chart_div("p1_bar", 332)]),
            cols="6fr 4fr"
        ),
        grid(
            card([html.H3("Income and Life Expectancy", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each point represents a country in the selected year.",
                         style={"display": "none"}),
                  chart_div("p1_scatter", 306)]),
            card([html.H3("Country Profiles Across Key Indicators", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each line traces a country across five normalized dimensions.",
                         style={"display": "none"}),
                  chart_div("p1_parallel", 306)]),
        ),
    ])

def build_page2():
    return html.Div([
        page_head("Lebanon in Crisis",
                  "A focused view of Lebanon's economic collapse: medical inflation, GDP deterioration, migration shifts, and the erosion of public health financing."),
        html.Div(id="kpis2", style={"display": "grid", "gridTemplateColumns": "repeat(4,1fr)",
                                     "gap": 14, "marginBottom": 16}),
        grid(
            card([html.H3("Medical Cost Inflation in Lebanon", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Annual change in medical consumer prices.", style={"display": "none"}),
                  chart_div("p2_cpi", 332)]),
            card([html.H3("Lebanon GDP Relative to Regional Peers", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Lebanon's income trajectory set against the regional average.", style={"display": "none"}),
                  chart_div("p2_gdpavg", 332)]),
        ),
        grid(
            card([html.H3("Health Financing Composition Over Time", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Out-of-pocket payments versus government and other sources.", style={"display": "none"}),
                  chart_div("p2_split", 306)]),
            card([html.H3("Population Size and Migration Pressure", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Separate panels to preserve scale integrity.", style={"display": "none"}),
                  chart_div("p2_migration_pop", 148),
                  chart_div("p2_migration_mig", 148)]),
            cols="4fr 6fr"
        ),
    ])

def build_page3():
    return html.Div([
        page_head("Healthcare Expenditure",
                  "Who pays, how much, and how spending has evolved across all countries, with a closer look at Lebanon's hospital infrastructure."),
        html.Div(id="kpis3", style={"display": "grid", "gridTemplateColumns": "repeat(4,1fr)",
                                     "gap": 14, "marginBottom": 16}),
        grid(
            card([html.H3("Health Financing: Out-of-Pocket vs Government", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Countries ranked by out-of-pocket share for the selected year.", style={"display": "none"}),
                  chart_div("p3_finance", 306)]),
            card([html.H3("Health Expenditure per Capita Over Time", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each country presented in its own panel.", style={"display": "none"}),
                  chart_div("p3_facet", 400)]),
        ),
        grid(
            card([html.H3("Hospital Distribution Across Lebanese Governorates", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Click a region on the map or bar to highlight. Color depth reflects hospital concentration.", style={"display": "none"}),
                  chart_div("p3_hospital", 400),
                  ]),
            card([html.H3("Out-of-Pocket Burden by Country", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Countries ranked for the selected year.", style={"display": "none"}),
                  chart_div("p3_oop_rank", 306)]),
        ),
    ])

def build_page4():
    return html.Div([
        page_head("Demographics",
                  "Population dynamics across all countries: fertility, mortality, aging, and gender disparities in life expectancy."),
        html.Div(id="kpis4", style={"display": "grid", "gridTemplateColumns": "repeat(4,1fr)",
                                     "gap": 14, "marginBottom": 16}),
        grid(
            card([html.H3("Population Trends, 2010-2024", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Individual trajectories per country.", style={"display": "none"}),
                  chart_div("p4_pop", 306)]),
            card([html.H3("Demographic Indicators at a Glance", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("All countries compared for the selected year.", style={"display": "none"}),
                  chart_div("p4_heat", 306)]),
        ),
        grid(
            card([html.H3("Life Expectancy by Gender in Lebanon", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Male and female trajectories over time.", style={"display": "none"}),
                  chart_div("p4_gender", 306)]),
            card([html.H3("Birth Rate and Death Rate by Country", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Countries sorted by birth rate for the selected year.", style={"display": "none"}),
                  chart_div("p4_rates", 306)]),
        ),
    ])

def build_page5():
    return html.Div([
        page_head("Economy & Affordability",
                  "Examining health spending capacity, affordability gaps, government commitment, and the relationship between national income and healthcare costs."),
        html.Div(id="kpis5", style={"display": "grid", "gridTemplateColumns": "repeat(4,1fr)",
                                     "gap": 14, "marginBottom": 16}),
        grid(
            card([html.H3("Health Affordability Index", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Health spending per capita expressed as a share of income per capita.", style={"display": "none"}),
                  chart_div("p5_afford", 306)]),
            card([html.H3("Economic Capacity vs Household Health Burden", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("The bar shows out-of-pocket burden; the marker indicates GDP tier.", style={"display": "none"}),
                  chart_div("p5_bullet", 306)]),
        ),
        grid(
            card([html.H3("Government Health Spending: Then and Now", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each line connects 2010 to the selected year.", style={"display": "none"}),
                  chart_div("p5_slope", 306)]),
            card([html.H3("National Income and Health Spending per Person", style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
                  html.P("Each country on its own scale, ordered by income level.", style={"display": "none"}),
                  chart_div("p5_dotplot", 306)]),
        ),
    ])

def build_page6():
    return html.Div([
        page_head("Indicator Comparison",
                  "Select any indicator to compare all countries across the full 2010-2024 period at a glance."),
        card([
            html.H3("Country and Year Comparison by Selected Indicator",
                    style={"fontSize": 16, "margin": "0 0 4px", "fontWeight": 900}),
            html.P("Raw values displayed by country and year. Deeper color indicates higher values.",
                   style={"display": "none"}),
            html.Div([
                html.Div([
                    html.Div("Metric", style={"fontSize": 10, "color": "#4A6478", "fontWeight": 800,
                                              "textTransform": "uppercase", "letterSpacing": ".08em"}),
                    dcc.Dropdown(
                        id="hm-metric",
                        options=[{"label": v, "value": k} for k, v in METRIC_LABELS.items()],
                        value="healthGDP",
                        clearable=False,
                        style={"fontSize": 11, "width": 260},
                    ),
                ]),
            ], style={"display": "flex", "gap": 10, "alignItems": "center",
                      "flexWrap": "wrap", "marginBottom": 10}),
            chart_div("p6_heatmap", 380),
        ], marginBottom=16),
    ])

PAGE_BUILDERS = {
    "p1": build_page1,
    "p2": build_page2,
    "p3": build_page3,
    "p4": build_page4,
    "p5": build_page5,
    "p6": build_page6,
}

# ── Callbacks ──────────────────────────────────────────────────────────────────

# Tab switching
@app.callback(
    Output("store-active-tab", "data"),
    [Input(f"tab_{pid}", "n_clicks") for pid, _ in TABS],
    prevent_initial_call=True,
)
def switch_tab(*args):
    ctx = callback_context
    if not ctx.triggered:
        return "p1"
    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return btn_id.replace("tab_", "")

# Tab visual styles (underline indicator)
@app.callback(
    [Output(f"tab_{pid}", "style") for pid, _ in TABS],
    Input("store-active-tab", "data"),
)
def update_tab_styles(active_tab):
    styles = []
    for pid, _ in TABS:
        is_active = pid == active_tab
        styles.append({
            "border": 0,
            "background": "transparent",
            "color": "#1E2A3A" if is_active else "#4A6478",
            "fontWeight": 650,
            "fontSize": 12,
            "padding": "11px 14px 12px",
            "borderBottom": f"3px solid {'#1558A8' if is_active else 'transparent'}",
            "cursor": "pointer",
            "whiteSpace": "nowrap",
            "fontFamily": "Inter, Arial, sans-serif",
        })
    return styles

# Year slider
@app.callback(
    Output("store-yi", "data"),
    Input("year-slider", "value"),
)
def update_yi(val):
    return val

# KPI country pills
@app.callback(
    Output("store-kpi-country", "data"),
    [Input(f"pill_{c}", "n_clicks") for c in COUNTRIES],
    State("store-kpi-country", "data"),
    State("store-active-tab", "data"),
    prevent_initial_call=True,
)
def pill_click(*args):
    n_clicks_list = args[:5]
    kpi_country = args[5]
    active_tab = args[6]
    ctx = callback_context
    if not ctx.triggered:
        return kpi_country
    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    c = btn_id.replace("pill_", "")
    if active_tab != "p6":
        return c
    return kpi_country

# Update pill visuals — update styles only, never recreate buttons
@app.callback(
    [Output(f"pill_{c}", "style") for c in COUNTRIES],
    Output("pills-label", "children"),
    Input("store-kpi-country", "data"),
    Input("store-active-tab", "data"),
    Input("store-hm-countries", "data"),
)
def update_pills(kpi_c, active_tab, hm_countries):
    is_heatmap = active_tab == "p6"
    label = "Countries" if is_heatmap else "Country"
    styles = []
    for c in COUNTRIES:
        color = COLORS[c]
        active = (c in hm_countries) if is_heatmap else (c == kpi_c)
        styles.append({
            "border": f"1.5px solid {color}",
            "padding": "5px 11px",
            "borderRadius": "999px",
            "fontSize": "11px",
            "fontWeight": "800",
            "background": color if active else "white",
            "color": "white" if active else color,
            "cursor": "pointer",
            "fontFamily": "Inter, Arial, sans-serif",
        })
    return *styles, label

# Country toggles for Indicator Comparison
@app.callback(
    Output("store-hm-countries", "data"),
    [Input(f"pill_{c}", "n_clicks") for c in COUNTRIES],
    State("store-hm-countries", "data"),
    State("store-active-tab", "data"),
    prevent_initial_call=True,
)
def toggle_heatmap_countries(*args):
    current = list(args[5] or COUNTRIES)
    active_tab = args[6]
    ctx = callback_context
    if active_tab != "p6" or not ctx.triggered:
        return current
    c = ctx.triggered[0]["prop_id"].split(".")[0].replace("pill_", "")
    if c in current and len(current) > 1:
        current.remove(c)
    elif c not in current:
        current.append(c)
    return [c for c in COUNTRIES if c in current]

# Render page content
@app.callback(
    Output("page-content", "children"),
    Input("store-active-tab", "data"),
)
def render_page(tab):
    return PAGE_BUILDERS.get(tab, build_page1)()

# ── KPI helpers ────────────────────────────────────────────────────────────────

def kpi_card(label, value, sub, delta_info=None, country="Lebanon", yi=14):
    color = COLORS[country]
    return html.Div([
        html.Div(style={
            "height": 5,
            "background": f"linear-gradient(90deg, {color}, {hex_to_rgba(color, 0.45)})",
            "borderRadius": "16px 16px 0 0",
            "margin": "-17px -20px 14px",
        }),
        html.Div(f"{country} · {YEARS[yi]}",
                 style={"display": "inline-block", "padding": "4px 10px",
                        "borderRadius": "999px",
                        "background": hex_to_rgba(color, .10),
                        "color": color, "fontSize": 10,
                        "textTransform": "uppercase",
                        "letterSpacing": ".08em", "fontWeight": 800,
                        "marginBottom": 8}),
        html.Div(label, style={"color": "#4A6478", "fontSize": 10,
                                "textTransform": "uppercase",
                                "letterSpacing": ".08em", "fontWeight": 650}),
        html.Div(value, style={"fontSize": 25, "fontWeight": 600,
                                "letterSpacing": "-.4px", "marginTop": 7,
                                "lineHeight": 1, "color": "#1E2A3A"}),
        html.Div(sub, style={"color": "#6A8BA4", "fontSize": 11, "marginTop": 7}),
    ], style={"background": "white", "border": f"1px solid {hex_to_rgba(color, 0.35)}",
              "borderRadius": 16, "padding": "17px 20px",
              "minHeight": 108, "boxShadow": f"0 10px 24px {hex_to_rgba(color, 0.08)}",
              "overflow": "hidden"})

def render_kpis(kpi_id, yi, kpi_c):
    d = D[kpi_c]
    lb = D["Lebanon"]
    avg = sum(D[c]["healthPC"][yi] for c in COUNTRIES if c != "Lebanon") / 4

    rows = {
        "kpis1": [
            kpi_card("Population", f"{d['pop'][yi]:.1f}M", "millions", prev_delta(kpi_c, "pop", yi), kpi_c, yi),
            kpi_card("Life Expectancy", f"{d['lifeExp'][yi]:.1f} yrs", "years at birth", prev_delta(kpi_c, "lifeExp", yi), kpi_c, yi),
            kpi_card("GDP per Capita", fmt_gdp(d["gdpPC"][yi]), "USD current", prev_delta(kpi_c, "gdpPC", yi), kpi_c, yi),
            kpi_card("Health Exp % GDP", fmt_pct(d["healthGDP"][yi]), "% of GDP", prev_delta(kpi_c, "healthGDP", yi), kpi_c, yi),
        ],
        "kpis2": [
            kpi_card("Medical CPI", f"{lb['cpi'][yi]:,}", "index", prev_delta("Lebanon", "cpi", yi), "Lebanon", yi),
            kpi_card("GDP vs 2018", f"{(lb['gdpPC'][yi]-lb['gdpPC'][8])/lb['gdpPC'][8]*100:.1f}%", "from 2018 peak", prev_delta("Lebanon", "gdpPC", yi), "Lebanon", yi),
            kpi_card("OOP Burden", fmt_pct(lb["oop"][yi]), "% health exp", prev_delta("Lebanon", "oop", yi), "Lebanon", yi),
            kpi_card("Net Migration", f"{lb['netMig'][yi]:.1f}", "per 1,000", prev_delta("Lebanon", "netMig", yi), "Lebanon", yi),
        ],
        "kpis3": [
            kpi_card("Health Exp / Capita", fmt_gdp(d["healthPC"][yi]), "USD per person", prev_delta(kpi_c, "healthPC", yi), kpi_c, yi),
            kpi_card("Out-of-Pocket %", fmt_pct(d["oop"][yi]), "% health exp", prev_delta(kpi_c, "oop", yi), kpi_c, yi),
            kpi_card("Govt Health Spending", fmt_pct(d["govtHlth"][yi]), "% govt exp", prev_delta(kpi_c, "govtHlth", yi), kpi_c, yi),
            kpi_card("Health Exp % GDP", fmt_pct(d["healthGDP"][yi]), "% GDP", prev_delta(kpi_c, "healthGDP", yi), kpi_c, yi),
        ],
        "kpis4": [
            kpi_card("Population", f"{d['pop'][yi]:.1f}M", "millions", prev_delta(kpi_c, "pop", yi), kpi_c, yi),
            kpi_card("Fertility", f"{d['fertility'][yi]:.1f}", "births/woman", prev_delta(kpi_c, "fertility", yi), kpi_c, yi),
            kpi_card("Infant Mortality", f"{d['infantMort'][yi]:.1f}", "per 1,000", prev_delta(kpi_c, "infantMort", yi), kpi_c, yi),
            kpi_card("Median Age", f"{d['medianAge'][yi]:.1f} yrs", "years", prev_delta(kpi_c, "medianAge", yi), kpi_c, yi),
        ],
        "kpis5": [
            kpi_card("Affordability Index", fmt_pct(d["healthPC"][yi]/d["gdpPC"][yi]*100), "health/cap / GDP/cap", prev_delta(kpi_c, "healthPC", yi), kpi_c, yi),
            kpi_card("OOP Burden", fmt_pct(d["oop"][yi]), "% health exp", prev_delta(kpi_c, "oop", yi), kpi_c, yi),
            kpi_card("Govt Share", fmt_pct(d["govtHlth"][yi]), "% govt exp", prev_delta(kpi_c, "govtHlth", yi), kpi_c, yi),
            kpi_card("Lebanon vs Regional Avg", f"{(D['Lebanon']['healthPC'][yi]-avg)/avg*100:.1f}%", "health spending/cap", prev_delta("Lebanon", "healthPC", yi), "Lebanon", yi),
        ],
    }
    return rows.get(kpi_id, [])

# ── Page-specific callbacks ──────────────────────────────────────────────────

# KPIs
for kid in ["kpis1", "kpis2", "kpis3", "kpis4", "kpis5"]:
    @app.callback(
        Output(kid, "children"),
        Input("store-yi", "data"),
        Input("store-kpi-country", "data"),
        Input("store-active-tab", "data"),
    )
    def _kpis(yi, kpi_c, tab, _kid=kid):
        return render_kpis(_kid, yi, kpi_c)

# ── PAGE 1 charts ──────────────────────────────────────────────────────────────

@app.callback(
    Output("p1_facet", "figure"),
    Output("p1_bar", "figure"),
    Output("p1_scatter", "figure"),
    Output("p1_parallel", "figure"),
    Input("store-yi", "data"),
    Input("store-active-tab", "data"),
)
def render_p1(yi, tab):
    # Facet: all countries on one chart (simplified from original's multi-trace approach)
    traces_facet = []
    for c in COUNTRIES:
        traces_facet.append(go.Scatter(
            x=YEARS, y=D[c]["healthGDP"], name=c,
            mode="lines+markers",
            line=dict(color=COLORS[c], width=2.8 if c == "Lebanon" else 1.8),
            marker=dict(size=8 if c == "Lebanon" else 6),
            hovertemplate=f"<b>{c}</b><br>Year: %{{x}}<br>Health Exp: %{{y:.1f}}%<extra></extra>",
        ))
    fig_facet = go.Figure(traces_facet)
    fig_facet.update_layout(
        **{k: v for k, v in BASE_LAYOUT.items() if k not in ("xaxis", "yaxis", "margin", "legend")},
        height=332, hovermode="x unified",
        margin=dict(l=70, r=25, t=20, b=55),
        legend=dict(orientation="h", x=0.15, y=1.1),
        xaxis=dict(title="Year", showgrid=False, tickangle=-45,
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        yaxis=dict(title="Health Expenditure (% GDP)", gridcolor="#E8EDF3",
                   zeroline=False, tickfont=dict(color="#566B80")),
    )

    # Normalized grouped bar
    metrics_labels = ["GDP/Capita", "Life Expectancy", "Low OOP", "Low Infant Mort"]
    gdp_v = [D[c]["gdpPC"][yi] for c in COUNTRIES]
    life_v = [D[c]["lifeExp"][yi] for c in COUNTRIES]
    oop_v = [D[c]["oop"][yi] for c in COUNTRIES]
    im_v = [D[c]["infantMort"][yi] for c in COUNTRIES]
    nGDP = norm_vals(gdp_v)
    nLife = norm_vals(life_v)
    nOOP = norm_vals(oop_v, True)
    nIM = norm_vals(im_v, True)
    traces_bar = [
        go.Bar(name=c, x=metrics_labels,
               y=[nGDP[i], nLife[i], nOOP[i], nIM[i]],
               marker=dict(color=hex_to_rgba(COLORS[c], .72),
                           line=dict(color=COLORS[c], width=1)),
               hovertemplate=f"<b>{c}</b><br>%{{x}}: %{{y:.0f}}/100<extra></extra>")
        for i, c in enumerate(COUNTRIES)
    ]
    fig_bar = go.Figure(traces_bar)
    fig_bar.update_layout(
        **{k: v for k, v in BASE_LAYOUT.items() if k not in ("xaxis", "yaxis", "margin", "legend")},
        barmode="group",
        xaxis=dict(type="category", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        yaxis=dict(title="Normalized score (0-100)", range=[0, 112],
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.18, x=0, bgcolor="rgba(255,255,255,0)",
                    font=dict(size=11)),
        margin=dict(l=58, r=25, t=24, b=48),
    )

    # Scatter
    traces_scatter = [
        go.Scatter(
            x=[D[c]["gdpPC"][yi]], y=[D[c]["lifeExp"][yi]],
            name=c, text=[c], mode="markers+text", textposition="top center", cliponaxis=False,
            marker=dict(size=11, color=hex_to_rgba(COLORS[c], .72),
                        line=dict(color=COLORS[c], width=2)),
            hovertemplate=f"<b>{c}</b><br>GDP: $%{{x:,.0f}}<br>Life exp: %{{y:.1f}} yrs<br>Pop: {D[c]['pop'][yi]:.1f}M<extra></extra>",
        )
        for c in COUNTRIES
    ]
    fig_scatter = go.Figure(traces_scatter)
    fig_scatter.update_layout(
        **{k: v for k, v in BASE_LAYOUT.items() if k not in ("xaxis", "yaxis", "margin", "legend")},
        showlegend=False,
        xaxis=dict(title="GDP per capita (USD)", tickprefix="$",
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        yaxis=dict(title="Life expectancy (years)", gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        margin=dict(l=70, r=80, t=30, b=58),
    )

    # Parallel (simulated with scatter)
    pc_metrics = ["GDP/Cap", "Life Exp", "Low OOP", "Low Inf Mort", "Med Age"]
    def norm_all(field, invert=False):
        vals = [D[c][field][yi] for c in COUNTRIES]
        mn, mx = min(vals), max(vals)
        span = mx - mn or 1
        result = [(D[c][field][yi] - mn) / span * 100 for c in COUNTRIES]
        return [100 - n for n in result] if invert else result
    gdpN = norm_all("gdpPC")
    lifeN = norm_all("lifeExp")
    oopN = norm_all("oop", True)
    imN = norm_all("infantMort", True)
    ageN = norm_all("medianAge")
    traces_par = [
        go.Scatter(
            x=[0, 1, 2, 3, 4],
            y=[gdpN[i], lifeN[i], oopN[i], imN[i], ageN[i]],
            name=c, mode="lines+markers",
            line=dict(color=COLORS[c], width=4 if c == "Lebanon" else 2.5),
            marker=dict(size=9 if c == "Lebanon" else 6, color=COLORS[c],
                        line=dict(color="#fff", width=1)),
            text=pc_metrics,
            hovertemplate=f"<b>{c}</b><br>%{{text}}: %{{y:.0f}}/100<extra></extra>",
        )
        for i, c in enumerate(COUNTRIES)
    ]
    fig_par = go.Figure(traces_par)
    fig_par.update_layout(
        **{k: v for k, v in BASE_LAYOUT.items() if k not in ("xaxis", "yaxis", "margin", "legend")},
        margin=dict(l=55, r=25, t=40, b=60),
        xaxis=dict(tickmode="array", tickvals=[0, 1, 2, 3, 4],
                   ticktext=pc_metrics, tickfont=dict(size=11),
                   automargin=True, gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5"),
        yaxis=dict(title="Normalized score", range=[-5, 110],
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.2, x=0, font=dict(size=11),
                    bgcolor="rgba(255,255,255,0)"),
    )
    return fig_facet, fig_bar, fig_scatter, fig_par


# ── PAGE 2 ──────────────────────────────────────────────────────────────────

@app.callback(
    Output("p2_cpi", "figure"),
    Output("p2_gdpavg", "figure"),
    Output("p2_split", "figure"),
    Output("p2_migration_pop", "figure"),
    Output("p2_migration_mig", "figure"),
    Input("store-yi", "data"),
    Input("store-active-tab", "data"),
)
def render_p2(yi, tab):
    lb = D["Lebanon"]

    # YoY CPI bar
    yoy = [0] + [(lb["cpi"][i] - lb["cpi"][i - 1]) / lb["cpi"][i - 1] * 100 for i in range(1, 15)]
    crisis_colors = [
        hex_to_rgba(COLORS["Lebanon"], 1) if v > 200 else
        hex_to_rgba(COLORS["Lebanon"], .75) if v > 50 else
        hex_to_rgba(COLORS["Lebanon"], .45)
        for v in yoy
    ]
    fig_cpi = go.Figure(go.Bar(
        x=YEARS, y=yoy,
        marker=dict(color=crisis_colors, line=dict(color=COLORS["Lebanon"], width=1)),
        text=["" if i == 0 else (f"+{v:.0f}%" if v > 1 else "") for i, v in enumerate(yoy)],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>YoY change: +%{y:.1f}%<extra></extra>",
    ))
    fig_cpi.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=35, b=48),
        shapes=[dict(type="line", xref="x", yref="paper", x0=2019.5, x1=2019.5,
                     y0=0, y1=1, line=dict(color="rgba(21,88,168,.6)", width=1.5, dash="dot"))],
        annotations=[
            dict(x=2019, y=max(yoy) * 0.72, text="2019 crisis", showarrow=True,
                 arrowhead=2, ay=-30, font=dict(size=10, color="#1558A8")),
            dict(x=2020, y=yoy[10], text="2020 blast", showarrow=True,
                 arrowhead=2, ay=-38, font=dict(size=10, color="#1558A8")),
        ],
        yaxis=dict(title="Year-over-Year % Change", ticksuffix="%",
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )

    # GDP comparison
    regional = [sum(D[c]["gdpPC"][i] for c in COUNTRIES if c != "Lebanon") / 4 for i in range(15)]
    fig_gdp = go.Figure([
        go.Scatter(x=YEARS, y=lb["gdpPC"], name="Lebanon", mode="lines+markers",
                   line=dict(color=COLORS["Lebanon"], width=2.8), marker=dict(size=5)),
        go.Scatter(x=YEARS, y=regional, name="Regional average", mode="lines+markers",
                   line=dict(color="#7f7a75", width=2.2, dash="dot"), marker=dict(size=4)),
    ])
    fig_gdp.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48),
        shapes=[crisis(yi), vline(yi)],
        annotations=[
            dict(x=2019, y=lb["gdpPC"][9], text="Currency collapse",
                 showarrow=True, arrowhead=2, ay=-40),
            dict(x=2020, y=lb["gdpPC"][10], text="Beirut blast",
                 showarrow=True, arrowhead=2, ay=45),
        ],
        yaxis=dict(title="GDP per capita", tickprefix="$",
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Split financing
    fig_split = go.Figure([
        go.Scatter(x=YEARS, y=lb["oop"], name="Out-of-pocket %",
                   mode="lines", stackgroup="one",
                   line=dict(color=COLORS["Lebanon"], width=1.8),
                   fillcolor=hex_to_rgba(COLORS["Lebanon"], .38)),
        go.Scatter(x=YEARS, y=[100 - v for v in lb["oop"]], name="Government & other",
                   mode="lines", stackgroup="one",
                   line=dict(color="#8a87d9", width=1.6),
                   fillcolor="rgba(138,135,217,.22)"),
    ])
    fig_split.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48),
        shapes=[crisis(yi), vline(yi)],
        yaxis=dict(range=[0, 100], ticksuffix="%", title="Share of expenditure",
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Migration pop
    crisis_shape_mig = dict(type="rect", xref="x", yref="paper", x0=2019, x1=2023,
                             y0=0, y1=1, fillcolor="rgba(21,88,168,.055)",
                             line=dict(width=0), layer="below")
    fig_pop = go.Figure(go.Scatter(
        x=YEARS, y=lb["pop"], mode="lines+markers", fill="tozeroy", name="Population (M)",
        line=dict(color=COLORS["Lebanon"], width=2.4),
        fillcolor=hex_to_rgba(COLORS["Lebanon"], .18),
    ))
    fig_pop.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=11),
        margin=dict(l=55, r=15, t=18, b=8), showlegend=False,
        shapes=[crisis_shape_mig],
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80"), showticklabels=False),
        yaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80", size=10),
                   title=dict(text="Population (M)", font=dict(size=10))),
        annotations=[dict(x=0.01, y=0.97, xref="paper", yref="paper",
                          text="<b>Population (M)</b>", showarrow=False,
                          font=dict(size=10, color=COLORS["Lebanon"]),
                          xanchor="left", yanchor="top")],
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )

    # Migration bar
    mig_colors = [hex_to_rgba("#1558A8", .65) if v >= 0 else hex_to_rgba("#1558A8", .28)
                  for v in lb["netMig"]]
    fig_mig = go.Figure(go.Bar(
        x=YEARS, y=lb["netMig"], name="Net migration rate",
        marker=dict(color=mig_colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Net migration: %{y:.1f} per 1,000<extra></extra>",
    ))
    fig_mig.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=11),
        margin=dict(l=55, r=15, t=8, b=38), showlegend=False,
        shapes=[crisis_shape_mig,
                dict(type="line", xref="x", yref="y", x0=2009.5, x1=2024.5, y0=0, y1=0,
                     line=dict(color="#566B80", width=1))],
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80", size=10)),
        yaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80", size=10),
                   title=dict(text="Net Mig Rate", font=dict(size=10))),
        annotations=[dict(x=0.01, y=0.97, xref="paper", yref="paper",
                          text="<b>Net Migration Rate (per 1,000)</b>", showarrow=False,
                          font=dict(size=10, color="#1558A8"),
                          xanchor="left", yanchor="top")],
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )
    return fig_cpi, fig_gdp, fig_split, fig_pop, fig_mig


# ── PAGE 3 ──────────────────────────────────────────────────────────────────

@app.callback(
    Output("p3_finance", "figure"),
    Output("p3_facet", "figure"),
    Output("p3_hospital", "figure"),
    Output("p3_oop_rank", "figure"),
    Input("store-yi", "data"),
    Input("store-active-tab", "data"),
)
def render_p3(yi, tab):
    # ── 1) Health financing: OOP vs Government/Other ───────────────────────
    sorted_fin = sorted(COUNTRIES, key=lambda c: D[c]["oop"][yi], reverse=True)
    fig_finance = go.Figure([
        go.Bar(
            name="Out-of-pocket %",
            x=sorted_fin,
            y=[D[c]["oop"][yi] for c in sorted_fin],
            marker=dict(color=[hex_to_rgba(COLORS[c], .72) for c in sorted_fin],
                        line=dict(color=[COLORS[c] for c in sorted_fin], width=1.2)),
            hovertemplate="<b>%{x}</b><br>OOP: %{y:.1f}%<extra></extra>",
        ),
        go.Bar(
            name="Government & Other",
            x=sorted_fin,
            y=[100 - D[c]["oop"][yi] for c in sorted_fin],
            marker=dict(color=[hex_to_rgba(COLORS[c], .18) for c in sorted_fin],
                        line=dict(color=[COLORS[c] for c in sorted_fin], width=1.2)),
            hovertemplate="<b>%{x}</b><br>Government & Other: %{y:.1f}%<extra></extra>",
        ),
    ])
    fig_finance.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        barmode="group", margin=dict(l=58, r=25, t=24, b=48),
        xaxis=dict(type="category", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        yaxis=dict(title="% of health expenditure", ticksuffix="%", range=[0, 100],
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # ── 2) Health expenditure per capita over time — facet per country ───────
    N = len(COUNTRIES)
    row_h = 1 / N
    gap = 0.012
    fig_facet = go.Figure()
    annotations_facet = []
    for i, c in enumerate(COUNTRIES):
        y_top = 1 - row_h * i
        y_bot = 1 - row_h * (i + 1)
        y_dom = [y_bot + gap, y_top - gap]
        is_last = i == N - 1
        x_ref = "x" if i == 0 else f"x{i+1}"
        y_ref = "y" if i == 0 else f"y{i+1}"
        xkey = "xaxis" if i == 0 else f"xaxis{i+1}"
        ykey = "yaxis" if i == 0 else f"yaxis{i+1}"
        fig_facet.add_trace(go.Scatter(
            x=YEARS, y=D[c]["healthPC"], mode="lines", fill="tozeroy",
            line=dict(color=COLORS[c], width=2.2),
            fillcolor=hex_to_rgba(COLORS[c], 0.15),
            showlegend=False,
            xaxis=x_ref, yaxis=y_ref,
            hovertemplate=f"<b>{c}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>",
        ))
        fig_facet.add_trace(go.Scatter(
            x=[YEARS[yi]], y=[D[c]["healthPC"][yi]], mode="markers",
            marker=dict(color=COLORS[c], size=6),
            showlegend=False, xaxis=x_ref, yaxis=y_ref, hoverinfo="skip",
        ))
        fig_facet.update_layout(**{
            xkey: dict(domain=[0, 1], anchor=y_ref, gridcolor="#efe8e0",
                       zeroline=False, linecolor="#e8dfd6",
                       tickfont=dict(color="#8c857d", size=9),
                       showticklabels=is_last, nticks=5),
            ykey: dict(domain=y_dom, anchor=x_ref, gridcolor="#efe8e0",
                       zeroline=False, linecolor="#e8dfd6",
                       tickfont=dict(color="#8c857d", size=9),
                       tickprefix="$", nticks=3),
        })
        annotations_facet.append(dict(
            x=-0.08, y=(y_dom[0] + y_dom[1]) / 2,
            xref="paper", yref="paper", text=f"<b>{c}</b>",
            showarrow=False, font=dict(size=10, color=COLORS[c],
                                        family="Inter,Arial,sans-serif"),
            xanchor="right", yanchor="middle",
        ))
    fig_facet.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=10),
        height=400, margin=dict(l=100, r=18, t=18, b=30), showlegend=False,
        annotations=annotations_facet,
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )

    # ── 3) Hospital bar chart ───────────────────────────────────────────────
    hospital_regions = ["Mount Lebanon", "Beirut", "North", "South", "Bekaa", "Nabatieh"]
    hospital_counts = [58, 32, 27, 21, 19, 14]

    # Muted slate-blue palette, high→low count
    hosp_colors  = ["#2C4A6E", "#3D6491", "#547DAF", "#7399C0", "#97B4D0", "#BDD0E2"]
    hosp_text_colors = ["#fff", "#fff", "#fff", "#1E2A3A", "#1E2A3A", "#1E2A3A"]

    fig_hospital = go.Figure(go.Bar(
        x=hospital_counts,
        y=hospital_regions,
        orientation="h",
        marker=dict(
            color=hosp_colors,
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[f"  {n}" for n in hospital_counts],
        textposition="inside",
        textfont=dict(color=hosp_text_colors, size=12, family="Inter, Arial, sans-serif"),
        insidetextanchor="start",
        hovertemplate="<b>%{y}</b><br>Hospitals: %{x}<extra></extra>",
    ))
    fig_hospital.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#F7F9FC",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        height=380, margin=dict(l=120, r=30, t=20, b=55),
        xaxis=dict(title="Number of hospitals", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        yaxis=dict(autorange="reversed", gridcolor="#F7F9FC", zeroline=False,
                   linecolor="#F7F9FC", tickfont=dict(color="#2C4A6E", size=11)),
        bargap=0.35,
        showlegend=False,
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # ── 5) OOP ranking ──────────────────────────────────────────────────────
    oop_sorted = sorted(COUNTRIES, key=lambda c: D[c]["oop"][yi], reverse=True)
    oop_vals   = [D[c]["oop"][yi] for c in oop_sorted]

    # Use each country's palette color, muted to 80% opacity, no outlines
    oop_colors      = [hex_to_rgba(COLORS[c], .78) for c in oop_sorted]
    oop_text_colors = ["#fff" if D[c]["oop"][yi] > 35 else "#1E2A3A" for c in oop_sorted]

    fig_oop = go.Figure(go.Bar(
        x=oop_vals,
        y=oop_sorted,
        orientation="h",
        marker=dict(
            color=oop_colors,
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[f"  {v:.1f}%" for v in oop_vals],
        textposition="inside",
        textfont=dict(color=oop_text_colors, size=12, family="Inter, Arial, sans-serif"),
        insidetextanchor="start",
        hovertemplate="<b>%{y}</b><br>Out-of-pocket: %{x:.1f}%<extra></extra>",
    ))
    fig_oop.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#F7F9FC",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        height=306, margin=dict(l=90, r=45, t=24, b=48),
        xaxis=dict(title="Out-of-pocket share (%)", ticksuffix="%", gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        yaxis=dict(autorange="reversed", gridcolor="#F7F9FC", zeroline=False,
                   linecolor="#F7F9FC", tickfont=dict(color="#1E2A3A", size=11)),
        bargap=0.35,
        showlegend=False,
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    return fig_finance, fig_facet, fig_hospital, fig_oop


# ── PAGE 4 ──────────────────────────────────────────────────────────────────

@app.callback(
    Output("p4_pop", "figure"),
    Output("p4_heat", "figure"),
    Output("p4_gender", "figure"),
    Output("p4_rates", "figure"),
    Input("store-yi", "data"),
    Input("store-active-tab", "data"),
)
def render_p4(yi, tab):
    # Population trends
    fig_pop = go.Figure([
        go.Scatter(x=YEARS, y=D[c]["pop"], name=c, mode="lines+markers",
                   line=dict(color=COLORS[c], width=2.6 if c == "Lebanon" else 2),
                   marker=dict(size=5 if c == "Lebanon" else 4),
                   hovertemplate=f"<b>{c}</b><br>%{{x}}: %{{y:.2f}}M<extra></extra>")
        for c in COUNTRIES
    ])
    fig_pop.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48),
        annotations=[dict(x=2012, y=18, text="Syrian conflict impact",
                          showarrow=True, arrowhead=2, ay=-38)],
        yaxis=dict(title="Population (M)", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        shapes=[vline(yi)],
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Heatmap
    indicators = ["Fertility", "Infant Mort.", "Median Age", "Life Exp."]
    z_vals = [[norm_country(c, "fertility", yi),
               norm_country(c, "infantMort", yi, True),
               norm_country(c, "medianAge", yi),
               norm_country(c, "lifeExp", yi)]
              for c in COUNTRIES]
    text_vals = [[f"{D[c]['fertility'][yi]:.2f}",
                  f"{D[c]['infantMort'][yi]:.1f}",
                  f"{D[c]['medianAge'][yi]:.1f}",
                  f"{D[c]['lifeExp'][yi]:.1f}"]
                 for c in COUNTRIES]
    fig_heat = go.Figure(go.Heatmap(
        x=indicators, y=COUNTRIES, z=z_vals, text=text_vals,
        texttemplate="%{text}", textfont=dict(size=11, family="Inter,Arial,sans-serif"),
        colorscale=[[0, "#F0F4FA"], [.5, "#8BAFD4"], [1, "#1558A8"]],
        showscale=True,
        colorbar=dict(title=dict(text="Score<br>(0-100)", font=dict(size=10)),
                      thickness=12, len=0.8),
        hovertemplate="<b>%{y}</b><br>%{x}<br>Score: %{z:.0f}/100<br>Value: %{text}<extra></extra>",
    ))
    fig_heat.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=95, r=70, t=30, b=55),
        xaxis=dict(type="category", tickfont=dict(size=11), gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5"),
        yaxis=dict(type="category", tickfont=dict(size=11), gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5"),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )

    # Gender life expectancy
    fig_gender = go.Figure([
        go.Scatter(x=YEARS, y=D["Lebanon"]["fLifeExp"], name="Female",
                   mode="lines+markers", line=dict(color=COLORS["Lebanon"], width=2.4),
                   marker=dict(size=5)),
        go.Scatter(x=YEARS, y=D["Lebanon"]["mLifeExp"], name="Male",
                   mode="lines+markers", line=dict(color=COLORS["Lebanon"], width=2.2, dash="dot"),
                   marker=dict(size=5)),
    ])
    fig_gender.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48),
        shapes=[vline(yi)],
        yaxis=dict(title="Life expectancy (years)", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        xaxis=dict(gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Birth/death rates — histogram-style bars, same pink identity
    sorted_rates = sorted(COUNTRIES, key=lambda c: D[c]["birthRate"][yi], reverse=True)
    fig_rates = go.Figure([
        go.Bar(name="Birth Rate ", x=sorted_rates,
               y=[D[c]["birthRate"][yi] for c in sorted_rates],
               marker=dict(color=hex_to_rgba("#1558A8", .72),
                           line=dict(color="#1558A8", width=1.4)),
               hovertemplate="<b>%{x}</b><br>Birth rate: %{y:.1f}<extra></extra>"),
        go.Bar(name="Death Rate ", x=sorted_rates,
               y=[D[c]["deathRate"][yi] for c in sorted_rates],
               marker=dict(color=hex_to_rgba("#1558A8", .22),
                           line=dict(color="#1558A8", width=1.4),
                           pattern=dict(shape="/", solidity=.18, fgcolor="#1558A8")),
               hovertemplate="<b>%{x}</b><br>Death rate: %{y:.1f}<extra></extra>"),
    ])
    fig_rates.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48),
        barmode="group",
        xaxis=dict(type="category", gridcolor="#E8EDF3", zeroline=False,
                   linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        yaxis=dict(title="Rate per 1,000", range=[0, 35], gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(255,255,255,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )
    return fig_pop, fig_heat, fig_gender, fig_rates


# ── PAGE 5 ──────────────────────────────────────────────────────────────────

@app.callback(
    Output("p5_afford", "figure"),
    Output("p5_bullet", "figure"),
    Output("p5_slope", "figure"),
    Output("p5_dotplot", "figure"),
    Input("store-yi", "data"),
    Input("store-active-tab", "data"),
)
def render_p5(yi, tab):
    # Affordability index
    vals_aff = sorted([(c, D[c]["healthPC"][yi] / D[c]["gdpPC"][yi] * 100) for c in COUNTRIES],
                      key=lambda x: x[1], reverse=True)
    fig_afford = go.Figure(go.Bar(
        orientation="h", y=[v[0] for v in vals_aff], x=[v[1] for v in vals_aff],
        marker=dict(color=[hex_to_rgba(COLORS[v[0]], .72) for v in vals_aff],
                    line=dict(color=[COLORS[v[0]] for v in vals_aff], width=1.2)),
        text=[f"{v[1]:.1f}%" for v in vals_aff], textposition="outside",
    ))
    fig_afford.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=58, r=25, t=24, b=48), showlegend=False,
        yaxis=dict(autorange="reversed", type="category", gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        xaxis=dict(title="Health exp/capita / GDP/capita", ticksuffix="%",
                   gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Bullet chart
    gdp_max = max(D[c]["gdpPC"][yi] for c in COUNTRIES)
    bullet_traces = []
    for c in COUNTRIES:
        oop = D[c]["oop"][yi]
        gdp_norm = D[c]["gdpPC"][yi] / gdp_max * 100
        bullet_traces.append(go.Bar(orientation="h", y=[c], x=[100],
            marker=dict(color="rgba(230,220,210,0.5)", line=dict(width=0)),
            showlegend=False, hoverinfo="skip", width=0.5))
        bullet_traces.append(go.Bar(orientation="h", y=[c], x=[gdp_norm],
            marker=dict(color=hex_to_rgba(COLORS[c], .18), line=dict(width=0)),
            showlegend=False,
            hovertemplate=f"<b>{c}</b><br>GDP tier: {gdp_norm:.0f}/100<extra></extra>", width=0.5))
        bullet_traces.append(go.Bar(orientation="h", y=[c], x=[oop],
            marker=dict(color=hex_to_rgba(COLORS[c], .8),
                        line=dict(color=COLORS[c], width=1.2)),
            showlegend=False,
            hovertemplate=f"<b>{c}</b><br>OOP burden: {oop:.1f}%<extra></extra>", width=0.3))
        bullet_traces.append(go.Scatter(mode="markers", x=[gdp_norm], y=[c],
            marker=dict(symbol="line-ns", size=16, color=COLORS[c],
                        line=dict(color=COLORS[c], width=2.5)),
            showlegend=False,
            hovertemplate=f"<b>{c}</b><br>GDP normalized: {gdp_norm:.0f}/100<extra></extra>"))
    fig_bullet = go.Figure(bullet_traces)
    fig_bullet.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        barmode="overlay", showlegend=False,
        margin=dict(l=80, r=25, t=24, b=48),
        xaxis=dict(title="OOP burden % (bars) vs GDP capacity (marker)", range=[0, 110],
                   ticksuffix="%", gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80")),
        yaxis=dict(type="category", autorange="reversed", gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", tickfont=dict(color="#566B80")),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # Slope chart
    x0, x1 = 2010, YEARS[yi]
    slope_traces = []
    for c in COUNTRIES:
        v0, v1 = D[c]["govtHlth"][0], D[c]["govtHlth"][yi]
        slope_traces.append(go.Scatter(
            x=[x0, x1], y=[v0, v1], name=c,
            mode="lines+markers+text",
            line=dict(color=COLORS[c], width=3 if c == "Lebanon" else 2),
            marker=dict(size=8, color=COLORS[c]),
            text=[f"{v0:.1f}%", f"{c}: {v1:.1f}%"],
            textposition=["middle left", "middle right"],
            textfont=dict(size=10, color=COLORS[c]),
            hovertemplate=f"<b>{c}</b><br>2010: {v0:.1f}%<br>{YEARS[yi]}: {v1:.1f}%<br>Change: {v1-v0:+.1f}%<extra></extra>",
        ))
    fig_slope = go.Figure(slope_traces)
    fig_slope.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        showlegend=False,
        margin=dict(l=80, r=160, t=40, b=45),
        xaxis=dict(tickvals=[x0, x1], ticktext=["2010", str(YEARS[yi])],
                   range=[x0 - 3, x1 + 8], tickfont=dict(size=11, color="#566B80"),
                   automargin=True, gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5"),
        yaxis=dict(title="Govt Health Spending %", ticksuffix="%",
                   automargin=True, gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                   tickfont=dict(color="#566B80", size=11)),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA", font=dict(color="#fff", size=12)),
    )

    # GDP vs Health subplots
    sorted_c = sorted(COUNTRIES, key=lambda c: D[c]["gdpPC"][yi], reverse=True)
    N = len(sorted_c)
    col_w = 1 / N
    gap = 0.018
    dot_traces = []
    dot_layout = dict(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter,Arial,sans-serif", color="#1E2A3A", size=10),
        margin=dict(l=52, r=12, t=42, b=40),
        showlegend=False,
        annotations=[],
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )
    for i, c in enumerate(sorted_c):
        x_ref = "x" if i == 0 else f"x{i+1}"
        y_ref = "y" if i == 0 else f"y{i+1}"
        xkey = "xaxis" if i == 0 else f"xaxis{i+1}"
        ykey = "yaxis" if i == 0 else f"yaxis{i+1}"
        x_dom = [col_w * i + gap, col_w * (i + 1) - gap]
        y_dom = [0, 0.84]
        gdp = D[c]["gdpPC"][yi]
        hlth = D[c]["healthPC"][yi]
        def fmt_val(v):
            return f"${v/1000:.1f}K" if v >= 1000 else f"${v:.0f}"
        dot_traces.append(go.Bar(
            x=["GDP/cap", "Health/cap"], y=[gdp, hlth],
            xaxis=x_ref, yaxis=y_ref,
            marker=dict(
                color=[hex_to_rgba(COLORS[c], 0.75), hex_to_rgba(COLORS[c], 0.35)],
                line=dict(color=COLORS[c], width=1.5),
            ),
            text=[fmt_val(gdp), fmt_val(hlth)],
            textposition="outside",
            cliponaxis=False,
            showlegend=False,
            hovertemplate=f"<b>{c}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>",
        ))
        dot_layout[xkey] = dict(domain=x_dom, anchor=y_ref, type="category",
                                 gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                                 tickfont=dict(color="#445566", size=10),
                                 showticklabels=True, ticks="outside")
        dot_layout[ykey] = dict(domain=y_dom, anchor=x_ref,
                                 gridcolor="#E8EDF3", zeroline=False, linecolor="#C8D6E5",
                                 tickfont=dict(color="#566B80", size=9),
                                 tickprefix="$", nticks=4,
                                 showticklabels=i == 0, showgrid=True)
        dot_layout["annotations"].append(dict(
            x=(x_dom[0] + x_dom[1]) / 2, y=0.98,
            xref="paper", yref="paper",
            text=f"<b>{c}</b>", showarrow=False,
            font=dict(size=11, color=COLORS[c], family="Inter,Arial,sans-serif"),
            xanchor="center", yanchor="top",
        ))
    fig_dot = go.Figure(dot_traces)
    fig_dot.update_layout(**dot_layout)
    return fig_afford, fig_bullet, fig_slope, fig_dot


# ── PAGE 6 ──────────────────────────────────────────────────────────────────

@app.callback(
    Output("p6_heatmap", "figure"),
    Input("store-yi", "data"),
    Input("hm-metric", "value"),
    Input("store-hm-countries", "data"),
    Input("store-active-tab", "data"),
)
def render_p6(yi, metric, hm_countries, tab):
    lb_only_metrics = ["cpi"]
    is_lb_only = metric in lb_only_metrics
    countries = ["Lebanon"] if is_lb_only else (hm_countries or COUNTRIES)

    filtered_years = YEARS[:yi + 1]
    z_mat = [[D[c][metric][i] if D[c].get(metric) else None for i in range(yi + 1)]
             for c in countries]

    def fmt_cell(c, i):
        v = D[c][metric][i] if D[c].get(metric) else None
        if v is None:
            return ""
        if metric in ("gdpPC", "healthPC"):
            return f"${v/1000:.1f}K" if v >= 1000 else f"${v:.0f}"
        if metric == "pop":
            return f"{v:.1f}M"
        if metric == "cpi":
            return f"{v/1000:.0f}K" if v >= 1000 else f"{v:.0f}"
        return f"{v:.1f}"

    text_mat = [[fmt_cell(c, i) for i in range(yi + 1)] for c in countries]

    invert_metrics = ["infantMort", "oop", "deathRate"]
    if metric in invert_metrics:
        col_scale = [[0, "#1558A8"], [.5, "#8BAFD4"], [1, "#F0F4FA"]]
    else:
        col_scale = [[0, "#F0F4FA"], [.5, "#8BAFD4"], [1, "#1558A8"]]

    fig_hm = go.Figure(go.Heatmap(
        x=filtered_years, y=countries, z=z_mat,
        text=text_mat, texttemplate="%{text}",
        textfont=dict(size=10, family="Inter,Arial,sans-serif"),
        colorscale=col_scale, showscale=True,
        colorbar=dict(title=dict(text=METRIC_LABELS.get(metric, metric), font=dict(size=10)),
                      thickness=14),
        hovertemplate=f"<b>%{{y}}</b><br>%{{x}}<br>{METRIC_LABELS.get(metric,'')}: %{{text}}<extra></extra>",
    ))
    fig_hm.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter, Arial, sans-serif", color="#1E2A3A", size=12),
        margin=dict(l=90, r=120, t=36, b=48),
        xaxis=dict(type="category", tickfont=dict(size=10), gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5"),
        yaxis=dict(type="category", tickfont=dict(size=11), gridcolor="#E8EDF3",
                   zeroline=False, linecolor="#C8D6E5", automargin=True),
        hoverlabel=dict(bgcolor="rgba(20,30,48,.95)", bordercolor="#90ACCA",
                        font=dict(color="#fff", size=12)),
    )
    return fig_hm


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
