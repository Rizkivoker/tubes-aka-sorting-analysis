Analisis Efisiensi Algoritma: Merge Sort Iteratif vs Rekursif
Tugas Besar Mata Kuliah Analisis Kompleksitas Algoritma (AKA) - Program Studi S1 Informatika - Kelas IF 48 - 12, Telkom University.

👥 **Kelompok Tugas Besar**
Kelompok 4 Beranggotakan : 
- Arfan Ramiro Mahzar - NIM: 103012400182
- Muhammad Ihsan Firjatullah Al-Khasaf - NIM: 103012580061
- Muhammad Rizki Anshari - NIM: 103012580057
  
**Dosen Pengampu** : Dr. Z K ABDURAHMAN BAIZAL, S.Si., M.Kom. Kode Dosen : ZKA
Aplikasi ini bertujuan untuk membandingkan efisiensi waktu eksekusi dan penggunaan memori antara dua pendekatan algoritma Merge Sort: Iteratif dan Rekursif, menggunakan dataset nama ruangan yang diproses secara natural sorting.

🚀 **Fitur Utama**
- Modern GUI: Antarmuka berbasis CustomTkinter dengan dukungan Dark Mode.
- Dual Approach Sorting: Implementasi Merge Sort secara Iteratif dan Rekursif.
- Dataset Generator: Membuat data acak nama ruangan secara otomatis (n data).
- Pengukuran Real-time: Menampilkan waktu eksekusi (detik) dan penggunaan memori (KB).
- Visualisasi Side-by-Side: Visualisasi proses pengurutan menggunakan Pygame untuk melihat perbedaan langkah algoritma secara grafis dan audio.
- Analisis Performa: Menampilkan grafik perbandingan menggunakan Matplotlib dan memberikan kesimpulan algoritma mana yang lebih efisien.

🛠️ **Prasyarat (Prerequisites)**
Sebelum menjalankan aplikasi, pastikan Anda telah menginstal Python (versi 3.10 atau lebih baru) dan library berikut:
- pip install customtkinter pygame matplotlib numpy

Aplikasi yang dibuat menggunakan library :
- customtkinter
- pygame
- matplotlib
- numpy

📂 **Struktur File**
- sorting_gui.py: File utama untuk menjalankan aplikasi GUI modern.
- merge_sort_side_by_side.py: Program visualisasi Pygame (Rekursif vs Iteratif).
- dataset_generator.py: Modul untuk menghasilkan dataset nama ruangan secara acak.
- dataset.py: berfungsi sebagai penyimpanan (storage) atau pengelola data statis yang digunakan sebagai sumber data awal sebelum dilakukan manipulasi (seperti pengurutan atau penambahan data baru)

💻 **Cara Menjalankan**
1. Clone Repositori:
   - git clone https://github.com/Rizkivoker/tubes-aka-sorting-analysis.git

2. Buat Virtual Environment untuk menjalankan aplikasi
   Jalankan command/perintah berikut di terminal dan direktori aplikasi yang benar
   - python -m venv venv 
   - venv\Scripts\activate 

3. Jalankan Aplikasi Utama:
   - python sorting_gui.py
   - lakukan generate data sebanyak n data, lalu lakukan Compare Both untuk membandingkan merge sort rekursif dengan iteratif
   - tampilkan grafik perbandingan setelah melakukan Compare Both lebih dari 1 kali untuk melihat perbandingan
   - Analisis perbandingan menampilkan hasil dari pengujian yang dilakukan pengguna
   - Visualisasi Merge Sort berfungsi untuk memvisualisasikan perbandingan antara algoritma Merge Sort Rekursif dengan Iteratif dengan cara input n data di window aplikasi

📊 **Hasil Analisis**
Berdasarkan pengujian yang dilakukan, algoritma akan memberikan output berupa:
- Waktu eksekusi dalam satuan milidetik.
- Puncak penggunaan memori (Peak Memory).
- Grafik tren performa seiring bertambahnya jumlah n data


💻 **Project Overview**
Proyek ini adalah kumpulan skrip Python untuk menganalisis dan memvisualisasikan perbandingan algoritma Merge Sort (rekursif vs iteratif) pada data nama ruangan. Terdapat utilitas generator dataset, GUI untuk eksperimen dan pencatatan metrik, serta dua visualisasi real-time berbasis Pygame.

Catatan: sebagian suara/sintesis audio menggunakan `numpy` + `pygame.sndarray`.

💻 **File overview**
- `dataset_generator.py` : fungsi `generate_room_names(n)` untuk membuat list nama ruangan acak.
- `dataset.py` : contoh singkat pemanggilan generator dan print data.
- `sorting_gui.py` : aplikasi GUI utama (CustomTkinter) untuk memasukkan atau menghasilkan data, menjalankan perbandingan Merge Sort rekursif vs iteratif, merekam waktu & memori, serta menampilkan grafik analisis.
- `merge_sort_rekursif.py` : visualisasi Merge Sort rekursif menggunakan Pygame (masukan: jumlah elemen).
- `merge_sort_side_by_side.py` : visualisasi perbandingan rekursif vs iteratif berdampingan (Pygame), memperlihatkan waktu eksekusi.

