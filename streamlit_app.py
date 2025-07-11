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

# -------------------- Data Spektrum IR --------------------
ir_data = [
    ("O–H (alkohol/fenol)", 3200, 3600, "Lebar, intens"),
    ("O–H (asam karboksilat)", 2500, 3300, "Sangat lebar, overlap"),
    ("N–H", 3300, 3500, "Tajam, 1–2 puncak"),
    ("C–H (alkana)", 2850, 2960, "Tajam, medium"),
    ("C–H (alkena)", 3020, 3100, "Tajam, lemah"),
    ("C–H (aromatik)", 3000, 3100, "Medium"),
    ("≡C–H (alkuna terminal)", 3300, 3300, "Tajam"),
    ("C≡C", 2100, 2260, "Tajam, lemah"),
    ("C≡N", 2210, 2260, "Tajam, kuat"),
    ("C=C (alkena)", 1620, 1680, "Tajam, medium"),
    ("C=C (aromatik)", 1450, 1600, "2 pita, medium"),
    ("C=O (karbonil)", 1650, 1750, "Tajam, sangat kuat"),
    ("C–O", 1000, 1300, "Tajam, 1–2 pita"),
    ("C–N", 1180, 1360, "Medium"),
    ("NO₂", 1345, 1560, "2 pita kuat")
]

# -------------------- Isi Tiap Halaman --------------------

if halaman == "🏠 Beranda":
    st.image("pp.jpg", caption="Selamat Datang!", use_container_width=True)
    st.markdown("### 🎯 Tujuan Aplikasi:")
    st.markdown("- Membantu mahasiswa mengenali gugus fungsi & senyawa dari spektrum IR")
    st.markdown("- Mempermudah analisis data praktikum")
    st.markdown("- Memberikan pembelajaran interaktif melalui teori & kuis")
    st.success("Silakan pilih menu di sebelah kiri untuk mulai menggunakan SPECTRO+.")

elif halaman == "📷 Upload Gambar Spektrum":
    st.markdown("## 📷 Upload Gambar Spektrum + OCR Deteksi Puncak")

    uploaded_file = st.file_uploader("Unggah gambar hasil IR (.jpg, .png)", type=["jpg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar Spektrum Terupload", use_column_width=True)

        with st.spinner("🔍 Mendeteksi angka bilangan gelombang..."):
            # Preprocessing gambar
            image = ImageOps.grayscale(image)
            image = image.filter(ImageFilter.SHARPEN)
            image = image.point(lambda x: 0 if x < 160 else 255, '1')

            text = pytesseract.image_to_string(image, config='--psm 6')
            angka = re.findall(r'\b[1-4]\d{2,3}\b', text)  # cari 3-4 digit angka antara 500–4000
            angka_valid = [int(a) for a in angka if 500 <= int(a) <= 4000]
            angka_unik = sorted(set(angka_valid))

        if angka_unik:
            st.success("📌 Puncak yang terdeteksi:")
            st.write(angka_unik)

            st.markdown("### 🔍 Prediksi Gugus Fungsi:")
            for p in angka_unik:
                match_found = False
                for gugus, start, end, desc in ir_data:
                    if start <= p <= end:
                        st.write(f"➡ {p} cm⁻¹: {gugus} ({desc})")
                        match_found = True
                        break
                if not match_found:
                    st.write(f"➡ {p} cm⁻¹: Belum terdaftar.")
        else:
            st.warning("⚠ Tidak ditemukan angka bilangan gelombang dari gambar.")

elif halaman == "📊 Input Data Panjang Gelombang":
    st.markdown("## 📊 Input Panjang Gelombang (IR, cm⁻¹)")

    panjang = st.text_input("Masukkan bilangan gelombang IR (misal: 1700):")

    if panjang:
        try:
            p = int(panjang)
            st.success(f"Bilangan gelombang yang dimasukkan: {p} cm⁻¹")

            st.markdown("### 🔍 Prediksi Otomatis:")
            match_found = False
            for gugus, start, end, desc in ir_data:
                if start <= p <= end:
                    st.write(f"🟢 {gugus} ({desc})")
                    match_found = True
                    break
            if not match_found:
                st.warning("⚠ Data tidak ditemukan di database.")
        except ValueError:
            st.error("Masukkan angka bilangan gelombang yang valid.")

elif halaman == "📚 Teori & Tabel Spektrum":
    st.markdown("## 📚 Teori & Tabel Spektrum IR")
    st.markdown("Berikut adalah rentang serapan IR untuk berbagai gugus fungsi:")

    df = pd.DataFrame(ir_data, columns=["Gugus Fungsi", "Dari (cm⁻¹)", "Sampai (cm⁻¹)", "Karakteristik"])
    st.table(df)

elif halaman == "🧪 Kuis Interaktif":
    st.markdown("## 🧪 Kuis Spektroskopi IR")
    st.markdown("Jawab pertanyaan berikut untuk menguji pemahaman kamu:")

    kuis_list = [
        {
            "soal": "Pita IR di sekitar 3300 cm⁻¹ yang tajam biasanya menandakan adanya?",
            "opsi": ["C=O", "O–H (lebar)", "≡C–H atau N–H", "C–O"],
            "jawaban": "≡C–H atau N–H"
        },
        {
            "soal": "Pita sangat lebar dari 2500–3300 cm⁻¹ adalah ciri khas dari?",
            "opsi": ["Alkohol", "Amina", "Asam karboksilat", "Ester"],
            "jawaban": "Asam karboksilat"
        },
        {
            "soal": "Pita serapan kuat dan tajam di 1700 cm⁻¹ biasanya merupakan?",
            "opsi": ["C=C", "C=O", "C–O", "C≡N"],
            "jawaban": "C=O"
        },
        {
            "soal": "Serapan 2210–2260 cm⁻¹ dapat menunjukkan adanya gugus?",
            "opsi": ["C–N", "C≡C", "C≡N", "C=C"],
            "jawaban": "C≡N"
        },
        {
            "soal": "Pita 2850–2960 cm⁻¹ umumnya berasal dari?",
            "opsi": ["O–H", "C–H (alkana)", "N–H", "C=C"],
            "jawaban": "C–H (alkana)"
        }
    ]

    for i, soal in enumerate(kuis_list):
        st.write(f"{i+1}. {soal['soal']}")
        jawaban = st.radio("Pilih jawaban:", soal["opsi"], key=i)
        if st.button(f"Cek Jawaban {i+1}"):
            if jawaban == soal["jawaban"]:
                st.success("✅ Benar!")
            else:
                st.error(f"❌ Salah. Jawaban benar: {soal['jawaban']}")
        st.markdown("---")