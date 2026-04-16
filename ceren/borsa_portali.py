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
                st.error("❌ Yetkisiz Giriş!")
else:
    st.sidebar.success("✅ Yetki Onaylandı.")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.title("🛰️ USTA BORSA PUSULASI v17.4")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    # --- TAB 1: DİNAMİK LİSTE ---
    with tabs[0]:
        st.subheader("Dinamik Liste Tarama")
        girdi = st.text_input("Hisseler (Örn: THYAO, SASA, BIGEN):", "BIGEN, THYAO, SASA", key="in127")
        if st.button("LİSTEYİ TARAMAYA BAŞLA 📡", key="btn127"):
            hisseler = [h.strip().upper() for h in girdi.split(",") if h.strip()]
            for s in hisseler:
                h_kod = s + ".IS" if "." not in s else s
                df = yf.download(h_kod, period="5d", progress=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                    fiyat_son = float(df['Close'].iloc[-1])
                    st.success(f"✅ {s}: {fiyat_son:.2f} TL")

    # --- TAB 2: AL-SAT SİNYAL ---
    with tabs[1]:
        st.subheader("v12.5: Al-Sat Sinyal Onayı")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="in125")
        if st.button("SİNYALİ SORGULA 🎯", key="btn125"):
            h = hisse_125.upper() + ".IS" if "." not in hisse_125 else hisse_125.upper()
            df = yf.download(h, period="6mo", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi_hesap = 100 - (100 / (1 + (gain / loss))).iloc[-1]
                st.info(f"📊 {h} RSI Değeri: {float(rsi_hesap):.2f}")
                fig, _ = mpf.plot(df.tail(60), type='candle', style='charles', returnfig=True)
                st.pyplot(fig)

    # --- TAB 3: GÜVENLİK ---
    with tabs[2]:
        st.subheader("v12.0: Güvenlik Sensörü")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="in120")
        if st.button("GÜVENLİK RAPORU AL 🛡️", key="btn120"):
            h = hisse_120.upper() + ".IS" if "." not in hisse_120 else hisse_120.upper()
            df = yf.download(h, period="1y", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                fiyat_güncel = float(df['Close'].iloc[-1])
                ema20_hesap = df['Close'].ewm(span=20).mean().iloc[-1]
                st.metric("Güncel Fiyat", f"{fiyat_güncel:.2f}")
                st.metric("EMA 20 Hattı", f"{float(ema20_hesap):.2f}")

    # --- TAB 4: ROD-BALANS ---
    with tabs[3]:
        st.subheader("v16.0: Rod-Balans (Destek/Direnç)")
        hisse_160 = st.text_input("Analiz Edilecek Hisse:", "BIGEN", key="in160")
        if st.button("SEVİYELERİ HESAPLA ⚖️", key="btn160"):
            h = hisse_160.upper() + ".IS" if "." not in hisse_160 else hisse_160.upper()
            df = yf.download(h, period="5d", progress=False)
            if not df.empty and len(df) >= 2:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                last = df.iloc[-2]
                hi, lo, cl = float(last['High']), float(last['Low']), float(last['Close'])
                p = (hi + lo + cl) / 3
                r1, s1 = (2 * p) - lo, (2 * p) - hi
                r2, s2 = p + (hi - lo), p - (hi - lo)
                st.markdown(f"### 📊 {h} Seviyeleri")
                c1, c2, c3 = st.columns(3)
                c1.metric("🚀 Direnç 2", f"{r2:.2f}")
                c1.metric("📈 Direnç 1", f"{r1:.2f}")
                c2.metric("⚖️ PİVOT", f"{p:.2f}")
                c3.metric("📉 Destek 1", f"{s1:.2f}")
                c3.metric("🚨 Destek 2", f"{s2:.2f}")
