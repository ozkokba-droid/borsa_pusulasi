import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import io
from contextlib import redirect_stdout

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")
st.title("🛡️ USTA BORSA PUSULASI: ÜÇLÜ TERMİNAL v15.5")

# MODÜLLERİ SEKMELERE AYIRDIK
tab1, tab2, tab3 = st.tabs(["🚀 v12.7 DİNAMİK LİSTE", "🎯 v12.5 AL-SAT SİNYAL", "⚠️ v12.0 GÜVENLİK SENSÖRÜ"])

# --- YARDIMCI FONKSİYON: TERMİNAL ÇIKTISINI YAKALAMA ---
def terminal_calistir(func, input_val):
    f = io.StringIO()
    # Senin input() fonksiyonunu Streamlit'in girdisiyle simüle ediyoruz
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: input_val
    
    with redirect_stdout(f):
        func()
    
    builtins.input = original_input
    return f.getvalue()

# --- SEKME 1: v12.7 DİNAMİK LİSTE ---
with tab1:
    st.header("v12.7: 'OTOMATİK GARAJ'")
    girdi_127 = st.text_input("🔍 Taranacak Hisseleri Gir (Örn: ASTOR, THYAO, SASA):", "THYAO, SASA, ASTOR", key="k127")
    if st.button("LİSTEYİ TARAMAYA BAŞLA 📡"):
        # Senin orijinal fonksiyonun
        def borsa_pusulasi_v12_7_dinamik_liste():
            print("\n" + "="*75)
            print(" 🎯 v12.7: 'OTOMATİK GARAJ' - DİNAMİK LİSTE TARAMA MODÜLÜ ")
            print("="*75)
            girdi = girdi_127
            izleme_listesi = [h.strip().upper() for h in girdi.split(",") if h.strip()]
            if not izleme_listesi: return
            print(f"\n📋 {len(izleme_listesi)} Adet Makine Kanala Alınıyor...\n")
            print(f"{'HİSSE':<10} | {'FİYAT':<8} | {'HACİM GÜCÜ':<12} | {'DURUM'}")
            print("-" * 65)
            for sembol in izleme_listesi:
                hisse_kod = sembol + ".IS" if not "." in sembol else sembol
                try:
                    data = yf.download(hisse_kod, period="1mo", interval="1d", progress=False)
                    if data.empty: continue
                    if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
                    ema20 = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
                    fiyat = data['Close'].iloc[-1]
                    hacim_ort = data['Volume'].rolling(window=10).mean().iloc[-1]
                    hacim_bugun = data['Volume'].iloc[-1]
                    hacim_gucu = (hacim_bugun / hacim_ort) * 100
                    if fiyat > ema20 and hacim_gucu > 120: durum = "🟢 GÜÇLÜ AL (Full Depo!)"
                    elif fiyat > ema20 and hacim_gucu <= 120: durum = "🟡 ZAYIF AL (Yakıt Az)"
                    elif fiyat < ema20 and hacim_gucu > 120: durum = "🟠 DİKKAT (Boşa Gaz Basıyor)"
                    else: durum = "🔴 SAT (Motor Soğuk)"
                    print(f"{sembol:<10} | {fiyat:>8.2f} | %{hacim_gucu:>10.0f} | {durum}")
                except: continue
            print("\n💡 Usta Tavsiyesi: Sadece 'Yeşil' yanan makinelerle %5 hedefine gazla!")

        st.code(terminal_calistir(borsa_pusulasi_v12_7_dinamik_liste, girdi_127), language='text')

