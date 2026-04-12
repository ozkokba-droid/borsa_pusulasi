import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import io
from contextlib import redirect_stdout

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")

# --- GÜVENLİK KİLİDİ FONKSİYONU ---
def giris_kontrol():
    if "giris_basarili" not in st.session_state:
        st.session_state["giris_basarili"] = False

    if not st.session_state["giris_basarili"]:
        st.markdown("<h1 style='text-align: center;'>🛡️ USTA TERMİNALİ GİRİŞ</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            kullanici = st.text_input("Kullanıcı Adı:")
            sifre = st.text_input("Şifre:", type="password")
            if st.button("Dükkanı Aç 🔑"):
                # BURADAN ŞİFREYİ DEĞİŞTİREBİLİRSİN USTA
                if kullanici == "usta" and sifre == "usta123":
                    st.session_state["giris_basarili"] = True
                    st.rerun()
                else:
                    st.error("❌ Yetkisiz Giriş! Şanzımanı dağıtma, şifreyi doğru gir.")
        return False
    return True

# --- YARDIMCI FONKSİYON: TERMİNAL ÇIKTISINI YAKALAMA ---
def terminal_calistir(func, input_val):
    f = io.StringIO()
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: input_val
    with redirect_stdout(f):
        func()
    builtins.input = original_input
    return f.getvalue()

# --- ANA SİSTEM BAŞLIYOR ---
if giris_kontrol():
    st.sidebar.success("✅ Yetki Onaylandı. Hoş geldin Usta!")
    if st.sidebar
