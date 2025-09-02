import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.basedatatypes import BaseFigure
import pandas as pd
from .constants import COLOR_MAP, METRIC_INFO

def create_metric_trend_chart(
              df:pd.DataFrame,
              metric='Revenue',
              companies=None)->BaseFigure:
    """Create trend chart for selected metric"""
        
    df_filtered = df if companies is None else df[df['Simbol'].isin(companies)]
        
    metric_info = METRIC_INFO 
        
    info = metric_info.get(
        metric, {
              'label': f'{metric} (Rn)',
              'title': f'{metric} Trend Over Time'})
        
    fig = px.line(
        df_filtered, 
        x='Report Date', 
        y=metric, 
        color='Simbol',
        title=info['title'],
        labels={metric: info['label'], 'Report Date': 'Date'},
        color_discrete_map=COLOR_MAP)
        
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        height=400,
        legend=dict(
            bgcolor="rgba(0, 0, 0, 0)",  
            bordercolor="rgba(0, 0, 0, 0.2)",  
            borderwidth=2
            ))
        
    return fig

def create_profitability_comparison(
              df:pd.DataFrame,
              companies=None)->BaseFigure:
    """Create profitability margins comparison"""
    df_filtered = df if companies is None else df[df['Simbol'].isin(companies)]
        
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Gross Margin %',
            'Operating Margin %',
            'Net Margin %',
            'Absolute Profits'),
        specs=[[
            {"secondary_y": False},
            {"secondary_y": False}],
        [
            {"secondary_y": False},
            {"secondary_y": False}]]
        )
        
    for company in df_filtered['Simbol'].unique():
        company_data = df_filtered[df_filtered['Simbol'] == company]
        color = COLOR_MAP.get(company, '#666666')
            
        fig.add_trace(
            go.Scatter(
                x=company_data['Report Date'],
                y=company_data['Gross Margin %'],
                name=f'{company} - Gross',
                line=dict(color=color),
                showlegend=True),
            row=1, col=1)
            
        fig.add_trace(
            go.Scatter(
                x=company_data['Report Date'],
                y=company_data['Operating Margin %'],
                name=f'{company} - Operating',
                line=dict(color=color, dash='dash'),
                showlegend=True),
            row=1, col=2)
            
        fig.add_trace(
            go.Scatter(
                x=company_data['Report Date'],
                y=company_data['Net Margin %'],
                name=f'{company} - Net',
                line=dict(color=color, dash='dot'),
                showlegend=True),
            row=2, col=1)
            
        fig.add_trace(
            go.Bar(
                x=company_data['Quarter_Year'],
                y=company_data['Net Income'],
                name=f'{company} - Net Income',
                marker_color=color,
                opacity=0.7,
                showlegend=True),
            row=2, col=2)
        
    fig.update_layout(
        height=600,
        template='plotly_white',
        title_text="Profitability Analysis Dashboard",
        legend=dict(
            bgcolor="rgba(0, 0, 0, 0)",  
            bordercolor="rgba(0, 0, 0, 0.2)",  
            borderwidth=2))                
        
    return fig