import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Fungsi untuk menghubungkan ke Google Sheets menggunakan ID Spreadsheet
def init_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    
    # Membaca kredensial JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    
    # Ganti dengan ID Spreadsheet Anda
    spreadsheet_id = "18onZkr9wvTq3BCQf2NvhICcBYAMW6l7c8O9T4SBCggA"
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # Pilih worksheet pertama
    return worksheet

# Fungsi untuk membersihkan nomor telepon dari karakter tambahan
def clean_phone_number(nomor_telepon):
    # Pastikan nomor telepon adalah string
    nomor_telepon = str(nomor_telepon)
    # Hapus karakter non-digit dan tanda kutip yang mungkin ada di sekitar nomor telepon
    cleaned_number = nomor_telepon.strip().replace("‘", "").replace("’", "").replace("'", "").replace('"', "")
    return cleaned_number

# Fungsi untuk memeriksa apakah nomor sudah melakukan input hari ini
def is_duplicate_entry(worksheet, nomor_telepon):
    records = worksheet.get_all_records()
    tanggal_hari_ini = datetime.now().strftime("%Y-%m-%d")
    for record in records:
        # Gunakan nomor telepon yang sudah dibersihkan
        if clean_phone_number(record.get("nomor_telepon", "")) == clean_phone_number(nomor_telepon) and record.get("tanggal") == tanggal_hari_ini:
            return True
    return False

# Fungsi untuk menyimpan data input ke Google Sheets
def save_to_google_sheets(worksheet, nama_orang_tua, nama_anak, jenis_kelamin, usia, tinggi_badan, berat_badan, nomor_telepon, result_tb_u, result_bb_u, result_bb_tb):
    tanggal_hari_ini = datetime.now().strftime("%Y-%m-%d")
    worksheet.append_row([tanggal_hari_ini, nama_orang_tua, nama_anak, jenis_kelamin, usia, tinggi_badan, berat_badan, clean_phone_number(nomor_telepon), result_tb_u, result_bb_u, result_bb_tb])
