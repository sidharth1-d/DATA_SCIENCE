import gradio as gr
import pandas as pd
from data_fetcher import fetch_oil_data, fetch_vix_data, get_oil_news, get_current_metrics
from calculations import calculate_volatility, calculate_technical_indicators, calculate_risk_sentiment
from components import create_candlestick_chart, create_volatility_chart, create_sentiment_gauge

# Load custom CSS
try:
    with open("style.css", "r") as f:
        custom_css = f.read()
except FileNotFoundError:
    custom_css = ""

def update_dashboard():
    # 1. Fetch Data
    df_oil = fetch_oil_data(period="6mo")
    df_vix = fetch_vix_data(period="6mo")
    
    # 2. Calculations
    df_oil = calculate_technical_indicators(df_oil)
    df_oil = calculate_volatility(df_oil)
    
    # 3. Metrics
    metrics = get_current_metrics()
    
    # Current RSI
    current_rsi = df_oil['RSI'].iloc[-1] if not df_oil.empty and 'RSI' in df_oil.columns else 50
    current_vix = metrics['vix']
    
    sentiment = calculate_risk_sentiment(current_vix, current_rsi)
    
    # 4. Generate Charts
    fig_trend = create_candlestick_chart(df_oil)
    fig_vol = create_volatility_chart(df_oil)
    fig_sentiment = create_sentiment_gauge(sentiment['score'], sentiment['level'], sentiment['color'])
    
    # 5. Format News
    news_items = get_oil_news()
    news_html = "<div style='height: 400px; overflow-y: auto; padding-right: 10px;'>"
    for item in news_items:
        news_html += f"""
        <div class="news-item">
            <div class="news-time">{item['time']} | {item['publisher']} <span class="news-impact {item['impact_class']}">{item['impact']}</span></div>
            <div class="news-title"><a href="{item['link']}" target="_blank" style="color: inherit; text-decoration: none;">{item['title']}</a></div>
        </div>
        """
    if not news_items:
        news_html += "<div class='news-item'><div class='news-title'>No recent news found.</div></div>"
    news_html += "</div>"
        
    # Format Metric Cards
    oil_color_class = "metric-positive" if metrics['oil_change'] >= 0 else "metric-negative"
    oil_sign = "+" if metrics['oil_change'] >= 0 else ""
    
    vix_color_class = "metric-positive" if metrics['vix_change'] < 0 else "metric-negative" # VIX down is generally positive
    vix_sign = "+" if metrics['vix_change'] >= 0 else ""
    
    metric_html = f"""
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="metric-card">
            <div class="metric-label">WTI Crude (CL=F)</div>
            <div class="metric-value">${metrics['oil_price']:.2f}</div>
            <div class="{oil_color_class}">{oil_sign}{metrics['oil_change']:.2f} ({oil_sign}{metrics['oil_change_pct']:.2f}%)</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Volatility Index (^VIX)</div>
            <div class="metric-value">{metrics['vix']:.2f}</div>
            <div class="{vix_color_class}">{vix_sign}{metrics['vix_change']:.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Current RSI</div>
            <div class="metric-value">{"--" if pd.isna(current_rsi) else f"{current_rsi:.1f}"}</div>
            <div class="metric-label" style="margin-top: 10px;">14-Day Period</div>
        </div>
    </div>
    """
    
    return metric_html, fig_trend, fig_vol, fig_sentiment, news_html

with gr.Blocks() as demo:
    gr.HTML("<h1>Crude Oil Volatility & Risk Dashboard</h1>")
    
    with gr.Row():
        with gr.Column(scale=1, elem_classes="panel-container"):
            metrics_display = gr.HTML(label="Real-Time Metrics")
            
    with gr.Row():
        with gr.Column(scale=2, elem_classes="panel-container"):
            gr.HTML("<h2>Trend Analysis</h2>")
            trend_chart = gr.Plot(label="Price & Technicals", show_label=False)
            
        with gr.Column(scale=1, elem_classes="panel-container"):
            gr.HTML("<h2>Risk Sentiment</h2>")
            sentiment_chart = gr.Plot(label="Composite Sentiment", show_label=False)
            
    with gr.Row():
        with gr.Column(scale=2, elem_classes="panel-container"):
            gr.HTML("<h2>Historical Volatility</h2>")
            volatility_chart = gr.Plot(label="20-Day Annualized Volatility", show_label=False)
            
        with gr.Column(scale=1, elem_classes="panel-container"):
            gr.HTML("<h2>News Catalyst Tracker</h2>")
            news_display = gr.HTML(label="Latest News")
            
    with gr.Row():
        refresh_btn = gr.Button("Refresh Data", elem_classes="gr-button-primary")
        
    # Wire up events
    outputs = [metrics_display, trend_chart, volatility_chart, sentiment_chart, news_display]
    
    demo.load(fn=update_dashboard, inputs=[], outputs=outputs)
    refresh_btn.click(fn=update_dashboard, inputs=[], outputs=outputs)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, theme=gr.themes.Base(), css=custom_css)
