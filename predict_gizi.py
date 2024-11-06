import pandas as pd
import joblib

# Memuat model yang sudah dilatih
model_tb_u = joblib.load('rf_model_tb_u_6040.pkl')   # Model untuk TB/U
model_bb_u = joblib.load('rf_model_bb_u_8020.pkl')   # Model untuk BB/U
model_bb_tb = joblib.load('rf_model_bb_tb_9010.pkl') # Model untuk BB/TB

# Fungsi untuk membuat input DataFrame sesuai data pelatihan
def create_input_dataframe(jenis_kelamin, usia, tinggi_badan, berat_badan):
    jenis_kelamin_encoded = 1 if jenis_kelamin.lower() == 'laki-laki' else 0
    input_tb_u = pd.DataFrame([[jenis_kelamin_encoded, usia, tinggi_badan]],
                              columns=['Jenis Kelamin', 'Usia Saat Ukur (bulan)', 'Tinggi (cm)'])
    input_bb_u = pd.DataFrame([[jenis_kelamin_encoded, berat_badan, usia]],
                              columns=['Jenis Kelamin', 'Berat (kg)', 'Usia Saat Ukur (bulan)'])
    input_bb_tb = pd.DataFrame([[jenis_kelamin_encoded, berat_badan, tinggi_badan, usia]],
                               columns=['Jenis Kelamin', 'Berat (kg)', 'Tinggi (cm)', 'Usia Saat Ukur (bulan)'])
    return input_tb_u, input_bb_u, input_bb_tb

# Fungsi untuk melakukan prediksi status gizi
def predict_status_gizi(jenis_kelamin, usia, tinggi_badan, berat_badan):
    input_tb_u, input_bb_u, input_bb_tb = create_input_dataframe(jenis_kelamin, usia, tinggi_badan, berat_badan)
    pred_tb_u = model_tb_u.predict(input_tb_u)[0]
    pred_bb_u = model_bb_u.predict(input_bb_u)[0]
    pred_bb_tb = model_bb_tb.predict(input_bb_tb)[0]

    status_gizi_tb_u = {0: 'Sangat Pendek', 1: 'Pendek', 2: 'Normal', 3: 'Tinggi'}
    status_gizi_bb_u = {0: 'Berat Badan Sangat Kurang', 1: 'Berat Badan Kurang', 2: 'Berat Badan Normal', 3: 'Berat Badan Berisiko Lebih'}
    status_gizi_bb_tb = {0: 'Gizi Buruk', 1: 'Gizi Kurang', 2: 'Gizi Normal', 3: 'Gizi Berisiko Lebih', 4: 'Gizi Lebih', 5: 'Obesitas'}

    result_tb_u = status_gizi_tb_u.get(pred_tb_u, "Unknown")
    result_bb_u = status_gizi_bb_u.get(pred_bb_u, "Unknown")
    result_bb_tb = status_gizi_bb_tb.get(pred_bb_tb, "Unknown")

    return result_tb_u, result_bb_u, result_bb_tb
