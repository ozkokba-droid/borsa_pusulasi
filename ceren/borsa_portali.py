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

    st.title("🛰️ USTA BORSA PUSULASI v18.7")
    st.write("---")
    
    tabs = st.tabs(["⚠️ v12.0 GÜVENLİK", "🎯 v12.5 AL-SAT", "🚀 v12.7 GARAJ", "💰 v13.3 KÂR", "⚙️ v12.1 ŞANZIMAN"])

    # --- TAB 1: v12.0 GÜVENLİK ---
    with tabs[0]:
        st.subheader("⚠️ v12.0: Güvenlik Paketi & Park Sensörü")
        h120 = st.text_input("Hisse Sorgula (Örn: ASELS):", "ASELS", key="t120_v187")
        if st.button("SENSÖRÜ ÇALIŞTIR 🛡️"):
            f = io.StringIO()
            with redirect_stdout(f):
                h = h120.strip().upper() + ".IS" if "." not in h120 else h120.upper()
                try:
                    d = yf.download(h, period="1y", progress=False)
                    if not d.empty:
                        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
                        e20 = d['Close'].ewm(span=20).mean().iloc[-1]
                        fiyat = d['Close'].iloc[-1]
                        print(f"📊 {h} RAPORU:\n💰 Fiyat: {fiyat:.2f}\n🔹 EMA20: {e20:.2f}")
                        if fiyat > e20: print("✅ DURUM: GÜVENLİ SÜRÜŞ. (Motor sesi sağlıklı.)")
                        else: print("🚨 TEHLİKE: ŞANZIMAN DAĞILDI! (Kemerleri bağla.)")
                    else: print("❌ Veri Hatası: Hisse bulunamadı.")
                except Exception as e: print(f"❌ Hata: {str(e)}")
            st.code(f.getvalue())

    # --- TAB 2: v12.5 AL-SAT ---
    with tabs[1]:
        st.subheader("🎯 v12.5: Profesyonel Sinyal Onayı")
        h125 = st.text_input("Hisse Sorgula (Örn: TOASO):", "TOASO", key="t125_v187")
        if st.button("SİNYALİ YAKALA 📡"):
            f = io.StringIO()
            with redirect_stdout(f):
                h = h125.strip().upper() + ".IS" if "." not in h
