import streamlit as st
from predict_gizi import predict_status_gizi
from send_single_message import send_single_message
from google_sheets_helper import init_google_sheets, is_duplicate_entry, save_to_google_sheets, clean_phone_number

# Inisialisasi Google Sheets
worksheet = init_google_sheets()

# Judul aplikasi
st.title("Prediksi Status Gizi Anak dan Pengiriman Hasil")

# Form input pengguna
nama_orang_tua = st.text_input("Nama Orang Tua:")
nama_anak = st.text_input("Nama Anak:")
jenis_kelamin = st.selectbox("Pilih jenis kelamin anak:", ("Laki-laki", "Perempuan"))
usia = st.number_input("Masukkan usia anak (dalam bulan):", min_value=0, max_value=60, step=1)
tinggi_badan = st.number_input("Masukkan tinggi badan anak (dalam cm):", min_value=0.0, step=0.1)
berat_badan = st.number_input("Masukkan berat badan anak (dalam kg):", min_value=0.0, step=0.1)
nomor_telepon = st.text_input("Nomor WhatsApp Anda (contoh: 081234567890)")

# Bersihkan nomor telepon sebelum pengecekan dan pengiriman
nomor_telepon_bersih = clean_phone_number(nomor_telepon)

# Cek duplikasi input harian
if nomor_telepon_bersih and is_duplicate_entry(worksheet, nomor_telepon_bersih):
    st.error("Anda sudah melakukan input hari ini. Silakan coba lagi besok.")
else:
    # Tombol untuk melakukan prediksi dan menyimpan hasil ke Google Sheets
    if st.button("Prediksi Status Gizi dan Simpan Hasil"):
        # Memastikan nomor telepon memiliki kode negara
        if not nomor_telepon_bersih.startswith("62"):
            nomor_telepon_bersih = "62" + nomor_telepon_bersih.lstrip("0")  # Mengganti '0' di awal dengan '62'

        # Lakukan prediksi
        result_tb_u, result_bb_u, result_bb_tb = predict_status_gizi(jenis_kelamin, usia, tinggi_badan, berat_badan)

        # Tampilkan hasil prediksi di layar
        st.subheader("Hasil Prediksi Status Gizi:")
        st.write(f"TB/U: {result_tb_u}")
        st.write(f"BB/U: {result_bb_u}")
        st.write(f"BB/TB: {result_bb_tb}")

        # Hasil prediksi dalam format pesan
        hasil_prediksi = (
            f"Nama Orang Tua: {nama_orang_tua}\n"
            f"Nama Anak: {nama_anak}\n"
            f"Jenis Kelamin: {jenis_kelamin}\n"
            f"Usia: {usia} bulan\n"
            f"Tinggi Badan: {tinggi_badan} cm\n"
            f"Berat Badan: {berat_badan} kg\n\n"
            f"Hasil Prediksi:\n"
            f"TB/U: {result_tb_u}\n"
            f"BB/U: {result_bb_u}\n"
            f"BB/TB: {result_bb_tb}"
        )

        # Simpan ke Google Sheets
        save_to_google_sheets(worksheet, nama_orang_tua, nama_anak, jenis_kelamin, usia, tinggi_badan, berat_badan, nomor_telepon_bersih, result_tb_u, result_bb_u, result_bb_tb)
        st.success("Data berhasil disimpan ke Google Sheets.")
        
        # Opsi untuk mengirim hasil ke WhatsApp setelah menyimpan
        if st.button("Kirim Hasil ke WhatsApp"):
            whatsapp_status = send_single_message(nomor_telepon_bersih, hasil_prediksi)
            st.success(whatsapp_status)
