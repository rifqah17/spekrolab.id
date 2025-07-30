# === SPECTRO+: Website Edukasi SPEKTROSKOPI ===

import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import re

# -------------------- Konfigurasi Judul --------------------
st.set_page_config(page_title="SPECTRO+", page_icon="🔬")

st.title("🔬 SPECTRO+")
st.subheader("Prediksi Senyawa dari Spektrum IR")
st.markdown("Aplikasi pintar untuk bantu interpretasi data spektrum, cocok untuk mahasiswa analis kimia!")

# -------------------- Sidebar Navigasi --------------------
halaman = st.sidebar.selectbox(
    "🧭 Navigasi Halaman",
    [
        "🏠 Beranda",
        "📷 Upload Gambar Spektrum",
        "📊 Input Data Panjang Gelombang",
        "📚 Teori & Tabel Spektrum",
        "🧪 Kuis Interaktif"
    ]
)

# -------------------- Data Spektrum IR --------------------
ir_data = [
    ("O–H (alkohol)", 3200, 3550, "Lebar, intens"),
    ("O–H (asam karboksilat)", 2500, 3300, "Sangat lebar dan tumpang tindih"),
    ("N–H (amina)", 3300, 3500, "Tajam, 1 atau 2 puncak"),
    ("C–H (alkana)", 2850, 2960, "Tajam, kuat"),
    ("C–H (alkena)", 3020, 3100, "Tajam, sedang"),
    ("C–H (aromatik)", 3000, 3100, "Lemah–sedang"),
    ("≡C–H (alkuna terminal)", 3300, 3300, "Tajam"),
    ("C≡C", 2100, 2260, "Tajam, lemah"),
    ("C≡N", 2210, 2260, "Tajam, kuat"),
    ("C=C (alkena)", 1620, 1680, "Tajam, sedang"),
    ("C=C (aromatik)", 1450, 1600, "2–3 pita lemah"),
    ("C=O (karbonil)", 1680, 1750, "Tajam, sangat kuat"),
    ("C–O", 1000, 1300, "Tajam, 1–2 pita"),
    ("C–N", 1180, 1360, "Medium"),
    ("Zona fingerprint", 400, 1400, "Sangat kompleks dan khas")
]

