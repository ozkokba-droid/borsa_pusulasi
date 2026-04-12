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
                # ŞİFRE AYARI
                if kullanici == "pusula1" and (sifre == "usta123" or sifre == "pusula123"):
                    st.session_state["giris_basarili"] = True
                    st.rerun()
                else:
                    st.error("❌ Yetkisiz Giriş! Şifreyi doğru gir usta.")
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
    if st.sidebar.button("Güvenli Çıkış"):
        st.session_state["giris_basarili"] = False
        st.rerun()

    st.sidebar.success("✅ Yetki Onaylandı. Hoş geldin Usta!")
    st.title("🛰️ USTA BORSA PUSULASI: ÖZEL PANEL v15.6")
    st.write("---")

    tab1, tab2, tab3 = st.tabs(["🚀 v12.7 DİNAMİK LİSTE", "🎯 v12.5 AL-SAT SİNYAL", "⚠️ v12.0 GÜVENLİK SENSÖRÜ"])

    # --- SEKME 1: v12.7 DİNAMİK
