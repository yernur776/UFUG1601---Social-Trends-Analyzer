# dashboard_dash.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load your merged dataset
data = pd.read_csv("./data/merged_country_data.csv")  # ensure proper columns

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Global Social Trends Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Global Social Trends Dashboard"),

    html.Div([
        html.Label("Select a Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in data['Country'].unique()],
            value=data['Country'].iloc[0]  # default
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div(id='country-info', style={'marginTop': 20}),

    html.H2("Global Comparisons"),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='choropleth-map'),

    html.Div(id='ai-summary', style={'marginTop': 20, 'whiteSpace': 'pre-line'})
])

# Callbacks
@app.callback(
    [Output('country-info', 'children'),
     Output('scatter-plot', 'figure'),
     Output('choropleth-map', 'figure'),
     Output('ai-summary', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_dashboard(selected_country):
    country_data = data[data['Country'] == selected_country].iloc[0]

    # Country indicators
    indicators = [
        html.P(f"Happiness Score: {country_data['Happiness Score']}"),
        html.P(f"GDP per Capita: {country_data['GDP per Capita']}"),
        html.P(f"Education Expenditure (% GDP): {country_data['Education Expenditure']}"),
        html.P(f"Life Expectancy: {country_data['Life Expectancy']}")
    ]
    if 'Predicted Happiness' in data.columns:
        indicators.append(html.P(f"Predicted Happiness Score: {country_data['Predicted Happiness']}"))

    # Scatter plot: GDP vs Happiness
    scatter_fig = px.scatter(
        data, x='GDP per Capita', y='Happiness Score', color='Region',
        hover_name='Country', size='Life Expectancy',
        title='GDP per Capita vs Happiness Score'
    )

    # Choropleth map by Happiness Score
    choropleth_fig = px.choropleth(
        data, locations='Country Code', color='Happiness Score',
        hover_name='Country', color_continuous_scale=px.colors.sequential.Plasma,
        title='World Happiness Map'
    )

    # AI Summary (optional)
    ai_text = country_data['AI Summary'] if 'AI Summary' in country_data else ""

    return indicators, scatter_fig, choropleth_fig, ai_text


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
