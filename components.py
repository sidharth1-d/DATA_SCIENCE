import plotly.graph_objects as go
import plotly.express as px

def create_candlestick_chart(df):
    """Create a premium candlestick chart with support/resistance."""
    if df.empty:
        return go.Figure()
        
    fig = go.Figure()
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='CL=F',
        increasing_line_color='#10b981', 
        decreasing_line_color='#ef4444'
    ))
    
    # Support/Resistance (if calculated)
    if 'Support' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['Support'], mode='lines', name='Support (20d)', line=dict(color='#3b82f6', width=1, dash='dot')))
    if 'Resistance' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['Resistance'], mode='lines', name='Resistance (20d)', line=dict(color='#d4af37', width=1, dash='dot')))
        
    # Moving Averages
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='#c0c0c0', width=1)))
        
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_rangeslider_visible=False,
        font=dict(family="Inter, sans-serif", color="#f8fafc"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_volatility_chart(df):
    """Create an area chart for historical volatility."""
    if df.empty or 'Hist_Vol' not in df.columns:
        return go.Figure()
        
    fig = go.Figure()
    
    # Filter out NaNs to prevent visual gaps
    valid_data = df.dropna(subset=['Hist_Vol'])
    
    fig.add_trace(go.Scatter(
        x=valid_data.index, 
        y=valid_data['Hist_Vol'],
        fill='tozeroy',
        mode='lines',
        line=dict(color='#d4af37', width=2),
        fillcolor='rgba(212, 175, 55, 0.2)',
        name='Historical Volatility (20d)'
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(family="Inter, sans-serif", color="#f8fafc")
    )
    
    return fig

def create_sentiment_gauge(score, level, color_str):
    """Create a gauge chart for risk sentiment."""
    
    # Map color string to hex
    color_map = {
        "red": "#ef4444",
        "orange": "#f97316",
        "gray": "#94a3b8",
        "green": "#10b981",
        "darkgreen": "#047857"
    }
    hex_color = color_map.get(color_str, "#d4af37")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Sentiment: {level}", 'font': {'size': 18, 'color': hex_color}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': hex_color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [30, 45], 'color': 'rgba(249, 115, 22, 0.2)'},
                {'range': [45, 55], 'color': 'rgba(148, 163, 184, 0.2)'},
                {'range': [55, 70], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(4, 120, 87, 0.2)'}
            ],
        }
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Inter, sans-serif", color="#f8fafc")
    )
    
    return fig
