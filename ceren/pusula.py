import yfinance as yf
import mplfinance as mpf
import pandas as pd

def borsa_pusulasi_v41():
    print("\n" + "="*50)
    print(" 🎯 BORSA PUSULASI v4.1: NET GÖSTERGE PANELİ ")
    print("="*50)
    
    hisse = input("Analiz edilecek hisse (Örn: ASELS): ").strip().upper()
    if not "." in hisse: hisse += ".IS"

    try:
        data = yf.download(hisse, period="6mo", interval="1d")
        if data.empty: return

        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

        # RSI ve EMA Hesaplama
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        data['RSI'] = 100 - (100 / (1 + (gain / loss)))
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()

        son_fiyat = data['Close'].iloc[-1]
        son_rsi = data['RSI'].iloc[-1]
        son_ema = data['EMA20'].iloc[-1]

        print(f"\n--- {hisse} CANLI VERİ PANELİ ---")
        print(f"💰 Güncel Fiyat : {son_fiyat:.2f} TL")
        print(f"🔵 EMA 20 Değeri: {son_ema:.2f} TL")
        print(f"📊 RSI (Hararet): {son_rsi:.2f}")

        # --- DURUM TESPİTİ ---
        print("\n--- USTA YORUMU ---")
        if son_fiyat > son_ema:
            fark = ((son_fiyat / son_ema) - 1) * 100
            print(f"✅ ÜSTÜNDE: Fiyat mavi çizginin %{fark:.2f} üzerinde. Vites İleri!")
        else:
            fark = ((son_ema / son_fiyat) - 1) * 100
            print(f"❌ ALTINDA : Fiyat mavi çizginin %{fark:.2f} altında. Beklemede kal!")

        if son_rsi < 35:
            print("💎 FIRSAT  : Hisse çok ucuz (RSI düşük), kırılım gelirse patlar!")

        # Grafik
        ap = [mpf.make_addplot(data['EMA20'], color='blue', width=1.5)]
        mpf.plot(data, type='candle', style='charles', addplot=ap,
                 title=f"\n{hisse} Analiz", volume=True)

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    borsa_pusulasi_v41()