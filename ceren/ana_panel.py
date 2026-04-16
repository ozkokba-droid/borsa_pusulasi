import streamlit as st
import importlib.util
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")

# Akıllı Yol Bulucu: ana_panel.py nerede duruyorsa orayı merkez alır
su_anki_dizin = os.path.dirname(os.path.abspath(__file__))

def modulu_calistir(dosya_adi):
    """Dosyayı bulur ve güvenli bir şekilde çalıştırır."""
    # Dosya yolunu birleştiriyoruz
    yol = os.path.join(su_anki_dizin, dosya_adi)
    
    if os.path.exists(yol):
        try:
            spec = importlib.util.spec_from_file_location("modul", yol)
            modul = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modul)
        except Exception as e:
            st.error(f"⚠️ Modül çalışırken hata verdi: {e}")
    else:
        st.error(f"❌ Dosya bulunamadı usta: {dosya_adi} \n\n Aranan yol: {yol}")

st.title("🛰️ USTA BORSA PUSULASI PANELİ v18.9")
st.write("---")

tabs = st.tabs(["⚠️ v12.0 GÜVENLİK", "🎯 v12.5 AL-SAT", "🚀 v12.7 LİSTE", "💰 KÂR-ZARAR", "⚖️ ROD-BALANS"])

with tabs[0]:
    if st.button("Hisse Güvenlik Modülünü Başlat"):
        modulu_calistir("HİSSE GÜVENLİK .PY")

with tabs[1]:
    if st.button("Al-Sat Kontrolünü Başlat"):
        modulu_calistir("AL SAT KONTROL.py")

with tabs[2]:
    st.info("Taramayı başlatmak için hisseleri gir usta.")

with tabs[3]:
    # KLASÖRDEKİ İSİM: KAAR ZARAR KONTROL.py (Tam eşleşme şart)
    if st.button("Kâr-Zarar Modülünü Yükle"):
        modulu_calistir("KAAR ZARAR KONTROL.py")

with tabs[4]:
    if st.button("Rod-Balans Ayarını Başlat"):
        modulu_calistir("KISAORTAUZUNKONTROL.py")
