import yfinance as yf
import pandas as pd

def borsa_pusulasi_v13_3():
    print("\n" + "="*60)
    print(" 🎯 v13.3: %5 KAR TAKİP PANELİ (MANUEL GİRİŞ) ")
    print("="*60)
    
    hisseler = ["EKGYO", "SAFKR", "GWIND"]
    alis_fiyatlari = {}

    # --- FİYAT GİRİŞLERİ ---
    for h in hisseler:
        try:
            inp = input(f"👉 {h} Alış Fiyatın: ")
            alis_fiyatlari[h] = float(inp.replace(",", "."))
        except:
            alis_fiyatlari[h] = 0.0

    print("\n" + "-"*75)
    header = f"{'HİSSE':<10} | {'ALIŞ':<8} | {'GÜNCEL':<8} | {'KAR%':<8} | {'DURUM'}"
    print(header)
    print("-" * 75)

    for hisse, alis in alis_fiyatlari.items():
        if alis == 0: continue
        try:
            ticker = yf.Ticker(hisse + ".IS")
            data = ticker.history(period="1d")
            if data.empty:
                data = yf.download(hisse + ".IS", period="1d", progress=False)

            guncel = data['Close'].iloc[-1]
            fark = ((guncel - alis) / alis) * 100
            
            # Durum Belirleme
            if fark >= 5.0:
                sinyal = "🎉 HEDEF TAMAM!"
            elif fark <= -3.0:
                sinyal = "⚠️ STOP-LOSS!"
            else:
                sinyal = "🚀 YOLDA"

            # Satırı parçalı yazdıralım ki hata vermesin
            satir = f"{hisse:<10} | {alis:>8.2f} | {guncel:>8.2f} | %{fark:>6.2f} | {sinyal}"
            print(satir)
        except:
            print(f"{hisse:<10} | Veri çekme hatası!")

    print("\n💡 Usta Tavsiyesi: Fiyatları girince ENTER'a bas, beklemeye geç!")

if __name__ == "__main__":
    borsa_pusulasi_v13_3()