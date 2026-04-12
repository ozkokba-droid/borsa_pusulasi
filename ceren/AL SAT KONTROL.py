import yfinance as yf
import pandas as pd
import mplfinance as mpf

def borsa_pusulasi_v12_5_alsat():
    print("\n" + "="*75)
    print(" 🎯 v12.5: PROFESYONEL GÜNLÜK AL-SAT & SİNYAL ONAY MODÜLÜ ")
    print("="*75)
    
    hisse = input("Analiz Edilecek Hisse (Örn: TOASO): ").strip().upper()
    if not "." in hisse: hisse += ".IS"

    try:
        # Günlük işlemler için daha kısa ama detaylı veri (6 aylık)
        data = yf.download(hisse, period="6mo", interval="1d", progress=False)
        if data.empty: return
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)

        # --- GÖSTERGELER ---
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        weights = range(1, 51)
        data['WMA50'] = data['Close'].rolling(50).apply(lambda x: (x * weights).sum() / sum(weights), raw=True)
        
        # RSI (Hararet)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        data['RSI'] = 100 - (100 / (1 + (gain / loss)))

        # Hacim Ortalaması (Yakıt Kontrolü)
        data['Hacim_Ort'] = data['Volume'].rolling(window=10).mean()

        # --- SİNYAL ONAY MANTIĞI ---
        fiyat = data['Close'].iloc[-1]
        mavi = data['EMA20'].iloc[-1]
        sari = data['WMA50'].iloc[-1]
        rsi = data['RSI'].iloc[-1]
        hacim_son = data['Volume'].iloc[-1]
        hacim_ort = data['Hacim_Ort'].iloc[-1]

        print(f"\n🚀 {hisse} İÇİN GÜNLÜK AL-SAT ANALİZİ:")
        print("-" * 55)

        # AL-SAT SİNYAL PUANLAMASI
        sinyal = "⚖️ BEKLE (Nötr)"
        onay_mesaji = "Motor rölantide, net bir hareket yok."

        # ALIM KOŞULU (Vites İleri)
        if fiyat > mavi and rsi > 50 and rsi < 70:
            if hacim_son > hacim_ort:
                sinyal = "🟢 GÜÇLÜ AL (Onaylı)"
                onay_mesaji = "Fiyat mavi üstünde, hararet ideal ve depoda yakıt (hacim) var!"
            else:
                sinyal = "🟡 ZAYIF AL (Yakıt Az)"
                onay_mesaji = "Fiyat iyi ama hacim düşük, her an stop edebilir."

        # SATIM KOŞULU (El Freni)
        elif fiyat < mavi or rsi > 75:
            if fiyat < mavi and fiyat < sari:
                sinyal = "🔴 GÜÇLÜ SAT (Binadan Çakılma)"
                onay_mesaji = "Tüm destekler kırıldı, şanzıman dağıldı. Kaç!"
            else:
                sinyal = "🟠 SAT/KAR AL (Motor Isındı)"
                onay_mesaji = "Fiyat hala yukarda ama hararet (RSI) çok yüksek, karı cebe koy."

        print(f"📡 SİNYAL DURUMU : {sinyal}")
        print(f"📢 USTA YORUMU  : {onay_mesaji}")
        print("-" * 55)
        print(f"💰 Fiyat: {fiyat:.2f} | 🌡️ RSI: {rsi:.2f} | ⚓ Hacim: %{((hacim_son/hacim_ort)*100):.0f}")

        # Görsel Sinyal Grafiği
        mpf.plot(data.tail(60), type='candle', style='charles', 
                 addplot=[mpf.make_addplot(data['EMA20'].tail(60), color='blue'),
                          mpf.make_addplot(data['WMA50'].tail(60), color='orange')],
                 title=f"\n{hisse} - GÜNLÜK SİNYAL PANELİ", figsize=(12, 7))

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    borsa_pusulasi_v12_5_alsat()
    