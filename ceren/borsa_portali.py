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
    st.title("🛰️ USTA BORSA PUSULASI: ÖZEL PANEL v16.1")
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
        st.header("v12.5: AL-SAT SİNYAL ONAY")
        hisse_125 = st.text_input("Hisse Kodu:", "FROTO", key="k125")
        if st.button("SİNYAL ONAYI AL 🎯"):
            def func_125():
                h = hisse_125 + ".IS" if "." not in hisse_125 else hisse_125
                d = yf.download(h, period="6mo", progress=False)
                if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
                f = d['Close'].iloc[-1]
                rsi = (100 - (100 / (1 + (d['Close'].diff().where(d['Close'].diff() > 0, 0).rolling(14).mean() / -d['Close'].diff().where(d['Close'].diff() < 0, 0).rolling(14).mean())))).iloc[-1]
                print(f"🚀 {h} ANALİZİ\nFiyat: {f:.2f}\nRSI: {rsi:.2f}\nSinyal: {'🟢 AL' if rsi < 70 else '🟠 DOYUM'}")
                st.session_state['d125'] = d
            st.code(terminal_calistir(func_125, hisse_125), language='text')
            if 'd125' in st.session_state:
                fig, _ = mpf.plot(st.session_state['d125'].tail(60), type='candle', style='charles', returnfig=True)
                st.pyplot(fig)

    # --- SEKME 3: v12.0 ---
    with tab3:
        st.header("v12.0: GÜVENLİK SENSÖRÜ")
        hisse_120 = st.text_input("Hisse Kodu:", "ASELS", key="k120")
        if st.button("GÜVENLİK RAPORU AL 🛡️"):
            def func_120():
                h = hisse_120 + ".IS" if "." not in hisse_120 else hisse_120
                d = yf.download(h, period="1y", progress=False)
                if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
                f = d['Close'].iloc[-1]; e20 = d['Close'].ewm(span=20).mean().iloc[-1]
                print(f"📊 {h} RAPORU\nDurum: {'✅ GÜVENLİ' if f > e20 else '🚨 RİSKLİ'}\nMesafe: %{((f-e20)/e20*100):.2f}")
            st.code(terminal_calistir(func_120, hisse_120), language='text')

    # --- SEKME 4: v16.0 ROD-BALANS ---
    with tab4:
        st.header("v16.0: DESTEK & DİRENÇ ANALİZİ")
        hisse_160 = st.text_input("Analiz Edilecek Makine (Örn: THYAO):", "THYAO", key="k160")
        if st.button("SEVİYELERİ HESAPLA ⚖️"):
            def func_160():
                h = hisse_160 + ".IS" if "." not in hisse_
