import streamlit as st
import importlib.util
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Usta Borsa Pusulası Pro", layout="wide")

# Klasör yolu (Senin dosyalarının olduğu yer)
klasor = "ceren"

def modulu_calistir(dosya_adi):
    """Klasördeki Python dosyalarını okur ve çalıştırır."""
    yol = os.path.join(klasor, dosya_adi)
    spec = importlib.util.spec_from_file_location("modul", yol)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    # Dosyanın içindeki ana fonksiyonu çağırıyoruz (Örn: pusula_pro_v12_0_guvenlik)
    # Eğer dosyaların içinde fonksiyon yoksa, import edildiği an zaten çalışacaktır.

st.title("🛰️ USTA BORSA PUSULASI PANELİ")
st.write("---")

# SEKMELERİ OLUŞTURUYORUZ
tabs = st.tabs(["⚠️ v12.0 GÜVENLİK", "🎯 v12.5 AL-SAT", "🚀 v12.7 LİSTE", "💰 KÂR-ZARAR", "⚖️ ROD-BALANS"])

with tabs[0]:
    st.subheader("Güvenlik Sensörleri")
    if st.button("Hisse Güvenlik Modülünü Başlat"):
        modulu_calistir("HİSSE GÜVENLİK .PY")

with tabs[1]:
    st.subheader("Al-Sat Onay Sistemi")
    if st.button("Al-Sat Kontrolünü Başlat"):
        modulu_calistir("AL SAT KONTROL.py")

with tabs[2]:
    st.subheader("Dinamik Liste Tarama")
    # Mevcut borsa_portali içindeki liste mantığını buraya alabilirsin
    st.info("Taramayı başlatmak için hisseleri gir usta.")

with tabs[3]:
    st.subheader("Maliyet ve Kâr Hesabı")
    if st.button("Kâr-Zarar Modülünü Yükle"):
        modulu_calistir("KAAR ZARAR KONTROL.py")

with tabs[4]:
    st.subheader("Kısa-Orta-Uzun Vade (Rod-Balans)")
    if st.button("Rod-Balans Ayarını Başlat"):
        modulu_calistir("KISAORTAUZUNKONTROL.py")
