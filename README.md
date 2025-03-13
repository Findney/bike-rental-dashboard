# Bike Rental Dashboard
Hasil: https://bike-rental-dashboard-am.streamlit.app

## Instalasi
Pastikan Anda memiliki **Python 3.8 atau lebih baru** dan **pip** terinstal di sistem Anda.

### 1. Clone repository ini
```bash
git clone https://github.com/Findney/bike-rental-dashboard.git
cd bike-rental-dashboard
```

### 2. Buat Virtual Environment (Opsional)
Disarankan menggunakan environment virtual untuk mengelola dependensi.

#### Menggunakan venv:
```bash
python -m venv env
source env/bin/activate  # Untuk macOS/Linux
env\Scripts\activate  # Untuk Windows
```

#### Menggunakan Conda:
```bash
conda create --name bike_env python=3.8
conda activate bike_env
```

### 3. Instal dependensi
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi
Jalankan perintah berikut untuk memulai aplikasi:
```bash
streamlit run dashboard.py --server.runOnSave=True
```

Akses dashboard melalui browser di `http://localhost:8501`

---
Dibuat oleh **Agil Mughni**

