# 🔧 Backend API - SIBI Reader

**SIBI Reader** adalah aplikasi cerdas berbasis Deep Learning yang dapat mengenali gerakan tangan pengguna dan mengubahnya menjadi teks secara otomatis. Backend ini dibangun menggunakan **FastAPI** dan dilengkapi model klasifikasi berbasis **ResNet** untuk mengenali citra tangan.

---

## 🚀 Fitur Utama

- 🔍 Pengenalan gesture tangan menggunakan model Deep Learning (.keras)
- 📷 Endpoint API untuk menerima dan memproses gambar
- 🧠 Integrasi dengan model ResNet untuk klasifikasi gerakan
- ⚡ Performa tinggi berkat framework FastAPI

---

## 🗂️ Struktur Folder
```bash
SIBI-Backend/
├── app/
│ ├── main.py # Entry point FastAPI
│ ├── model/
│ │ └── resnet.keras # Trained ResNet model
│ └── utils/
│ ├── hand_landmarker.task # File landmark tangan
│ └── predict.py # Fungsi prediksi gesture
├── images/
│ ├── raw/ # Folder gambar mentah
│ └── preprocess/ # Folder gambar hasil preprocessing
├── requirements.txt # Daftar dependensi Python
```  
## 📦 Instalasi Lokal

1. **Clone repo**:

```bash
git clone https://github.com/USERNAME/SIBI-Backend.git
cd SIBI-Backend
``` 
2. **Aktifkan virtual environment (opsional)**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. **Install dependensi**:
```bash
pip install -r requirements.txt
```
4. **Jalankan server**:
```bash
uvicorn app.main:app --reload
```

## 🛠️ Endpoint API
| Method | Endpoint   | Deskripsi   |
| ------ | ---------- | ----------- |
| POST   | `/predict` | Menerima gambar & mengembalikan prediksi gesture |


Contoh penggunaan bisa dikembangkan melalui frontend kamera atau aplikasi mobile.

## 🧠 Tentang Model
Model resnet.keras dilatih untuk mengenali gesture tangan berdasarkan data yang telah melalui preprocessing dan ekstraksi landmark menggunakan Mediapipe.

## 🧑‍💻 Tim Pengembang
Proyek ini dikembangkan oleh Laskar AI
ID Tim: LAI25-SM016