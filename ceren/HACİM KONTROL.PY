import yfinance as yf
import pandas as pd

def borsa_pusulasi_v12_7_dinamik_liste():
    print("\n" + "="*75)
    print(" 🎯 v12.7: 'OTOMATİK GARAJ' - DİNAMİK LİSTE TARAMA MODÜLÜ ")
    print("="*75)
    
    # --- GİRİŞ PANELİ ---
    girdi = input("🔍 Taranacak Hisseleri Gir (Arada virgül olsun, Örn: ASTOR, THYAO, SASA): ")
    
    # Kullanıcının girdiği listeyi temizleyip parçalıyoruz
    izleme_listesi = [h.strip().upper() for h in girdi.split(",") if h.strip()]
    
    if not izleme_listesi:
        print("❌ Usta, herhangi bir hisse girmedin! Dükkan boş kaldı.")
        return

    print(f"\n📋 {len(izleme_listesi)} Adet Makine Kanala Alınıyor...\n")
    print(f"{'HİSSE':<10} | {'FİYAT':<8} | {'HACİM GÜCÜ':<12} | {'DURUM'}")
    print("-" * 65)

    for sembol in izleme_listesi:
        hisse_kod = sembol + ".IS" if not "." in sembol else sembol
        try:
            # Veri çekme (En güncel haliyle)
            data = yf.download(hisse_kod, period="1mo", interval="1d", progress=False)
            if data.empty:
                print(f"{sembol:<10} | {'❌ Veri Yok':<35}")
                continue
                
            if isinstance(data.columns, pd.MultiIndex): 
                data.columns = data.columns.get_level_values(0)

            # --- TEKNİK ANALİZ ---
            ema20 = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
            fiyat = data['Close'].iloc[-1]
            hacim_ort = data['Volume'].rolling(window=10).mean().iloc[-1]
            hacim_bugun = data['Volume'].iloc[-1]
            hacim_gucu = (hacim_bugun / hacim_ort) * 100

            # --- SİNYAL MANTIĞI ---
            if fiyat > ema20 and hacim_gucu > 120:
                durum = "🟢 GÜÇLÜ AL (Full Depo!)"
            elif fiyat > ema20 and hacim_gucu <= 120:
                durum = "🟡 ZAYIF AL (Yakıt Az)"
            elif fiyat < ema20 and hacim_gucu > 120:
                durum = "🟠 DİKKAT (Boşa Gaz Basıyor)"
            else:
                durum = "🔴 SAT (Motor Soğuk)"

            print(f"{sembol:<10} | {fiyat:>8.2f} | %{hacim_gucu:>10.0f} | {durum}")

        except Exception as e:
            print(f"{sembol:<10} | ⚠️ Hata: {str(e)[:20]}...")

    print("\n💡 Usta Tavsiyesi: Sadece 'Yeşil' yanan makinelerle %5 hedefine gazla!")

if __name__ == "__main__":
    borsa_pusulasi_v12_7_dinamik_liste()