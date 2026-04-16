import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import io
from contextlib import redirect_stdout

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")

# --- GÜVENLİK KİLİDİ ---
if "giris_basarili" not in st.session_state:
    st.session_state["giris_basarili"] = False

if not st.session_state["giris_basarili"]:
    st.markdown("<h1 style='text-align: center;'>🛡️ USTA TERMİNALİ GİRİŞ</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        kullanici = st.text_input("Kullanıcı Adı:", key="u_in")
        sifre = st.text_input("Şifre:", type="password", key="p_in")
        if st.button("Dükkanı Aç 🔑"):
            if kullanici == "usta" and sifre.lower() == "usta123":
                st.session_state["giris_basarili"] = True
                st.rerun()
            else: st.error("❌ Yetkisiz Giriş!")
else:
    st.sidebar.success("✅ Yetki Onaylandı.")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.title("🛰️ USTA BORSA PUSULASI v18.5")
    
    tabs = st.tabs(["⚠️ v12.0 GÜVENLİK", "🎯 v12.5 AL-SAT", "🚀 v12.7 GARAJ", "💰 v13.3 KÂR", "⚙️ v12.1 ŞANZIMAN"])

    # --- TAB 1: v12.0 GÜVENLİK (PARK SENSÖRÜ) ---
    with tabs[0]:
        st.subheader("⚠️ v12.0: Güvenlik Paketi & Park Sensörü")
        h120 = st.text_input("Hisse (Örn: ASELS):", "ASELS", key="t120")
        if st.button("GÜVENLİK RAPORU AL 🛡️"):
            f = io.StringIO()
            with redirect_stdout(f):
                h = h120.strip().upper() + ".IS" if "." not in h120 else h120.upper()
                data = yf.download(h, period="1y", progress=False)
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
                    data['EMA20'] = data['Close'].ewm(span=20).mean()
                    delta = data['Close'].diff(); gain = (delta.where(delta > 0, 0)).rolling(14).mean(); loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                    rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
                    fiyat, e20 = data['Close'].iloc[-1], data['EMA20'].iloc[-1]
                    h_son, h_ort = data['Volume'].iloc[-1], data['Volume'].tail(10).mean()
                    print(f"📊 {h} RAPOR: Fiyat {fiyat:.2f} | RSI: {rsi:.2f} | Hacim: {'ZAYIF' if h_son < h_ort else 'GÜÇLÜ'}")
                    if fiyat > e20 and h_son < h_ort and rsi > 65: print("🚨 TEHLİKE: BİNADAN ÇAKILMA RİSKİ!")
                    elif rsi > 75: print("⚠️ UYARI: DOYUM NOKTASI (Motor Isındı!)")
                    elif fiyat > e20: print("✅ DURUM: GÜVENLİ SÜRÜŞ.")
                    else: print("⚖️ DURUM: BELİRSİZ / RÖLANTİ.")
                else: print("❌ Veri Hatası")
            st.code(f.getvalue())

    # --- TAB 2: v12.5 AL-SAT SİNYAL ONAY ---
    with tabs[1]:
        st.subheader("🎯 v12.5: Profesyonel Sinyal Onayı")
        h125 = st.text_input("Hisse (Örn: TOASO):", "TOASO", key="t125")
        if st.button("SİNYAL SORGULA 📡"):
            f = io.StringIO()
            with redirect_stdout(f):
                h = h125.strip().upper() + ".IS" if "." not in h125 else h125.upper()
