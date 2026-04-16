import streamlit as st
import yfinance as yf
import pandas as pd

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

    st.title("🛰️ USTA BORSA PUSULASI v16.9")
    st.write("---")

    tabs = st.tabs(["🚀 v12.7 LİSTE", "🎯 v12.5 SİNYAL", "⚠️ v12.0 GÜVENLİK", "⚖️ v16.0 ROD-BALANS"])

    # --- TAB 4: ROD-BALANS (BURASI SENİN ÇALIŞMAYAN KISIM) ---
    with tabs[3]:
        st.subheader("Rod-Balans (Destek/Direnç)")
        hisse_input = st.text_input("Analiz Edilecek Hisse:", "SASA", key="in160")
        
        if st.button("SEVİYELERİ HESAPLA ⚖️"):
            h_kod = hisse_input.upper() + ".IS" if "." not in hisse_input else hisse_input.upper()
            
            with st.spinner('Veriler garajdan getiriliyor...'):
                df = yf.download(h_kod, period="5d", progress=False)
            
            if not df.empty and len(df) >= 2:
                # KRİTİK TAMİR: MultiIndex hatasını temizliyoruz
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                
                # Verileri float tipine zorla (Gözükmeme sorununu çözer)
                last_day = df.iloc[-2]
                h = float(last_day['High'])
                l = float(last_day['Low'])
                c = float(last_day['Close'])
                
                # Pivot Hesaplamaları
                pivot = (h + l + c) / 3
                r1, s1 = (2 * pivot) - l, (2 * pivot) - h
                r2, s2 = pivot + (h - l), pivot - (h - l)
                
                # SONUÇLARI GÖSTER
                st.markdown(f"### 📊 {h_kod} Analiz Sonuçları")
                
                # Metrikleri büyük kutularda göster
                m1, m2, m3 = st.columns(3)
                m1.metric("🚀 Direnç 2 (Tavan)", f"{r2:.2f}")
                m1.metric("📈 Direnç 1 (Üst)", f"{r1:.2f}")
                
                m2.subheader(f"⚖️ PİVOT: {pivot:.2f}")
                m2.write("---")
                m2.info(f"💰 Kapanış: {c:.2f}")
                
                m3.metric("📉 Destek 1 (Kriko)", f"{s1:.2f}")
                m3.metric("🚨 Destek 2 (Dip)", f"{s2:.2f}")
                
                if c > pivot:
                    st.success("🟢 Motor Sesi Sağlıklı: Fiyat Pivotun Üstünde!")
                else:
                    st.warning("🔴 Dikkat: Fiyat Pivotun Altında, Vitesi Küçült!")
            else:
                st.error("❌ Veri çekilemedi! İnterneti veya hisse kodunu kontrol et.")

    # Diğer sekmeler (v16.8 ile aynı mantıkta sadeleşti)
    with tabs[0]: st.write("Taramayı başlatmak için hisseleri gir usta.")
    with tabs[1]: st.write("Hisse analiz grafiği burada görünecek.")
    with tabs[2]: st.write("EMA20 güvenlik mesafesi ölçülecek.")
