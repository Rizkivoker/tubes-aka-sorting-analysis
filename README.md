Analisis Efisiensi Algoritma: Merge Sort Iteratif vs Rekursif
Tugas Besar Mata Kuliah Analisis Kompleksitas Algoritma (AKA) - Program Studi S1 Informatika - Kelas IF 48 - 12, Telkom University.

👥 Kelompok Tugas Besar
Kelompok 4 Beranggotakan : 
- Arfan Ramiro Mahzar - NIM: 103012400182
- Muhammad Ihsan Firjatullah Al-Khasaf - NIM: 103012580061
- Muhammad Rizki Anshari - NIM: 103012580057
  
Dosen Pengampu : Dr. Z K ABDURAHMAN BAIZAL, S.Si., M.Kom. Kode Dosen : ZKA
Aplikasi ini bertujuan untuk membandingkan efisiensi waktu eksekusi dan penggunaan memori antara dua pendekatan algoritma Merge Sort: Iteratif dan Rekursif, menggunakan dataset nama ruangan yang diproses secara natural sorting.

🚀 Fitur Utama
- Modern GUI: Antarmuka berbasis CustomTkinter dengan dukungan Dark Mode.
- Dual Approach Sorting: Implementasi Merge Sort secara Iteratif dan Rekursif.
- Dataset Generator: Membuat data acak nama ruangan secara otomatis (n data).
- Pengukuran Real-time: Menampilkan waktu eksekusi (detik) dan penggunaan memori (KB).
- Visualisasi Side-by-Side: Visualisasi proses pengurutan menggunakan Pygame untuk melihat perbedaan langkah algoritma secara grafis dan audio.
- Analisis Performa: Menampilkan grafik perbandingan menggunakan Matplotlib dan memberikan kesimpulan algoritma mana yang lebih efisien.

🛠️ Prasyarat (Prerequisites)
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal Python (versi 3.10 atau lebih baru) dan library berikut:
- pip install customtkinter pygame matplotlib numpy

📂 Struktur File
- sorting_gui.py: File utama untuk menjalankan aplikasi GUI modern.
- merge_sort_side_by_side.py: Program visualisasi Pygame (Rekursif vs Iteratif).
- dataset_generator.py: Modul untuk menghasilkan dataset nama ruangan secara acak.
- dataset.py: berfungsi sebagai penyimpanan (storage) atau pengelola data statis yang digunakan sebagai sumber data awal sebelum dilakukan manipulasi (seperti pengurutan atau penambahan data baru)

💻 Cara Menjalankan
1. Clone Repositori:
   - git clone https://github.com/Rizkivoker/tubes-aka-sorting-analysis.git

2. Jalankan Aplikasi Utama:
   - python sorting_gui.py
  
📊 Hasil Analisis
Berdasarkan pengujian yang dilakukan, algoritma akan memberikan output berupa:
- Waktu eksekusi dalam satuan milidetik.
- Puncak penggunaan memori (Peak Memory).
- Grafik tren performa seiring bertambahnya jumlah $n$.