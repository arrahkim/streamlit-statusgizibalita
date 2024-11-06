import requests

# API Token dari Fonnte
api_token = "2yEEZeL6pEZuS9kLaM3m"  # Ganti dengan token API Anda dari Fonnte

def send_single_message(nomor_telepon, message):
    url = "https://api.fonnte.com/send"
    headers = {
        "Authorization": api_token
    }
    data = {
        "target": nomor_telepon,
        "message": message,
        "countryCode": "62",  # Kode negara Indonesia
        "delay": "2"          # Tunda 2 detik (opsional)
    }

    response = requests.post(url, headers=headers, data=data)
    
    # Log respons untuk debugging
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        return "Pesan berhasil dikirim!"
    else:
        error_message = f"Gagal mengirim pesan: {response.text}"
        return error_message