import yfinance as yf
import pandas as pd
import mplfinance as mpf

def borsa_pusulasi_v12_1_fix():
    print("\n" + "="*65)
    print(" 🚀 BORSA PUSULASI v12.1: BOYUT AYARI & ÜÇLÜ ŞANZIMAN ")
    print("="*65)
    
    hisse = input("Analiz Edilecek Hisse (Örn: ASTOR): ").strip().upper()
    if not "." in hisse: hisse += ".IS"

    try:
        # 1 yıllık veri çekiyoruz (Ortalamaların sağlıklı hesaplanması için)
        data = yf.download(hisse, period="1y", interval="1d", progress=False)
        if data.empty: return
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)

        # --- ŞANZIMAN AYARLARI ---
        data['EMA20']  = data['Close'].ewm(span=20, adjust=False).mean()  # 🔵 Mavi: Kısa
        data['EMA50']  = data['Close'].ewm(span=50, adjust=False).mean()  # 🟡 Sarı: Orta
        data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean() # 🔴 Kırmızı: Uzun (Şasi)

        # --- HATAYI ÖNLEYEN BOYUT AYARI ---
        # Sadece son 100 günü kesip alıyoruz ki grafik çizgileriyle mumlar çakışmasın
        plot_data = data.tail(100).copy()

        # Grafiğe eklenecek yan modüller
        apds = [
            mpf.make_addplot(plot_data['EMA20'], color='blue', width=1.2),
            mpf.make_addplot(plot_data['EMA50'], color='orange', width=1.2),
            mpf.make_addplot(plot_data['EMA200'], color='red', width=1.8)
        ]

        # Ana Grafik Çizimi
        mpf.plot(plot_data, type='candle', style='charles', 
                 addplot=apds,
                 title=f"\n{hisse} - v12.1 ŞANZIMAN KONTROLÜ",
                 ylabel='Fiyat (TL)',
                 volume=True,
                 figsize=(12, 8))

        # --- USTA ÖZETİ ---
        fiyat = plot_data['Close'].iloc[-1]
        print(f"\n📋 {hisse} EKSPERTİZ RAPORU:")
        print(f"💰 Güncel Fiyat: {fiyat:.2f}")
        
        if fiyat > plot_data['EMA20'].iloc[-1]: print("✅ Kısa Vade: Vites İleri!")
        else: print("❌ Kısa Vade: Şanzıman Dağıldı!")

        if fiyat > plot_data['EMA200'].iloc[-1]: print("✅ Uzun Vade: Şasi Sağlam, Korkma!")
        else: print("❌ Uzun Vade: Motor Rektefiye İstiyor!")

    except Exception as e:
        print(f"⚠️ Arıza tespiti başarısız: {e}")

if __name__ == "__main__":
    borsa_pusulasi_v12_1_fix()