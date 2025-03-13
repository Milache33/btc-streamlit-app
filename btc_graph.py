import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Fonction pour récupérer les données de bougies depuis Binance
def get_candlestick_data(interval):
    limits = {"5m": 288, "15m": 96, "1h": 24}  # Assure 24h d'historique
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval={interval}&limit={limits[interval]}"
    response = requests.get(url)
    data = response.json()
st.write("Données brutes reçues :", data)
    # Transformer les données en DataFrame
df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "-", "-", "-", "-", "-", "-"
    ])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)

    return df

# Interface Streamlit
st.title("📊 Graphique BTC - Chandeliers (Multi Timeframes)")

# Sélection du timeframe
timeframe = st.selectbox("Sélectionnez le timeframe", ["5m", "15m", "1h"])

# Récupérer les données du timeframe sélectionné
df = get_candlestick_data(timeframe)

# Fonction pour afficher le graphique en chandeliers
def plot_candlestick(df, title):
    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"], high=df["high"], low=df["low"], close=df["close"],
        increasing_line_color="green", decreasing_line_color="red"
    )])
    fig.update_layout(title=title, xaxis_title="Temps", yaxis_title="Prix (USD)")
    return fig
# Afficher les données dans Streamlit pour vérifier
st.write("Données récupérées :", df)

# Afficher le graphique
st.plotly_chart(plot_candlestick(df, f"BTC/USD ({timeframe})"))
"Ajout de l'affichage des données pour debug"
