import streamlit as st
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")

# Bulunduğumuz dizini alıyoruz
su_anki_dizin = os.path.dirname(os.path.abspath(__file__))

def modulu_calistir(hedef_dosya_adi):
    """Dosyayı bulur ve doğrudan Python içinde çalıştırır."""
    butun_dosyalar = os.listdir(su_anki_dizin)
    gercek_dosya_adi = None
    
    # Harf duyarsız dosya arama
    for dosya in butun_dosyalar:
        if dosya.lower() == hedef_dosya_adi.lower():
            gercek_dosya_adi = dosya
            break
            
    if gercek_dosya_adi:
        yol = os.path.join(su_anki_dizin, gercek_dosya_adi)
        try:
            # DİREKT ÇALIŞTIRMA YÖNTEMİ (Daha Sağlam)
            with open(yol, "r", encoding="utf-8") as f:
                kod = f.read()
                exec(kod, globals()) # Dosyayı ana bellek üzerinde çalıştırır
        except Exception as e:
            st.error(f"⚠️ Modül çalışırken hata verdi: {e}")
    else:
        st.error(f"❌ '{hedef_dosya_adi}' bulunamadı usta!")

st.title("🛰️ USTA BORSA PUSULASI PANELİ v19.1")
st.write("---")

tabs = st.tabs(["⚠️ v12.0 GÜVENLİK", "🎯 v12.5 AL-SAT", "🚀 v12.7 LİSTE", "💰 KÂR-ZARAR", "⚖️ ROD-BALANS"])

with tabs[0]:
    if st.button("Hisse Güvenlik Modülünü Başlat"):
        modulu_calistir("HİSSE GÜVENLİK .PY")

with tabs[1]:
    if st.button("Al-Sat Kontrolünü Başlat"):
        modulu_calistir("AL SAT KONTROL.py")

with tabs[2]:
    st.info("Liste tarama için dosyayı klasöre eklemelisin usta.")

with tabs[3]:
    if st.button("Kâr-Zarar Modülünü Yükle"):
        modulu_calistir("KAAR ZARAR KONTROL.py")

with tabs[4]:
    if st.button("Rod-Balans Ayarını Başlat"):
        modulu_calistir("KISAORTAUZUNKONTROL.PY")
