# app.py - FIXED FOR RENDER DEPLOYMENT
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import requests
import os
from fredapi import Fred

# Initialize FRED API (for live data)
fred = Fred(api_key='YOUR_API_KEY_HERE')  # You'll need to get a free API key from FRED

def load_and_enrich_data():
    """Load your data and enrich with more indicators"""
    try:
        file_path = Path("data/processed/merged_data.csv")
        
        if not file_path.exists():
            print("❌ No local data file found. Using sample data...")
            return create_sample_data()
            
        df = pd.read_csv(file_path)
        print(f"✅ Local data loaded! Shape: {df.shape}")
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        # Fill NaN values in GDP (forward fill)
        if 'gdp' in df.columns:
            df['gdp'] = df['gdp'].fillna(method='ffill')
        
        # Add more economic indicators (sample calculation)
        if 'fedfunds' in df.columns:
            df['inflation_estimate'] = df['fedfunds'] * 0.5  # Simplified relationship
        
        # Add technical indicators
        if 'gdp' in df.columns:
            df['gdp_growth'] = df['gdp'].pct_change() * 100
            df['gdp_ma_12'] = df['gdp'].rolling(window=12).mean()
        
        if 'fedfunds' in df.columns:
            df['fedfunds_ma_6'] = df['fedfunds'].rolling(window=6).mean()
        
        print(f"📊 Final columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return create_sample_data()

def create_sample_data():
    """Create rich sample data with multiple indicators"""
    print("📋 Creating enriched sample data...")
    dates = pd.date_range(start='2000-01-01', end=datetime.now(), freq='M')
    n_periods = len(dates)
    
    # Create realistic economic data
    np.random.seed(42)
    base_gdp = 10000
    growth_trend = np.array([base_gdp + i*80 for i in range(n_periods)])
    gdp_cycles = 50 * np.sin(2 * np.pi * np.arange(n_periods) / 60)  # 5-year cycles
    gdp_random = np.random.normal(0, 100, n_periods)
    gdp_values = growth_trend + gdp_cycles + gdp_random
    
    # Federal funds rate with economic cycles
    fedfunds_trend = np.array([5.0 - i*0.01 for i in range(n_periods)])
    fedfunds_cycles = 2 * np.sin(2 * np.pi * np.arange(n_periods) / 40)
    fedfunds_random = np.random.normal(0, 0.3, n_periods)
    fedfunds_values = np.clip(fedfunds_trend + fedfunds_cycles + fedfunds_random, 0, 10)
    
    df = pd.DataFrame({
        'date': dates,
        'gdp': gdp_values,
        'fedfunds': fedfunds_values,
        'unemployment': np.clip(8.0 - np.arange(n_periods)*0.02 + np.random.normal(0, 0.5, n_periods), 3, 10),
        'cpi': np.array([180 + i*0.3 + 5*np.sin(2*np.pi*i/24) for i in range(n_periods)]),
        'industrial_production': np.array([100 + i*0.5 + 10*np.sin(2*np.pi*i/36) for i in range(n_periods)])
    })
    
    # Add derived indicators
    df['gdp_growth'] = df['gdp'].pct_change() * 100
    df['inflation_rate'] = df['cpi'].pct_change() * 100
    df['gdp_ma_12'] = df['gdp'].rolling(window=12).mean()
    df['fedfunds_ma_6'] = df['fedfunds'].rolling(window=6).mean()
    
    return df

# Load data
df = load_and_enrich_data()
numeric_columns = [col for col in df.columns if col != 'date' and pd.api.types.is_numeric_dtype(df[col])]

print(f"📅 Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
print(f"📊 Available indicators: {numeric_columns}")

# Create Dash app
app = dash.Dash(__name__, title="Advanced FRED Economic Dashboard")
server = app.server  # CRITICAL: This makes the server available to Render

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📈 ADVANCED FRED ECONOMIC DASHBOARD", 
                style={'textAlign': 'center', 'color': 'white', 'marginBottom': '10px'}),
        html.P("Port 8053 | Real-time Economic Indicators | Interactive Analysis",
              style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.8)', 'fontSize': '16px'})
    ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
              'padding': '30px', 'borderRadius': '15px', 'marginBottom': '30px'}),
    
    # Controls
    html.Div([
        html.Div([
            html.Label("📊 Select Primary Indicator:"),
            dcc.Dropdown(
                id='primary-indicator',
                options=[{'label': col.upper(), 'value': col} for col in numeric_columns],
                value='gdp',
                clearable=False,
                style={'width': '100%'}
            )
        ], className='six columns'),
        
        html.Div([
            html.Label("📈 Select Secondary Indicator:"),
            dcc.Dropdown(
                id='secondary-indicator',
                options=[{'label': col.upper(), 'value': col} for col in numeric_columns],
                value='fedfunds',
                clearable=False,
                style={'width': '100%'}
            )
        ], className='six columns')
    ], className='row', style={'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.Label("📅 Date Range:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            )
        ], className='six columns'),
        
        html.Div([
            html.Label("⚡ Chart Type:"),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': ' Line Chart', 'value': 'line'},
                    {'label': ' Area Chart', 'value': 'area'},
                    {'label': ' Scatter Plot', 'value': 'scatter'}
                ],
                value='line',
                inline=True,
                style={'marginTop': '10px'}
            )
        ], className='six columns')
    ], className='row', style={'marginBottom': '30px'}),
    
    # Main Charts
    html.Div([
        dcc.Graph(id='main-chart', style={'height': '500px'})
    ], className='row', style={'marginBottom': '30px'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='primary-chart', style={'height': '350px'})
        ], className='six columns'),
        
        html.Div([
            dcc.Graph(id='secondary-chart', style={'height': '350px'})
        ], className='six columns')
    ], className='row', style={'marginBottom': '30px'}),
    
    # Statistics and Data Table
    html.Div([
        html.Div([
            html.H3("📋 Summary Statistics"),
            html.Div(id='summary-stats')
        ], className='six columns', style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3("📊 Raw Data Preview"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.tail(10).to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'}
            )
        ], className='six columns')
    ], className='row'),
    
    # Footer
    html.Div([
        html.P(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
               f"Data Points: {len(df):,} | Indicators: {len(numeric_columns)}",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '30px'})
    ])
], style={'padding': '20px', 'backgroundColor': '#f5f7fa'})

