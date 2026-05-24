from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash application
app = Dash(__name__)

# 1. Load the cleaned dataset generated in Task 2
df = pd.read_csv("formatted_data.csv")

# Ensure the Date column is read as a date type and sorted chronologically
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

# Group data by Date to sum up total sales for each day across all regions
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# 2. Create the Plotly Line Chart
fig = px.line(
    daily_sales, 
    x="Date", 
    y="Sales", 
    title="Pink Morsel Daily Sales Performance",
    labels={"Date": "Transaction Date", "Sales": "Total Revenue ($)"}
)

# FIXED: Add the vertical milestone line safely without conflicting internal string types
fig.add_vline(
    x="2021-01-15", 
    line_width=3, 
    line_dash="dash", 
    line_color="red"
)

# Safely overlay the label annotation onto the graph layout manually
fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["Sales"].max(),
    text="Price Increase (Jan 15, 2021)",
    showarrow=True,
    arrowhead=1,
    ax=-50,
    ay=-30
)

# 3. Define the Web Application Layout HTML
app.layout = html.Div(children=[
    html.H1(
        children="Soul Foods Sales Performance Dashboard",
        style={"textAlign": "center", "fontFamily": "sans-serif", "color": "#2c3e50"}
    ),
    
    html.P(
        children="Answering the impact of the Pink Morsel price increase on January 15, 2021.",
        style={"textAlign": "center", "fontFamily": "sans-serif", "color": "#7f8c8d"}
    ),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# Run the local development server
if __name__ == "__main__":
    app.run(debug=True)