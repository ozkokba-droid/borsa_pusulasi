import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def pusula_pro_v12_0_guvenlik():
    print("\n" + "="*85)
    print(" 🎯 BORSA PUSULASI v12.0: GÜVENLİK PAKETİ & PARK SENSÖRÜ ")
    print("="*85)
    
    hisse = input("Analiz Edilecek Hisse Kodu (Örn: ASELS): ").strip().upper()
    if not "." in hisse: hisse += ".IS"

    try:
        data = yf.download(hisse, period="1y", interval="1d", progress=False)
        if data.empty: return print("❌ Veri çekilemedi.")

        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

        # --- TEKNİK HESAPLAMALAR ---
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()
        
        # RSI Hesabı
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))

        fiyat = data['Close'].iloc[-1]
        e20 = data['EMA20'].iloc[-1]
        hacim_son = data['Volume'].iloc[-1]
        hacim_ort = data['Volume'].tail(10).mean() # Son 10 günün hacim ortalaması

        # --- GÜVENLİK SENSÖRLERİ (YENİ) ---
        mesafe_e20 = ((fiyat - e20) / e20) * 100
        hacim_dususu = hacim_son < hacim_ort # Hacim ortalamanın altındaysa yakıt bitiyor demektir.
        
        print(f"\n📊 {hisse} GÜVENLİK RAPORU:")
        print("-" * 85)
        print(f"💰 Fiyat: {fiyat:.2f} | 🌡️ RSI: {rsi:.2f} | ⛽ Hacim Gücü: {'ZAYIF' if hacim_dususu else 'GÜÇLÜ'}")
        print("-" * 85)

        # 1. BINADAN ÇAKILMA RİSKİ (TUZAK) SENSÖRÜ
        if fiyat > e20 and hacim_dususu and rsi > 65:
            print("🚨 TEHLİKE: BİNADAN ÇAKILMA RİSKİ! (Fiyat yükseliyor ama para girişi zayıf, RSI şişmiş.)")
            print("   > Öneri: Kemerleri bağla, stop seviyeni çok yakın tut!")
        
        # 2. HEDEFE GELDİ / SAT SENSÖRÜ
        elif rsi > 75:
            print("⚠️ UYARI: DOYUM NOKTASI! (Motor aşırı ısındı, RSI 75 üstü.)")
            print("   > Öneri: Buralar kâr realizasyonu için uygun olabilir, sağa çekip dinlen.")
            
        # 3. GÜVENLİ SÜRÜŞ SENSÖRÜ
        elif fiyat > e20 and not hacim_dususu:
            print("✅ DURUM: GÜVENLİ SÜRÜŞ. (Motor sesi sağlıklı, vites ileri.)")
        
        else:
            print("⚖️ DURUM: BELİRSİZ / RÖLANTİ. (Trendin netleşmesini bekle.)")

        print("-" * 85)
        print(f"🔹 Mavi Çizgi (EMA 20) Desteği: {e20:.2f}")
        print(f"📏 Destekle Mesafe: %{mesafe_e20:.2f}")
        print("-" * 85)

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    pusula_pro_v12_0_guvenlik()