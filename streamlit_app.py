=== SPECTRO+: Website Edukasi SPEKTROSKOPI ===

import streamlit as st import pandas as pd from PIL import Image import pytesseract import re

-------------------- Judul & Navigasi --------------------

st.set_page_config(page_title="SPECTRO+", page_icon="🔬")

st.title("🔬 SPECTRO+") st.subheader("AI Prediksi Senyawa dari Spektrum IR, UV-Vis, dan GC") st.markdown("Aplikasi pintar untuk bantu interpretasi data spektrum, cocok untuk mahasiswa analis kimia!")

-------------------- Navigasi Sidebar --------------------

halaman = st.sidebar.selectbox( "🧭 Navigasi Halaman", [ "🏠 Beranda", "📷 Upload Gambar Spektrum", "📊 Input Data Panjang Gelombang", "📈 Hasil Prediksi", "📚 Teori & Tabel Spektrum", "🧪 Kuis Interaktif (Opsional)" ] )

-------------------- Isi Tiap Halaman --------------------

if halaman == "🏠 Beranda": st.image("https://i.imgur.com/3ZQ3Z5L.png", caption="Selamat datang di SPECTRO+", use_column_width=True) st.markdown("### 🎯 Tujuan Aplikasi:") st.markdown("- Membantu mahasiswa mengenali gugus fungsi & senyawa dari spektrum IR & UV-Vis") st.markdown("- Mempermudah analisis data praktikum") st.markdown("- Memberikan pembelajaran interaktif melalui teori & kuis") st.success("Silakan pilih menu di sebelah kiri untuk mulai menggunakan SPECTRO+.")

elif halaman == "📷 Upload Gambar Spektrum": st.markdown("## 📷 Upload Gambar Spektrum + OCR Deteksi Puncak")

uploaded_file = st.file_uploader("Unggah gambar hasil IR / UV-Vis / Kromatografi (.jpg, .png)", type=["jpg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar Spektrum Terupload", use_column_width=True)

    with st.spinner("🔍 Mendeteksi angka bilangan gelombang..."):
        text = pytesseract.image_to_string(image)
        angka = re.findall(r'\b[1-3]?\d{3}\b', text)
        angka_unik = sorted(set(map(int, angka)))

    if angka_unik:
        st.success("📌 Puncak yang terdeteksi:")
        st.write(angka_unik)

        st.markdown("### 🔍 Prediksi Gugus Fungsi:")
        for p in angka_unik:
            if 2850 <= p <= 2960 or 1350 <= p <= 1470:
                st.write(f"➡ {p} cm⁻¹: *C–H (Alkana)*")
            elif 3020 <= p <= 3080 or 675 <= p <= 870:
                st.write(f"➡ {p} cm⁻¹: *C–H (Alkena)*")
            elif 3000 <= p <= 3100:
                st.write(f"➡ {p} cm⁻¹: *C–H (Aromatik)*")
            elif p == 3300:
                st.write(f"➡ {p} cm⁻¹: *C≡H (Alkuna)*")
            elif 1640 <= p <= 1680:
                st.write(f"➡ {p} cm⁻¹: *C=C (Alkena)*")
            elif 1500 <= p <= 1600:
                st.write(f"➡ {p} cm⁻¹: *C=C (Aromatik/Cincin)*")
            elif 1080 <= p <= 1300:
                st.write(f"➡ {p} cm⁻¹: *C–O (Alkohol, Ester, Asam Karboksilat)*")
            elif 1690 <= p <= 1760:
                st.write(f"➡ {p} cm⁻¹: *C=O (Karbonil)*")
            elif 3610 <= p <= 3640:
                st.write(f"➡ {p} cm⁻¹: *O–H (Alkohol/Fenol)*")
            elif 2000 <= p <= 3600:
                st.write(f"➡ {p} cm⁻¹: *O–H (Ikatan H)*")
            elif 3310 <= p <= 3500:
                st.write(f"➡ {p} cm⁻¹: *N–H (Amina)*")
            elif 1180 <= p <= 1360:
                st.write(f"➡ {p} cm⁻¹: *C–N (Amina)*")
            elif 1515 <= p <= 1560 or 1345 <= p <= 1385:
                st.write(f"➡ {p} cm⁻¹: *–NO₂ (Nitro)*")
            else:
                st.write(f"➡ {p} cm⁻¹: Belum terdaftar.")
    else:
        st.warning("⚠ Tidak ditemukan angka bilangan gelombang dari gambar.")

elif halaman == "📊 Input Data Panjang Gelombang": st.markdown("## 📊 Input Panjang Gelombang (IR, cm⁻¹)")

panjang = st.text_input("Masukkan bilangan gelombang IR (misal: 1700):")

if panjang:
    try:
        p = int(panjang)
        st.success(f"Bilangan gelombang yang dimasukkan: {p} cm⁻¹")

        st.markdown("### 🔍 Prediksi Otomatis:")
        # (Gunakan logika prediksi yang sama dengan di OCR)
    except ValueError:
        st.error("Masukkan angka bilangan gelombang yang valid.")

elif halaman == "📈 Hasil Prediksi": st.markdown("## 📈 Hasil Analisis Spektrum") st.markdown("### 💡 Deteksi Gugus Fungsi:") st.markdown("- C=O, O-H, N-H, C=C") st.markdown("### 🧬 Kemungkinan Senyawa:") st.markdown("- Asam benzoat, Asetofenon, Etanol") st.markdown("### 🧪 Struktur Kimia:") st.image("https://i.imgur.com/MuGqYEx.png", caption="Contoh struktur: Asam Benzoat", width=300) st.download_button("📥 Export Hasil sebagai PDF", data="Hasil analisis...", file_name="hasil_spectro+.pdf")

elif halaman == "📚 Teori & Tabel Spektrum": st.markdown("## 📚 Teori & Tabel Spektrum IR") st.markdown("Berikut adalah rentang serapan IR untuk berbagai gugus fungsi:")

data = {
    "Gugus": ["C–H", "C–H", "C–H", "C≡H", "C=C", "C=C", "C–O", "C=O", "O–H", "O–H", "O–H", "N–H", "C–N", "–NO₂"],
    "Jenis Senyawa": [
        "Alkana", "Alkena", "Aromatik", "Alkuna", "Alkena", "Aromatik (cincin)",
        "Alkohol, eter, asam karboksilat, ester",
        "Aldehida, keton, asam karboksilat, ester",
        "Alkohol, fenol (monomer)",
        "Alkohol, fenol (ikatan H)",
        "Asam karboksilat",
        "Amina", "Amina", "Nitro"
    ],
    "Daerah Serapan (cm⁻¹)": [
        "2850–2960, 1350–1470",
        "3020–3080, 675–870",
        "3000–3100, 675–870",
        "3300",
        "1640–1680",
        "1500–1600",
        "1080–1300",
        "1690–1760",
        "3610–3640",
        "2000–3600 (lebar)",
        "3000–3600 (lebar)",
        "3310–3500",
        "1180–1360",
        "1515–1560, 1345–1385"
    ]
}
df = pd.DataFrame(data)
st.table(df)

elif halaman == "🧪 Kuis Interaktif (Opsional)": st.markdown("## 🧪 Kuis Spektroskopi") st.markdown("(Coming soon!) 🎉") st.info("Kuis IR dan UV-Vis akan ditambahkan untuk menguji pemahaman.")
