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

    st.title("🛰️ USTA BORSA PUSULASI v17.0")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    # --- TAB 1: DİNAMİK LİSTE (TOPLU TARAMA) ---
    with tabs[0]:
        st.subheader("Dinamik Liste Tarama")
        girdi = st.text_input("Hisseler (Örn: THYAO, SASA, ASTOR):", "THYAO, SASA, FROTO", key="in127")
        if st.button("LİSTEYİ TARAMAYA BAŞLA 📡"):
            hisseler = [h.strip().upper() for h in girdi.split(",") if h.strip()]
            for s in hisseler:
                h_kod = s + ".IS" if "." not in s else s
                df = yf.download(h_kod, period="5d", progress=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                    fiyat = float(df['Close'].iloc[-1])
                    st.success(f"✅ {s}: {fiyat:.2f} TL")
                else:
                    st.error(f"❌ {s} verisi çekilemedi.")

    # --- TAB 2: AL-SAT SİNYAL (GRAFİK + RSI) ---
    with tabs[1]:
        st.subheader("v12.5: Al-Sat Sinyal Onayı")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="in125")
        if st.button("SİNYALİ SORGULA 🎯"):
            h = hisse_125.upper() + ".IS" if "." not in hisse_125 else hisse_125.upper()
            df = yf.download(h, period="6mo", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                # RSI Hesapla
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
                
                st.info(f"📊 {h} RSI Değeri: {float(rsi):.2f}")
                if rsi < 30: st.success("🟢 AŞIRI SATIM (Fırsat olabilir)")
                elif rsi > 70: st.warning("🔴 AŞIRI ALIM (Dikkatli ol)")
                
                fig, _ = mpf.plot(df.tail(60), type='candle', style='charles', returnfig=True, title=f"{h} Grafik")
                st.pyplot(fig)

    # --- TAB 3: GÜVENLİK (EMA 20 MESAFESİ) ---
    with tabs[2]:
        st.subheader("v12.0: Güvenlik Sensörü")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="in120")
        if st.button("GÜVENLİK RAPORU AL 🛡️"):
            h = hisse_120.upper() + ".IS" if "." not in hisse_120 else hisse_120.upper()
            df = yf.download(h, period="1y", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                fiyat = float(df['Close'].iloc[-1])
                ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
                fark = ((fiyat - ema20) / ema20) * 100
                
                st.metric("Güncel Fiyat", f"{fiyat:.2f}")
                st.metric("EMA 20 (Güvenlik Hattı)", f"{float(ema20):.2f}", f"%{float(fark):.2f}")
                if fiyat > ema20: st.success("✅ Güvenli Sürüş: Fiyat desteğin üstünde.")
                else: st.error("🚨 Riskli Bölge: Fiyat desteğin altında!")

    # --- TAB 4: ROD-BALANS (D/D) ---
    with tabs[3]:
        st.subheader("v16.0: Rod-Balans (Destek/Direnç)")
        hisse_160 = st.text_input("Analiz Edilecek Hisse:", "SASA", key="in160")
        if st.button("SEVİYELERİ HESAPLA ⚖️"):
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
                c
