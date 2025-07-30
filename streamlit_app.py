# === SPECTRO+: Website Edukasi SPEKTROSKOPI ===

import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
import re

# -------------------- Judul & Navigasi --------------------
st.set_page_config(page_title="SPECTRO+", page_icon="🔬")

st.title("🔬 SPECTRO+")
st.subheader("Prediksi Senyawa dari Spektrum IR")
st.markdown("Aplikasi pintar untuk bantu interpretasi data spektrum, cocok untuk mahasiswa analis kimia!")

# -------------------- Navigasi Sidebar --------------------
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

# -------------------- Data Spektrum IR Akurat --------------------
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

# -------------------- Isi Tiap Halaman --------------------

if halaman == "🧪 Kuis Interaktif":
    st.markdown("## 🧪 Kuis Spektroskopi IR")
    st.markdown("Jawab pertanyaan berikut untuk menguji pemahaman kamu:")

    kuis_list = [
        {
            "soal": "Rentang 1680–1750 cm⁻¹ merupakan ciri khas gugus?",
            "opsi": ["C=C", "C≡N", "C=O", "O–H"],
            "jawaban": "C=O",
            "penjelasan": "C=O atau gugus karbonil memiliki pita serapan yang sangat tajam dan kuat di rentang ini karena vibrasi ikatan rangkap dua antara karbon dan oksigen sangat khas dan mudah dideteksi dengan IR. Gugus ini terdapat pada senyawa seperti aldehida, keton, asam karboksilat, dan ester."
        },
        {
            "soal": "Spektrum IR di 3200–3550 cm⁻¹ yang lebar dan intens biasanya menunjukkan?",
            "opsi": ["C–H", "N–H", "O–H (alkohol)", "C≡C"],
            "jawaban": "O–H (alkohol)",
            "penjelasan": "Spektrum O–H alkohol menunjukkan pita lebar karena adanya ikatan hidrogen yang menyebabkan peregangan molekul tidak seragam. Ini membuat sinyalnya melebar dan intens pada rentang tersebut. Ini berbeda dengan N–H yang tajam dan sempit."
        },
        {
            "soal": "Bilangan 2210–2260 cm⁻¹ dengan intensitas kuat kemungkinan besar adalah?",
            "opsi": ["C≡C", "C=O", "C≡N", "C=C"],
            "jawaban": "C≡N",
            "penjelasan": "C≡N atau gugus nitril memiliki pita tajam dan kuat karena vibrasi ikatan rangkap tiga antara karbon dan nitrogen yang sangat polar. Intensitasnya tinggi karena perbedaan keelektronegatifan antara C dan N sangat besar."
        },
        {
            "soal": "Gugus fungsi aromatik biasa menunjukkan serapan pada rentang?",
            "opsi": ["1450–1600 cm⁻¹", "1000–1300 cm⁻¹", "2850–2960 cm⁻¹", "3300–3500 cm⁻¹"],
            "jawaban": "1450–1600 cm⁻¹",
            "penjelasan": "Gugus aromatik seperti cincin benzena menunjukkan beberapa pita sedang hingga lemah dalam rentang ini, yang merupakan kombinasi dari vibrasi C=C konjugasi. Biasanya terdiri dari dua atau lebih pita khas yang digunakan untuk mengidentifikasi struktur aromatik."
        },
        {
            "soal": "Zona fingerprint biasanya berada di rentang?",
            "opsi": ["2500–3300 cm⁻¹", "1450–1750 cm⁻¹", "400–1400 cm⁻¹", "3500–4000 cm⁻¹"],
            "jawaban": "400–1400 cm⁻¹",
            "penjelasan": "Zona fingerprint adalah bagian spektrum IR yang sangat khas untuk tiap senyawa karena mencerminkan kombinasi vibrasi kompleks dari kerangka molekul. Biasanya sulit dianalisis secara langsung, tapi sangat berguna untuk membandingkan identitas senyawa dengan spektrum referensi."
        }
    ]

    skor = 0
    total = len(kuis_list)
    jawaban_pengguna = {}

    for i, soal in enumerate(kuis_list):
        st.write(f"{i+1}. {soal['soal']}")
        jawaban = st.radio("Pilih jawaban:", soal["opsi"], key=i)
        jawaban_pengguna[i] = jawaban
        if st.button(f"Cek Jawaban {i+1}"):
            if jawaban == soal["jawaban"]:
                st.success("✅ Benar!")
                st.info(soal["penjelasan"])
                skor += 1
            else:
                st.error(f"❌ Salah. Jawaban benar: {soal['jawaban']}")
                st.info(soal["penjelasan"])
        st.markdown("---")

    if st.button("🎯 Lihat Skor Akhir"):
        nilai = skor * 10
        st.subheader(f"Skor Akhir Kamu: {nilai} / 100")
        if nilai == 100:
            st.success("🎉 Luar biasa! Kamu menjawab semua soal dengan benar.")
        elif nilai >= 70:
            st.info("👍 Bagus! Kamu cukup menguasai materi spektroskopi IR.")
        else:
            st.warning("📚 Masih perlu belajar lebih dalam tentang interpretasi spektrum IR.")S