# Callbacks
@app.callback(
    [Output('main-chart', 'figure'),
     Output('primary-chart', 'figure'),
     Output('secondary-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('primary-indicator', 'value'),
     Input('secondary-indicator', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('chart-type', 'value')]
)
def update_all_charts(primary_ind, secondary_ind, start_date, end_date, chart_type):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Main chart (both indicators)
    if chart_type == 'line':
        fig_main = make_subplots(specs=[[{"secondary_y": True}]])
        fig_main.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df[primary_ind], 
                                    name=primary_ind.upper(), line=dict(color='#3498db')), secondary_y=False)
        fig_main.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df[secondary_ind], 
                                    name=secondary_ind.upper(), line=dict(color='#e74c3c')), secondary_y=True)
        fig_main.update_layout(title=f"{primary_ind.upper()} vs {secondary_ind.upper()}", hovermode='x unified')
    else:
        fig_main = px.scatter(filtered_df, x=primary_ind, y=secondary_ind, 
                             title=f"{primary_ind.upper()} vs {secondary_ind.upper()} Correlation")
    
    # Individual charts
    fig_primary = px.area(filtered_df, x='date', y=primary_ind, title=f"{primary_ind.upper()} Trend")
    fig_secondary = px.area(filtered_df, x='date', y=secondary_ind, title=f"{secondary_ind.upper()} Trend")
    
    # Summary statistics
    stats = []
    for col in [primary_ind, secondary_ind]:
        if col in filtered_df.columns:
            stats.append(html.Div([
                html.H4(f"{col.upper()} STATS"),
                html.P(f"📈 Current: {filtered_df[col].iloc[-1]:.2f}"),
                html.P(f"📊 Average: {filtered_df[col].mean():.2f}"),
                html.P(f"📉 Min: {filtered_df[col].min():.2f}"),
                html.P(f"📈 Max: {filtered_df[col].max():.2f}"),
                html.P(f"📋 Change: {(filtered_df[col].iloc[-1] - filtered_df[col].iloc[0]):.2f}"),
            ], style={'marginRight': '20px', 'display': 'inline-block', 'verticalAlign': 'top'}))
    
    return fig_main, fig_primary, fig_secondary, stats

# THIS IS THE ONLY if __name__ BLOCK - CRITICAL FOR RENDER
if __name__ == '__main__':
    # Get port from environment variable or default to 8053
    port = int(os.environ.get('PORT', 8053))
    # Get debug mode from environment (False in production)
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("🚀 Starting ADVANCED FRED Dashboard...")
    print(f"👉 Open: http://localhost:{port}")
    print(f"📅 Data from {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"📊 Indicators available: {', '.join(numeric_columns)}")
    
    app.run_server(
        host='0.0.0.0',  # Important: listen on all interfaces
        port=port,
        debug=debug,
        dev_tools_ui=debug,
        dev_tools_props_check=debug
    )