# --- SEKME 2: v12.5 AL-SAT SİNYAL ---
with tab2:
    st.header("v12.5: GÜNLÜK AL-SAT & SİNYAL ONAY")
    hisse_125 = st.text_input("Analiz Edilecek Hisse (Örn: TOASO):", "TOASO", key="k125")
    if st.button("SİNYAL ONAYI AL 🎯"):
        def borsa_pusulasi_v12_5_alsat():
            # Senin 12.5 kodun (Grafik kısmı Streamlit'e uyarlandı)
            hisse = hisse_125
            if not "." in hisse: hisse += ".IS"
            try:
                data = yf.download(hisse, period="6mo", interval="1d", progress=False)
                if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
                data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
                weights = range(1, 51)
                data['WMA50'] = data['Close'].rolling(50).apply(lambda x: (x * weights).sum() / sum(weights), raw=True)
                delta = data['Close'].diff(); gain = (delta.where(delta > 0, 0)).rolling(window=14).mean(); loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                data['RSI'] = 100 - (100 / (1 + (gain / loss))); data['Hacim_Ort'] = data['Volume'].rolling(window=10).mean()
                fiyat = data['Close'].iloc[-1]; rsi = data['RSI'].iloc[-1]; hacim_son = data['Volume'].iloc[-1]; hacim_ort = data['Hacim_Ort'].iloc[-1]
                print(f"🚀 {hisse} İÇİN GÜNLÜK ANALİZ:\n" + "-"*40)
                if fiyat > data['EMA20'].iloc[-1] and 50 < rsi < 70: sinyal = "🟢 GÜÇLÜ AL" if hacim_son > hacim_ort else "🟡 ZAYIF AL"
                elif fiyat < data['EMA20'].iloc[-1] or rsi > 75: sinyal = "🔴 GÜÇLÜ SAT" if fiyat < data['WMA50'].iloc[-1] else "🟠 SAT/KAR AL"
                else: sinyal = "⚖️ BEKLE (Nötr)"
                print(f"📡 SİNYAL: {sinyal}\n💰 Fiyat: {fiyat:.2f} | 🌡️ RSI: {rsi:.2f}")
                st.session_state['data_125'] = data
            except Exception as e: print(f"Hata: {e}")

        st.code(terminal_calistir(borsa_pusulasi_v12_5_alsat, hisse_125), language='text')
        if 'data_125' in st.session_state:
            fig, ax = mpf.plot(st.session_state['data_125'].tail(60), type='candle', style='charles', returnfig=True, figsize=(10, 5))
            st.pyplot(fig)

# --- SEKME 3: v12.0 GÜVENLİK ---
with tab3:
    st.header("v12.0: GÜVENLİK & PARK SENSÖRÜ")
    hisse_120 = st.text_input("Analiz Edilecek Hisse Kodu (Örn: ASELS):", "ASELS", key="k120")
    if st.button("GÜVENLİK RAPORU AL 🛡️"):
        def pusula_pro_v12_0_guvenlik():
            hisse = hisse_120
            if not "." in hisse: hisse += ".IS"
            data = yf.download(hisse, period="1y", interval="1d", progress=False)
            if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
            data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            fiyat = data['Close'].iloc[-1]; e20 = data['EMA20'].iloc[-1]
            hacim_son = data['Volume'].iloc[-1]; hacim_ort = data['Volume'].tail(10).mean()
            print(f"📊 {hisse} GÜVENLİK RAPORU:\n" + "-"*40)
            if fiyat > e20 and hacim_son < hacim_ort: print("🚨 TEHLİKE: BİNADAN ÇAKILMA RİSKİ!")
            elif fiyat > e20: print("✅ DURUM: GÜVENLİ SÜRÜŞ")
            else: print("⚖️ DURUM: BELİRSİZ / RÖLANTİ")
            print(f"📏 Destekle Mesafe: %{(((fiyat - e20) / e20) * 100):.2f}")

        st.code(terminal_calistir(pusula_pro_v12_0_guvenlik, hisse_120), language='text')
        import streamlit as st
# ... diğer kütüphaneler (yf, pd vs.) aynı kalacak ...

# --- GÜVENLİK KİLİDİ ---
def giris_kontrol():
    if "giris_basarili" not in st.session_state:
        st.session_state["giris_basarili"] = False

    if not st.session_state["giris_basarili"]:
        st.title("🛡️ USTA TERMİNALİ - GÜVENLİ GİRİŞ")
        kullanici = st.text_input("Kullanıcı Adı:")
        sifre = st.text_input("Şifre:", type="password")
        
        if st.button("Dükkanı Aç"):
            # BURADAN KENDİ ŞİFRENİ AYARLAYABİLİRSİN USTA
            if kullanici == "usta" and sifre == "usta123":
                st.session_state["giris_basarili"] = True
                st.rerun()
            else:
                st.error("❌ Yetkisiz Giriş! Şifreyi yanlış girdin usta.")
        return False
    return True

# --- ANA SİSTEM ---
if giris_kontrol():
    # BURADAN SONRASI SENİN ESKİ KODLARININ TAMAMI (Tablar, Modüller vs.)
    st.sidebar.success("✅ Yetki Onaylandı. Hoş geldin Usta!")
    
    # ... (Buraya tab1, tab2, tab3 ve o uzun fonksiyonlar gelecek)