# -------------------- Data Kuis --------------------
kuis_list = [
    {
        "soal": "Spektrum IR menunjukkan pita tajam dan kuat di sekitar 1700 cm⁻¹. Gugus fungsi apa yang kemungkinan besar ada?",
        "opsi": ["Amina", "Karbonil", "Alkuna", "Alkana"],
        "jawaban": "Karbonil",
        "penjelasan": "Pita tajam dan kuat di sekitar 1700 cm⁻¹ merupakan ciri khas gugus karbonil (C=O)."
    },
    {
        "soal": "Pita serapan lebar di sekitar 3200–3600 cm⁻¹ kemungkinan disebabkan oleh?",
        "opsi": ["N–H", "C≡C", "O–H", "C–H"],
        "jawaban": "O–H",
        "penjelasan": "Gugus hidroksil (O–H) menimbulkan pita lebar karena adanya ikatan hidrogen."
    },
    {
        "soal": "Serapan pada 2100–2260 cm⁻¹ menunjukkan keberadaan gugus?",
        "opsi": ["C≡N atau C≡C", "C–N", "C=O", "C–O"],
        "jawaban": "C≡N atau C≡C",
        "penjelasan": "Daerah ini khas untuk gugus rangkap tiga seperti nitril (C≡N) dan alkuna (C≡C)."
    },
    {
        "soal": "Apa fungsi zona fingerprint dalam spektrum IR?",
        "opsi": ["Menentukan panjang gelombang", "Identifikasi senyawa secara spesifik", "Menentukan konsentrasi", "Menentukan warna senyawa"],
        "jawaban": "Identifikasi senyawa secara spesifik",
        "penjelasan": "Zona fingerprint (1500–400 cm⁻¹) sangat kompleks dan unik untuk setiap senyawa."
    },
    {
        "soal": "Pita regangan C–H sp³ dari alkana biasanya muncul di sekitar?",
        "opsi": ["2850–2960 cm⁻¹", "3300 cm⁻¹", "1700 cm⁻¹", "2200 cm⁻¹"],
        "jawaban": "2850–2960 cm⁻¹",
        "penjelasan": "Alkana memperlihatkan pita C–H sp³ di kisaran 2850–2960 cm⁻¹ yang tajam dan kuat."
    },
    {
        "soal": "Bilangan gelombang sekitar 3300 cm⁻¹ dengan dua puncak biasanya menunjukkan keberadaan?",
        "opsi": ["Amina sekunder", "Amina primer", "Alkohol", "Karbonil"],
        "jawaban": "Amina primer",
        "penjelasan": "Amina primer (R-NH₂) menghasilkan dua pita tajam pada 3300–3500 cm⁻¹ karena dua regangan N–H simetris dan asimetris."
    },
    {
        "soal": "Serapan tajam dan kuat di sekitar 1740 cm⁻¹ dapat menunjukkan gugus?",
        "opsi": ["Amina", "Ester", "Alkena", "Alkana"],
        "jawaban": "Ester",
        "penjelasan": "Ester menunjukkan pita kuat C=O di sekitar 1735–1750 cm⁻¹, sedikit lebih tinggi dari keton biasa karena efek tarik gugus O–R."
    },
    {
        "soal": "Jika spektrum menunjukkan pita lemah di 2100–2260 cm⁻¹, kemungkinan senyawa tersebut mengandung?",
        "opsi": ["C–N", "C≡C", "C=O", "O–H"],
        "jawaban": "C≡C",
        "penjelasan": "C≡C (alkuna) sering memberikan pita lemah dalam IR karena perubahan dipolnya kecil."
    },
    {
        "soal": "Apa yang menyebabkan pita O–H dari asam karboksilat sangat lebar?",
        "opsi": ["Ikatan hidrogen intramolekul", "Ikatan hidrogen kuat", "Tidak polar", "Ikatan rangkap tiga"],
        "jawaban": "Ikatan hidrogen kuat",
        "penjelasan": "O–H dari asam karboksilat sangat lebar karena ikatan hidrogen kuat dan ekstensif antar molekul."
    },
    {
        "soal": "Ciri khas C–O ester biasanya muncul di daerah?",
        "opsi": ["900–1100 cm⁻¹", "1000–1300 cm⁻¹", "1600–1750 cm⁻¹", "2850–2960 cm⁻¹"],
        "jawaban": "1000–1300 cm⁻¹",
        "penjelasan": "Regangan C–O dari ester biasanya menghasilkan pita kuat di kisaran 1050–1300 cm⁻¹."
    },
    {
        "soal": "Gugus NO₂ menunjukkan berapa pita khas dalam spektrum IR?",
        "opsi": ["1", "2", "3", "4"],
        "jawaban": "2",
        "penjelasan": "NO₂ memberikan dua pita kuat khas: regangan simetris (sekitar 1350 cm⁻¹) dan asimetris (sekitar 1530 cm⁻¹)."
    },
    {
        "soal": "Pita pada 2850 dan 2920 cm⁻¹ paling mungkin berasal dari?",
        "opsi": ["Alkana", "Aromatik", "Karbonil", "Nitril"],
        "jawaban": "Alkana",
        "penjelasan": "C–H sp³ (alkana) menunjukkan dua pita regangan CH pada sekitar 2850 dan 2920 cm⁻¹."
    },
    {
        "soal": "Serapan C=C pada alkena biasanya muncul di?",
        "opsi": ["1000–1300 cm⁻¹", "1500–1600 cm⁻¹", "1600–1680 cm⁻¹", ">3000 cm⁻¹"],
        "jawaban": "1600–1680 cm⁻¹",
        "penjelasan": "Regangan C=C pada alkena menghasilkan pita medium pada 1620–1680 cm⁻¹."
    },
    {
        "soal": "Jika spektrum IR menunjukkan serapan kuat pada 1700 cm⁻¹ dan pita lebar pada 2500–3300 cm⁻¹, senyawa tersebut kemungkinan adalah?",
        "opsi": ["Ester", "Amina", "Asam karboksilat", "Aldehida"],
        "jawaban": "Asam karboksilat",
        "penjelasan": "Asam karboksilat menunjukkan kombinasi dua pita khas: C=O kuat di 1700 cm⁻¹ dan O–H sangat lebar di 2500–3300 cm⁻¹."
    },
    {
        "soal": "Serapan tajam di sekitar 3300 cm⁻¹, tidak terlalu lebar, kemungkinan adalah?",
        "opsi": ["C–H sp³", "N–H", "O–H", "C≡N"],
        "jawaban": "N–H",
        "penjelasan": "N–H dari amina menimbulkan pita tajam sekitar 3300 cm⁻¹, biasanya lebih sempit daripada O–H."
    },
    {
        "soal": "Apa perbedaan utama serapan C=O dari aldehida dan keton?",
        "opsi": ["Aldehida lebih rendah", "Keton lebih kuat", "Aldehida punya dua pita tambahan", "Keton lebih lebar"],
        "jawaban": "Aldehida punya dua pita tambahan",
        "penjelasan": "Aldehida menunjukkan dua pita regangan C–H di sekitar 2700–2900 cm⁻¹, selain pita C=O di 1720 cm⁻¹."
    },
    {
        "soal": "Jika tidak ditemukan pita C=O, kemungkinan besar senyawa tersebut bukan?",
        "opsi": ["Alkohol", "Ester", "Amina", "Alkana"],
        "jawaban": "Ester",
        "penjelasan": "Ester selalu memiliki pita C=O kuat. Jika tidak ada, senyawa tersebut kemungkinan bukan ester."
    },
    {
        "soal": "Spektrum dengan pita di 1450–1600 cm⁻¹ dan 3000–3100 cm⁻¹ kemungkinan menunjukkan keberadaan?",
        "opsi": ["Alkana", "Aromatik", "Ester", "Alkena"],
        "jawaban": "Aromatik",
        "penjelasan": "Aromatik menunjukkan regangan C=C pada 1450–1600 cm⁻¹ dan regangan C–H aromatik di 3000–3100 cm⁻¹."
    },
    {
        "soal": "Pita IR dari C≡N cenderung lebih kuat daripada C≡C karena?",
        "opsi": ["C≡N lebih panjang", "Dipol C≡N lebih besar", "C≡N tidak menyerap", "C≡C simetris"],
        "jawaban": "Dipol C≡N lebih besar",
        "penjelasan": "C≡N menyerap lebih kuat karena memiliki momen dipol yang lebih besar daripada C≡C yang simetris."
    },
    {
        "soal": "Bilangan gelombang lebih tinggi dari 3000 cm⁻¹ biasanya menandakan regangan?",
        "opsi": ["C–C", "C–O", "X–H", "C=O"],
        "jawaban": "X–H",
        "penjelasan": "Bilangan >3000 cm⁻¹ biasanya berasal dari regangan ikatan X–H seperti O–H, N–H, atau C–H sp²/sp³."
    }
]

