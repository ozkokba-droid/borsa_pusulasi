import streamlit as st
import yfinance as yf
import pandas as pd
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
            else:
                st.error("❌ Şifre yanlış!")
else:
    st.sidebar.success("✅ Yetki Onaylandı.")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.title("🛰️ USTA BORSA PUSULASI v17.5")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    # TERMINAL ÇIKTISI YAKALAYICI
    def terminal_ekrani(fonksiyon, *args):
        f = io.StringIO()
        with redirect_stdout(f):
            fonksiyon(*args)
        return f.getvalue()

    # --- TAB 1: DİNAMİK LİSTE ---
    with tabs[0]:
        st.subheader("Dinamik Liste Tarama")
        girdi = st.text_input("Hisseler:", "THYAO, SASA, BIGEN", key="in127")
        if st.button("LİSTEYİ TARAMAYA BAŞLA 📡"):
            def tarama_logic():
                hisseler = [h.strip().upper() for h in girdi.split(",") if h.strip()]
                print(f"{'HİSSE':<10} | {'FİYAT':<10} | {'DURUM'}")
                print("-" * 35)
                for s in hisseler:
                    h_kod = s + ".IS" if "." not in s else s
                    df = yf.download(h_kod, period="1d", progress=False)
                    if not df.empty:
                        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                        fiyat = df['Close'].iloc[-1]
                        print(f"{s:<10} | {fiyat:>10.2f} | 🟢 AKTİF")
                    else:
                        print(f"{s:<10} | {'---':>10} | ❌ HATA")
            
            st.code(terminal_ekrani(tarama_logic))

    # --- TAB 2: AL-SAT SİNYAL ---
    with tabs[1]:
        st.subheader("v12.5: Al-Sat Sinyal Onayı")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="in125")
        if st.button("SİNYALİ SORGULA 🎯"):
            def sinyal_logic():
                h = hisse_125.upper() + ".IS" if "." not in hisse_125 else hisse_125.upper()
                df = yf.download(h, period="6mo", progress=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                    delta = df['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
                    print(f"ANALİZ RAPORU: {h}")
                    print("-" * 30)
                    print(f"SON FİYAT : {df['Close'].iloc[-1]:.2f}")
                    print(f"RSI DEĞERİ: {rsi:.2f}")
                    print(f"SİNYAL    : {'GÜÇLÜ' if rsi < 50 else 'DİKKAT'}")
            
            st.code(terminal_ekrani(sinyal_logic))

    # --- TAB 3: GÜVENLİK ---
    with tabs[2]:
        st.subheader("v12.0: Güvenlik Sensörü")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="in120")
        if st.button("GÜVENLİK RAPORU AL 🛡️"):
            def guvenlik_logic():
                h = hisse_120.upper() + ".IS" if "." not in hisse_120 else hisse_120.upper()
                df = yf.download(h, period="1y", progress=False)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                    fiyat = df['Close'].iloc[-1]
                    ema20 = df['Close'].ewm(span=20).mean().iloc[-1]
                    print(f"GÜVENLİK KONTROLÜ: {h}")
                    print("-" * 30)
                    print(f"MEVCUT FİYAT: {fiyat:.2f}")
                    print(f"EMA 20 HATTI: {ema20:.2f}")
                    print(f"MESAFE      : %{((fiyat-ema20)/ema20)*100:.2f}")
                    print(f"DURUM       : {'GÜVENLİ' if fiyat > ema20 else '🚨 RİSKLİ'}")
            
            st.code(terminal_ekrani(guvenlik_logic))

    # --- TAB 4: ROD-BALANS ---
    with tabs[3]:
        st.subheader("v16.0: Rod-Balans (Destek/Direnç)")
        hisse_160 = st.text_input("Hisse:", "SASA", key="in160")
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
                
                # Burayı metrik olarak bırakıyorum çünkü görseli çok iyi ama istersen st.code yapabilirim.
                st.markdown(f"### 📊 {h} Analiz")
                c1, c2, c3 = st.columns(3)
                c1.metric("🚀 Direnç 2", f"{r2:.2f}")
                c1.metric("📈 Direnç 1", f"{r1:.2f}")
                c2.metric("⚖️ PİVOT", f"{p:.2f}")
                c3.metric("📉 Destek 1", f"{s1:.2f}")
                c3.metric("🚨 Destek 2", f"{s2:.2f}")
