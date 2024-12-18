#**E-commerce Dashboard**

Aplikasi interaktif untuk menganalisis data e-commerce menggunakan Python dan Streamlit. Beberapa pertanyaan yang bisa dijawab dengan dashboard ini:
- Produk apa yang paling banyak dan paling sedikit terjual?
- Bagaimana demografi pelanggan kita?
- Kapan terakhir kali pelanggan melakukan transaksi?

##Cara Menjalankan Dashboard

###1. Persyaratan Sistem
Pastikan Anda memiliki:
- Python 3.8 atau lebih baru
- Paket Python yang diperlukan (lihat bagian "Instalasi")

###2. Instalasi
1. Clone repositori atau unduh file sumber kode ke komputer Anda.
2. Buka terminal/command prompt dan navigasikan ke direktori proyek.
3. Instal dependensi dengan perintah:

   ```bash
   pip install -r requirements.txt
   ```

   Jika belum ada `requirements.txt`, instal paket-paket berikut secara manual:

   ```bash
   pip install pandas matplotlib seaborn streamlit babel
   ```

###3. Menyiapkan Data
1. Pastikan Anda memiliki file data `main_data.csv`.
2. Letakkan file tersebut di direktori proyek atau sesuaikan path dalam kode:

   ```python
   main_data = pd.read_csv(r'D:\proyek_analisis_data\dicoding\main_data.csv')
   ```
- **Local URL**:  
  - `http://localhost:8502`: URL ini digunakan untuk mengakses dashboard di komputer yang menjalankan Streamlit. Anda bisa mengaksesnya langsung dari browser di mesin yang sama.

###4. Menjalankan Dashboard
- Di Visual Studio Code (VSC):
  - Buka file `dashboard.py` dan klik tombol Run Python File.
  - URL Streamlit akan muncul di terminal:
    - Local URL: `http://localhost:8502`
    - Network URL: `http://192.168.1.6:8502`
  - Klik URL untuk membuka dashboard.

- Di Terminal:
  - Jalankan perintah:

    ```bash
    streamlit run dashboard.py
    ```

  - URL lokal akan muncul di terminal: `http://localhost:8502`. Untuk akses di jaringan, gunakan Network URL yang tertera.

###5. Menggunakan Dashboard
- Jelajahi fitur dashboard:
  - Produk paling banyak dan paling sedikit terjual
  - Demografi pelanggan berdasarkan kota
  - Waktu transaksi terakhir

##Fitur Utama
- Visualisasi Data: Menggunakan Matplotlib dan Seaborn untuk grafik.
- Interaktivitas: Dibangun dengan Streamlit untuk pengalaman pengguna yang mudah.
- Analisis E-commerce: Insight penting tentang penjualan, pelanggan, dan performa produk.

##Catatan
- Pastikan data dan dependensi sudah benar.
- Hubungi pengembang untuk bantuan lebih lanjut.

---

**Selamat menggunakan E-commerce Dashboard!**

---