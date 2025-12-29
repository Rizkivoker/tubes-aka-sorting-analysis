**Project Overview**

Proyek ini adalah kumpulan skrip Python untuk menganalisis dan memvisualisasikan perbandingan algoritma Merge Sort (rekursif vs iteratif) pada data nama ruangan. Terdapat utilitas generator dataset, GUI untuk eksperimen dan pencatatan metrik, serta dua visualisasi real-time berbasis Pygame.

**Fitur utama**
- Generator dataset nama ruangan acak (`dataset_generator.py`).
- Contoh penggunaan generator (`dataset.py`).
- GUI modern untuk input, generate, perbandingan, dan visualisasi (`sorting_gui.py`).
- Visualisasi Merge Sort interaktif: rekursif (`merge_sort_rekursif.py`) dan side-by-side perbandingan rekursif vs iteratif (`merge_sort_side_by_side.py`).

**Requirements**
- Python 3.8+
- Packages (install via pip): `pygame`, `numpy`, `matplotlib`, `customtkinter`

Contoh instalasi:

```bash
pip install pygame numpy matplotlib customtkinter
```

Catatan: sebagian suara/sintesis audio menggunakan `numpy` + `pygame.sndarray`.

**File overview**
- `dataset_generator.py` : fungsi `generate_room_names(n)` untuk membuat list nama ruangan acak.
- `dataset.py` : contoh singkat pemanggilan generator dan print data.
- `sorting_gui.py` : aplikasi GUI utama (CustomTkinter) untuk memasukkan atau menghasilkan data, menjalankan perbandingan Merge Sort rekursif vs iteratif, merekam waktu & memori, serta menampilkan grafik analisis.
- `merge_sort_rekursif.py` : visualisasi Merge Sort rekursif menggunakan Pygame (masukan: jumlah elemen).
- `merge_sort_side_by_side.py` : visualisasi perbandingan rekursif vs iteratif berdampingan (Pygame), memperlihatkan waktu eksekusi.

**Usage**

1) Jalankan generator contoh:

```bash
python dataset.py
```

2) Jalankan GUI eksperimen:

```bash
python sorting_gui.py
```

Di GUI Anda dapat: menambahkan data manual, memuat file teks/csv, generate dataset otomatis, menjalankan perbandingan (mengukur waktu dan memori), menampilkan grafik, dan membuka visualisasi Merge Sort.

3) Visualisasi Pygame (terminal interactive input):

```bash
python merge_sort_rekursif.py
python merge_sort_side_by_side.py
```

Kedua skrip akan meminta Anda memasukkan jumlah data (n) pada layar Pygame lalu menekan Enter.

**Notes & Tips**
- Untuk dataset besar, pastikan layar dan pengaturan FPS sesuai agar visualisasi tetap responsif.
- Jika `sorting_gui.py` tidak menemukan `dataset_generator.py`, ia menyediakan fallback sederhana — namun direkomendasikan tetap menyimpan `dataset_generator.py` di folder yang sama.
- Gunakan virtual environment untuk mengisolasi dependensi.
