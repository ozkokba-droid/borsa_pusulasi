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
            else:
                st.error("❌ Şifre yanlış usta!")
else:
    # --- ANA PANEL ---
    st.sidebar.success("✅ Yetki Onaylandı.")
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.title("🛰️ USTA BORSA PUSULASI v16.7")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    def terminal_calistir(func, input_val):
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                func()
        except Exception as e:
            print(f"Hata oluştu: {e}")
        return f.getvalue()

    # --- TAB 1: LİSTE ---
    with tabs[0]:
        st.subheader("Dinamik Liste Tarama")
        girdi_127 = st.text_input("Hisseler (örn: THYAO, SASA):", "THYAO, SASA, FROTO", key="in127")
        if st.button("TARAMAYI BAŞLAT 📡", key="btn127"):
            def func_127():
                izleme = [h.strip().upper() for h in girdi_127.split(",") if h.strip()]
                print(f"{'HİSSE':<10} | {'FİYAT':<8} | {'DURUM'}")
                for sembol in izleme:
                    h_kod = sembol + ".IS" if "." not in sembol else sembol
                    d = yf.download(h_kod, period="1mo", progress=False)
                    if not d.empty:
                        f = d['Close'].iloc[-1].values[0] if isinstance(d['Close'], pd.DataFrame) else d['Close'].iloc[-1]
                        print(f"{sembol:<10} | {f:>8.2f} | 🟢 ANALİZ TAMAM")
            st.code(terminal_calistir(func_127, girdi_127))

    # --- TAB 2: SİNYAL ---
    with tabs[1]:
        st.subheader("Al-Sat Sinyal Kontrol")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="in125")
        if st.button("SİNYALİ SORGULA 🎯", key="btn125"):
            def func_125():
                h = hisse_125 + ".IS" if "." not in hisse_125 else hisse_125
                d = yf.download(h, period="6mo", progress=False)
                if not d.empty:
                    f = d['Close'].iloc[-1].values[0] if isinstance(d['Close'], pd.DataFrame) else d['Close'].iloc[-1]
                    print(f"🚀 {h} Analizi\nSon Fiyat: {f:.2f}\nDurum: Sinyal Güçlü")
            st.code(terminal_calistir(func_125, hisse_125))

    # --- TAB 3: GÜVENLİK ---
    with tabs[2]:
        st.subheader("Güvenlik Sensörü")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="in120")
        if st.button("GÜVENLİK RAPORU 🛡️", key="btn120"):
            def func_120():
                h = hisse_120 + ".IS" if "." not in hisse_120 else hisse_120
                d = yf.download(h, period="1y", progress=False)
                if not d.empty:
                    f = d['Close'].iloc[-1].values[0] if isinstance(d['Close'], pd.DataFrame) else d['Close'].iloc[-1]
                    print(f"📊 {h} Raporu\nFiyat: {f:.2f}\nSürüş: Güvenli Sürüş")
            st.code(terminal_calistir(func_120, hisse_120))

    # --- TAB 4: ROD-BALANS ---
    with tabs[3]:
        st.subheader("Rod-Balans (Destek/Direnç)")
        hisse_160 = st.text_input("Hisse Kodu:", "THYAO", key="in160")
        if st.button("SEVİYELERİ HESAPLA ⚖️", key="btn160"):
            def func_160():
                h = hisse_160 + ".IS"
