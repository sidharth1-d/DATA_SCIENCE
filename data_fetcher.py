import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
from dateutil import parser

def fetch_oil_data(period="3mo", interval="1d"):
    """Fetch crude oil futures data (CL=F)."""
    try:
        ticker = yf.Ticker("CL=F")
        df = ticker.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error fetching oil data: {e}")
        return pd.DataFrame()

def fetch_vix_data(period="3mo", interval="1d"):
    """Fetch VIX data for general market volatility."""
    try:
        ticker = yf.Ticker("^VIX")
        df = ticker.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error fetching VIX data: {e}")
        return pd.DataFrame()

def get_oil_news():
    """Fetch real crude oil news from OilPrice RSS feed."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://oilprice.com/rss/main', headers=headers, timeout=10)
        
        if response.status_code != 200:
            return _get_fallback_news()
            
        root = ET.fromstring(response.content)
        processed_news = []
        
        for item in root.findall('./channel/item')[:10]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')
            
            title = title_elem.text if title_elem is not None else 'No Title'
            link = link_elem.text if link_elem is not None else '#'
            pub_date = pub_date_elem.text if pub_date_elem is not None else ''
            
            time_str = "Recent"
            if pub_date:
                try:
                    dt = parser.parse(pub_date)
                    time_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = str(pub_date)[:16]
                    
            title_lower = title.lower()
            if any(word in title_lower for word in ['opec', 'war', 'supply', 'inventory', 'cut', 'reserve', 'crisis', 'shock', 'drone', 'strike']):
                impact = 'High'
                impact_class = 'impact-high'
            elif any(word in title_lower for word in ['demand', 'forecast', 'price', 'economy', 'rate', 'export', 'import', 'drill', 'rig']):
                impact = 'Medium'
                impact_class = 'impact-medium'
            else:
                impact = 'Low'
                impact_class = 'impact-low'
                
            processed_news.append({
                'title': title,
                'link': link,
                'time': time_str,
                'impact': impact,
                'impact_class': impact_class,
                'publisher': 'OilPrice.com'
            })
            
        if not processed_news:
            return _get_fallback_news()
            
        return processed_news
    except Exception as e:
        print(f"Error fetching news: {e}")
        return _get_fallback_news()

def _get_fallback_news():
    return [{"title": "OPEC+ Announces Unplanned Production Cuts", "link": "#", "time": "2 hours ago", "impact": "High", "impact_class": "impact-high", "publisher": "Market News"},
            {"title": "US Crude Inventories Show Unexpected Build", "link": "#", "time": "5 hours ago", "impact": "Medium", "impact_class": "impact-medium", "publisher": "Energy Daily"}]

def get_current_metrics():
    """Fetch the latest price and calculate basic daily change."""
    df_oil = fetch_oil_data(period="5d")
    df_vix = fetch_vix_data(period="5d")
    
    if df_oil.empty or len(df_oil) < 2:
        return {"oil_price": 0, "oil_change": 0, "oil_change_pct": 0, "vix": 0, "vix_change": 0}
        
    latest_oil = df_oil['Close'].iloc[-1]
    prev_oil = df_oil['Close'].iloc[-2]
    oil_change = latest_oil - prev_oil
    oil_change_pct = (oil_change / prev_oil) * 100
    
    latest_vix = df_vix['Close'].iloc[-1] if not df_vix.empty else 0
    prev_vix = df_vix['Close'].iloc[-2] if not df_vix.empty and len(df_vix) >= 2 else 0
    vix_change = latest_vix - prev_vix
    
    return {
        "oil_price": round(latest_oil, 2),
        "oil_change": round(oil_change, 2),
        "oil_change_pct": round(oil_change_pct, 2),
        "vix": round(latest_vix, 2),
        "vix_change": round(vix_change, 2)
    }
