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
        kullanici = st.text_input("Kullanıcı Adı:")
        sifre = st.text_input("Şifre:", type="password")
        if st.button("Dükkanı Aç 🔑"):
            if kullanici == "usta" and (sifre == "usta123" or sifre == "Usta123"):
                st.session_state["giris_basarili"] = True
                st.rerun()
            else:
                st.error("❌ Yetkisiz Giriş! Şifreyi doğru gir usta.")
else:
    # --- ANA PANEL ---
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.sidebar.success("✅ Yetki Onaylandı. Hoş geldin Usta!")
    st.title("🛰️ USTA BORSA PUSULASI: ÖZEL PANEL v16.2")
    st.write("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 v12.7 DİNAMİK LİSTE", 
        "🎯 v12.5 AL-SAT SİNYAL", 
        "⚠️ v12.0 GÜVENLİK SENSÖRÜ",
        "⚖️ v16.0 ROD-BALANS (D/D)"
    ])

    def terminal_calistir(func, input_val):
        f = io.StringIO()
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: input_val
        with redirect_stdout(f):
            func()
        builtins.input = original_input
        return f.getvalue()

    # --- SEKME 1: v12.7 ---
    with tab1:
        st.header("v12.7: 'OTOMATİK GARAJ'")
        girdi_127 = st.text_input("🔍 Taranacak Hisseler:", "THYAO, SASA, ASTOR, FROTO", key="k127")
        if st.button("LİSTEYİ TARAMAYA BAŞLA 📡"):
            def func_127():
                print("\n" + "="*75 + "\n 🎯 v12.7: DİNAMİK LİSTE TARAMA \n" + "="*75)
                izleme = [h.strip().upper() for h in girdi_127.split(",") if h.strip()]
                print(f"{'HİSSE':<10} | {'FİYAT':<8} | {'HACİM':<10} | {'DURUM'}")
                for sembol in izleme:
                    try:
                        h_kod = sembol + ".IS" if "." not in sembol else sembol
                        d = yf.download(h_kod, period="1mo", progress=False)
                        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
                        f = d['Close'].iloc[-1]; e20 = d['Close'].ewm(span=20).mean().iloc[-1]
                        h_gucu = (d['Volume'].iloc[-1] / d['Volume'].tail(10).mean()) * 100
                        durum = "🟢 GÜÇLÜ AL" if f > e20 and h_gucu > 120 else "🔴 BEKLE"
                        print(f"{sembol:<10} | {f:>8.2f} | %{h_gucu:>10.0f} | {durum}")
                    except: continue
            st.code(terminal_calistir(func_127, girdi_127), language='text')

    # --- SEKME 2: v12.5 ---
    with tab2:
