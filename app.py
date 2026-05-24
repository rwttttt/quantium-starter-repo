from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash application
app = Dash(__name__)

# 1. Load the cleaned dataset generated in Task 2
df = pd.read_csv("formatted_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

# 2. Define the Styled Web Application Layout
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "backgroundColor": "#f8f9fa",
        "padding": "40px",
        "minHeight": "100vh"
    },
    children=[
        # App Header Card
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "30px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
                "marginBottom": "30px",
                "textAlign": "center"
            },
            children=[
                html.H1(
                    children="Soul Foods Sales Performance Dashboard",
                    style={"margin": "0 0 10px 0", "color": "#2c3e50", "fontWeight": "600"}
                ),
                html.P(
                    children="Analyzing the business impact of the Pink Morsel price increase on January 15, 2021.",
                    style={"margin": "0", "color": "#7f8c8d", "fontSize": "16px"}
                )
            ]
        ),
        
        # Interactive Controls Card
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "20px 30px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)",
                "marginBottom": "30px"
            },
            children=[
                html.Label(
                    "Filter Visualization by Region:",
                    style={"fontWeight": "bold", "color": "#34495e", "display": "block", "marginBottom": "12px"}
                ),
                # Radio button component matching the five required options
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                        {"label": " All Regions", "value": "all"}
                    ],
                    value="all", # Default selection
                    inline=True,
                    labelStyle={
                        "marginRight": "25px",
                        "color": "#2c3e50",
                        "fontSize": "15px",
                        "cursor": "pointer"
                    }
                )
            ]
        ),

        # Chart Display Card
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "padding": "25px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 6px rgba(0,0,0,0.05)"
            },
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        )
    ]
)

# 3. Define the Callback to Make the App Interactive
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    # Filter dataset based on the radio button input
    if selected_region == "all":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["region"].str.lower() == selected_region.lower()]
    
    # Group by date to aggregate regional total values cleanly
    daily_sales = filtered_df.groupby("Date")["Sales"].sum().reset_index()
    
    # Generate interactive plot
    fig = px.line(
        daily_sales, 
        x="Date", 
        y="Sales", 
        title=f"Pink Morsel Daily Sales — Performance ({selected_region.upper()})",
        labels={"Date": "Transaction Date", "Sales": "Total Revenue ($)"},
        template="plotly_white"
    )
    
    # Apply clean chart design styles
    fig.update_traces(line_color="#e74c3c" if selected_region == "all" else "#3498db", line_width=2.5)
    
    # Safely append the January 15th price milestone marker line
    fig.add_vline(
        x="2021-01-15", 
        line_width=2, 
        line_dash="dash", 
        line_color="#27ae60"
    )
    
    # Dynamic annotation placement based on the maximum data peak
    if not daily_sales.empty:
        fig.add_annotation(
            x="2021-01-15",
            y=daily_sales["Sales"].max(),
            text="Price Increase (Jan 15, 2021)",
            showarrow=True,
            arrowhead=1,
            ax=-60,
            ay=-30,
            font=dict(color="#27ae60", size=11)
        )
        
    return fig

# Start the application server
if __name__ == "__main__":
    app.run(debug=True)