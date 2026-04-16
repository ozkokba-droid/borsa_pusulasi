import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf

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
            else:
                st.error("❌ Şifre yanlış usta!")
else:
    st.sidebar.success("✅ Yetki Onaylandı.")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.title("🛰️ USTA BORSA PUSULASI v16.8")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    # --- TAB 1: LİSTE ---
    with tabs[0]:
        st.subheader("Dinamik Liste Tarama")
        girdi_127 = st.text_input("Hisseler:", "THYAO, SASA, FROTO", key="in127")
        if st.button("TARAMAYI BAŞLAT 📡"):
            izleme = [h.strip().upper() for h in girdi_127.split(",") if h.strip()]
            for sembol in izleme:
                h_kod = sembol + ".IS" if "." not in sembol else sembol
                d = yf.download(h_kod, period="1mo", progress=False)
                if not d.empty:
                    f = float(d['Close'].iloc[-1])
                    st.success(f"✅ {sembol}: {f:.2f} TL")

    # --- TAB 2: SİNYAL ---
    with tabs[1]:
        st.subheader("Al-Sat Sinyal Kontrol")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="in125")
        if st.button("SİNYALİ SORGULA 🎯"):
            h = hisse_125 + ".IS" if "." not in hisse_125 else hisse_125
            d = yf.download(h, period="6mo", progress=False)
            if not d.empty:
                f = float(d['Close'].iloc[-1])
                st.info(f"🚀 {h} Son Fiyat: {f:.2f} TL | Sinyal: Aktif")
                fig, _ = mpf.plot(d.tail(60), type='candle', style='charles', returnfig=True)
                st.pyplot(fig)

    # --- TAB 3: GÜVENLİK ---
    with tabs[2]:
        st.subheader("Güvenlik Sensörü")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="in120")
        if st.button("GÜVENLİK RAPORU 🛡️"):
            h = hisse_120 + ".IS" if "." not in hisse_120 else hisse_120
            d = yf.download(h, period="1y", progress=False)
            if not d.empty:
                f = float(d['Close'].iloc[-1])
                e20 = d['Close'].ewm(span=20).mean().iloc[-1]
                st.warning(f"📊 {h} Fiyat: {f:.2f} | EMA20 Desteği: {float(e20):.2f}")

    # --- TAB 4: ROD-BALANS (DESTEK/DİRENÇ) ---
    with tabs[3]:
        st.subheader("Rod-Balans (Destek/Direnç)")
        hisse_160 = st.text_input("Analiz Edilecek Hisse:", "THYAO", key="in160")
        if st.button("SEVİYELERİ HESAPLA ⚖️"):
            h_kod = hisse_160.upper() + ".IS" if "." not in hisse_160 else hisse_160.upper()
            df = yf.download(h_kod, period="5d", progress=False)
            
            if not df.empty and len(df) >= 2:
                # Veri temizleme
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                
                last_day = df.iloc[-2] # Bir önceki günün verisi
                h, l, c = float(last_day['High']), float(last_day['Low']), float(last_day['Close'])
                
                # Pivot Hesaplamaları
                pivot = (h + l + c) / 3
                r1 = (2 * pivot) - l
                s1 = (2 * pivot) - h
                r2 = pivot + (h - l)
                s2 = pivot - (h - l)
                
                # EKRANA BASMA (Kutucuklarla)
                st.markdown(f"### 📊 {h_kod} Analiz Sonuçları")
                col1, col2, col3 = st.columns(3)
