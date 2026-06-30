from binance.client import Client
from binance.enums import *
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

api_key = "SUA_API_KEY_TESTNET"
api_secret = "SEU_API_SECRET_TESTNET"

client = Client(api_key, api_secret, testnet=True)

# 1. Obter dados históricos
klines = client.get_historical_klines("XRPUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

df = pd.DataFrame(klines, columns=[
    "timestamp","open","high","low","close","volume",
    "close_time","quote_asset_volume","trades","taker_buy_base",
    "taker_buy_quote","ignore"
])

df["close"] = df["close"].astype(float)

# 2. Calcular indicadores técnicos
df["RSI"] = ta.rsi(df["close"], length=14)
df["SMA10"] = df["close"].rolling(10).mean()
df["SMA30"] = df["close"].rolling(30).mean()

# 3. Simulação de operações
usdt = 1000
xrp = 0
trades = []

for i in range(30, len(df)):
    price = df["close"].iloc[i]
    rsi = df["RSI"].iloc[i]
    sma10 = df["SMA10"].iloc[i]
    sma30 = df["SMA30"].iloc[i]

    # Estratégia RSI
    if rsi < 30 and usdt >= price * 10:
        usdt -= price * 10
        xrp += 10
        trades.append(("COMPRA", price, usdt, xrp))
    elif rsi > 70 and xrp >= 10:
        usdt += price * 10
        xrp -= 10
        trades.append(("VENDA", price, usdt, xrp))

    # Estratégia Médias Móveis
    if sma10 > sma30 and usdt >= price * 10:
        usdt -= price * 10
        xrp += 10
        trades.append(("COMPRA", price, usdt, xrp))
    elif sma10 < sma30 and xrp >= 10:
        usdt += price * 10
        xrp -= 10
        trades.append(("VENDA", price, usdt, xrp))

# 4. Resultado final
saldo_final = usdt + xrp * df["close"].iloc[-1]
print("Saldo final:", saldo_final)

# 5. Gráfico
plt.figure(figsize=(12,6))
plt.plot(df["close"], label="Preço XRP", color="blue")
plt.plot(df["SMA10"], label="SMA10", color="green")
plt.plot(df["SMA30"], label="SMA30", color="red")
plt.legend()
plt.show()