# -------------------- Halaman Kuis --------------------
if halaman == "🧪 Kuis Interaktif":
    st.markdown("## 🧪 Kuis Spektroskopi IR")
    st.markdown("Jawab pertanyaan berikut untuk menguji pemahaman kamu:")

    if 'skor' not in st.session_state:
        st.session_state.skor = 0

    for i, soal in enumerate(kuis_list):
        st.write(f"### {i+1}. {soal['soal']}")
        jawaban = st.radio("Pilih jawaban kamu:", soal["opsi"], key=f"kuis_{i}")
        if st.button(f"Cek Jawaban {i+1}", key=f"cek_{i}"):
            if jawaban == soal["jawaban"]:
                st.success("✅ Jawaban kamu BENAR!")
                st.info(soal["penjelasan"])
                st.session_state.skor += 5
            else:
                st.error(f"❌ Jawaban kamu SALAH. Jawaban yang benar: {soal['jawaban']}")
                st.info(soal["penjelasan"])
        st.markdown("---")

    if st.button("🎯 Lihat Skor Akhir"):
        nilai = st.session_state.skor * 100 // (len(kuis_list) * 5)
        st.subheader(f"Skor Akhir Kamu: {nilai} / 100")
        if nilai == 100:
            st.success("🎉 Luar biasa! Kamu menjawab semua soal dengan benar.")
        elif nilai >= 70:
            st.info("👍 Bagus! Kamu cukup menguasai materi spektroskopi IR.")
        else:
            st.warning("📚 Masih perlu belajar lebih dalam tentang interpretasi spektrum IR.")
