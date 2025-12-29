import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import time
import tracemalloc
import re
import matplotlib.pyplot as plt

# Pastikan file dataset_generator.py ada di folder yang sama
try:
    from dataset_generator import generate_room_names
except ImportError:
    def generate_room_names(n):
        # Fallback sederhana jika file generator tidak ditemukan
        import random
        prefixes = ["Ruang", "Lab", "A", "B", "R"]
        return [f"{random.choice(prefixes)}.{random.randint(1, 500)}" for _ in range(n)]

#  Konfigurasi Tema 
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue") 

#  FUNGSI PEMBANDING (NATURAL SORTING) 
def natural_keys(text):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

#  ALGORITMA SORTING 
def merge_sort_recursive(arr):
    if len(arr) <= 1: return arr[:]
    mid = len(arr) // 2
    left = merge_sort_recursive(arr[:mid])
    right = merge_sort_recursive(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if natural_keys(left[i]) <= natural_keys(right[j]):
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:]); merged.extend(right[j:])
    return merged

def merge_sort_iterative(arr):
    n = len(arr)
    if n <= 1: return arr[:]
    result = arr[:]
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = result[i : i + width]
            right = result[i + width : i + 2 * width]
            li = ri = 0
            merged = []
            while li < len(left) and ri < len(right):
                if natural_keys(left[li]) <= natural_keys(right[ri]):
                    merged.append(left[li]); li += 1
                else:
                    merged.append(right[ri]); ri += 1
            merged.extend(left[li:]); merged.extend(right[ri:])
            result[i : i + len(merged)] = merged
        width *= 2
    return result

# GLOBAL HISTORY UNTUK GRAFIK 
history_n = []
history_time_iter = []
history_time_rec = []

def measure_function(func, *args):
    tracemalloc.start()
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak / 1024.0

class SortingAppModern(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App: Perbandingan Algoritma Merge Sort(Rekursif vs Iteratif) Pada Data Nama Ruangan")
        self.geometry("1100x900")
        self.data = []
        
        self.grid_columnconfigure(0, weight=1)
        self.setup_ui()

    def setup_ui(self):
        # 1. Header
        self.header = ctk.CTkLabel(self, text="ANALISIS EFISIENSI ALGORITMA MERGE SORT: REKURSIF VS ITERATIF PADA DATA RUANGAN", 
                                   font=ctk.CTkFont(size=22, weight="bold"), text_color="white")
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. Frame Input Data Manual
        self.frm_input = ctk.CTkFrame(self)
        self.frm_input.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frm_input, text="Input Data Nama Ruangan", text_color="white", 
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.entry = ctk.CTkEntry(self.frm_input, placeholder_text="Contoh: Ruang 1, Ruang 2", width=450)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        
        # Tombol Tambah Data
        ctk.CTkButton(self.frm_input, text="Tambah Data", font=ctk.CTkFont(weight="bold"), 
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.add_from_entry).grid(row=1, column=1, padx=5)
        
        # Tombol Load File
        ctk.CTkButton(self.frm_input, text="Load File", font=ctk.CTkFont(weight="bold"), 
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.load_from_file).grid(row=1, column=2, padx=5)
        
        # Tombol Clear Dataset
        ctk.CTkButton(self.frm_input, text="Clear Dataset", fg_color="transparent", border_width=1, 
                     command=self.clear_all).grid(row=1, column=3, padx=5)

        # 3. Frame Generator Dataset Otomatis
        self.frm_gen = ctk.CTkFrame(self)
        self.frm_gen.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frm_gen, text="Generator Dataset Otomatis", text_color="white", 
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.entry_gen = ctk.CTkEntry(self.frm_gen, placeholder_text="Masukkan jumlah n data", width=200)
        self.entry_gen.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        # Tombol Generate Data
        ctk.CTkButton(self.frm_gen, text="Generate Data", font=ctk.CTkFont(weight="bold"), 
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.generate_dataset).grid(row=1, column=1, padx=5, sticky="w")

        # 4. Frame Preview Data
        self.frm_preview = ctk.CTkFrame(self)
        self.frm_preview.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frm_preview, text="Preview Data (Nama Ruangan)", text_color="white", 
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        
        self.textbox_preview = ctk.CTkTextbox(self.frm_preview, height=120)
        self.textbox_preview.pack(fill="both", expand=True, padx=10, pady=10)

        # 5. Frame Sorting & Pengukuran
        self.frm_ctrl = ctk.CTkFrame(self)
        self.frm_ctrl.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frm_ctrl, text="Sorting & Pengukuran", text_color="white", 
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w", columnspan=5)

        # Tombol Compare Both
        ctk.CTkButton(self.frm_ctrl, text="Compare Both", font=ctk.CTkFont(weight="bold"),
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.compare_both).grid(row=1, column=0, padx=10, pady=10)

        # Tombol Tampilkan Grafik
        ctk.CTkButton(self.frm_ctrl, text="Tampilkan Grafik", font=ctk.CTkFont(weight="bold"),
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.show_plot).grid(row=1, column=1, padx=10)

        # Tombol Analisis Perbandingan
        ctk.CTkButton(self.frm_ctrl, text="Analisis Perbandingan", font=ctk.CTkFont(weight="bold"),
                     fg_color="#1F538D", hover_color="#00BFFF", 
                     text_color="white", border_width=2, border_color="#FFFFFF",
                     command=self.show_analysis).grid(row=1, column=2, padx=10)

        # Tombol Visualisasi 
        ctk.CTkButton(
            self.frm_ctrl, 
            text="Visualisasi Merge Sort", 
            fg_color="#FFD700",      #FFFF00    FFD700
            hover_color="#FFFF00",   #B8860B
            text_color="black", 
            font=ctk.CTkFont(weight="bold"), 
            border_width=2, 
            border_color="#FFFFFF", 
            command=self.open_visualization
        ).grid(row=1, column=3, padx=10)

        # Tombol Reset 
        ctk.CTkButton(
            self.frm_ctrl, 
            text="Reset Semua", 
            fg_color="#8B0000",      
            hover_color="#FF4B4B",   
            text_color="white",      
            font=ctk.CTkFont(weight="bold"), 
            border_width=2, 
            border_color="#FFFFFF", 
            command=self.clear_all_full
        ).grid(row=1, column=4, padx=10)

        # 6. Log Output & Hasil
        ctk.CTkLabel(self, text="Log Output & Hasil Sorting Lengkap", text_color="white", 
                     font=ctk.CTkFont(weight="bold")).grid(row=5, column=0, padx=20, sticky="w")
        
        self.txt_result = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.txt_result.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.grid_rowconfigure(6, weight=1)

    # LOGIC METHODS 
    def generate_dataset(self):
        try:
            n_text = self.entry_gen.get().strip()
            if not n_text: return
            n = int(n_text)
            if n <= 0: raise ValueError
            
            self.data = generate_room_names(n)
            self.update_preview()
            
            self.txt_result.insert("end", f"\n[GENERATED] {n} data nama ruangan baru berhasil dibuat.\n")
            self.txt_result.insert("end", f"Data: {', '.join(self.data[:15])}{'...' if n > 15 else ''}\n")
            self.txt_result.see("end")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka jumlah data yang valid.")

    def add_from_entry(self):
        val = self.entry.get().strip()
        if val:
            items = [i.strip() for i in val.split(",") if i.strip()]
            self.data.extend(items)
            self.update_preview()
            self.txt_result.insert("end", f"\n[INPUT] Menambahkan data manual: {val}\n")
            self.entry.delete(0, 'end')

    def update_preview(self):
        self.textbox_preview.delete("1.0", "end")
        self.textbox_preview.insert("end", "\n".join(self.data))

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt *.csv")])
        if path:
            with open(path, 'r') as f:
                for line in f:
                    if line.strip(): self.data.append(line.strip())
            self.update_preview()
            self.txt_result.insert("end", f"\n[LOAD] Berhasil memuat data dari file luar.\n")

    def compare_both(self):
        if not self.data:
            messagebox.showwarning("Warning", "Dataset masih kosong!")
            return
            
        arr_to_sort = self.data[:]
        
        # Eksekusi Pengukuran
        res_i, t_i, m_i = measure_function(merge_sort_iterative, arr_to_sort)
        res_r, t_r, m_r = measure_function(merge_sort_recursive, arr_to_sort)
        
        # Output Log Metadata
        self.txt_result.insert("end", f"\n{'='*65}\nHASIL PERBANDINGAN SORTING (n={len(arr_to_sort)})\n{'='*65}\n")
        self.txt_result.insert("end", f"1. Merge Sort Iteratif: {t_i:.6f} detik | Memori: {m_i:.2f} KB\n")
        self.txt_result.insert("end", f"2. Merge Sort Rekursif: {t_r:.6f} detik | Memori: {m_r:.2f} KB\n")
        
        # Menampilkan HASIL SORTING LENGKAP
        self.txt_result.insert("end", f"\nHasil Sorting:\n")
        self.txt_result.insert("end", f"{', '.join(res_i)}\n")
        self.txt_result.insert("end", f"{'='*65}\n")
        self.txt_result.see("end")
        
        # Simpan ke history untuk grafik
        history_n.append(len(arr_to_sort))
        history_time_iter.append(t_i)
        history_time_rec.append(t_r)

    def show_analysis(self):
        if not history_n:
            messagebox.showerror("Error", "Belum ada riwayat eksperimen untuk dianalisis.")
            return
        
        # Hitung rata-rata waktu
        avg_i = sum(history_time_iter) / len(history_time_iter)
        avg_r = sum(history_time_rec) / len(history_time_rec)
        
        # Tentukan kesimpulan
        if avg_i < avg_r:
            selisih = avg_r - avg_i
            kesimpulan = f"KESIMPULAN:\nMetode ITERATIF lebih cepat sekitar {selisih:.6f} detik dibandingkan metode Rekursif pada dataset ini."
        elif avg_r < avg_i:
            selisih = avg_i - avg_r
            kesimpulan = f"KESIMPULAN:\nMetode REKURSIF lebih cepat sekitar {selisih:.6f} detik dibandingkan metode Iteratif pada dataset ini."
        else:
            kesimpulan = "KESIMPULAN:\nKedua metode memiliki performa waktu yang identik."

        # Tampilkan dalam MessageBox
        messagebox.showinfo("Analisis Perbandingan Algoritma", 
                            f"Hasil Rata-rata Pengujian (n={sum(history_n)/len(history_n):.0f} data):\n\n"
                            f"• Rata-rata Iteratif : {avg_i:.6f} detik\n"
                            f"• Rata-rata Rekursif : {avg_r:.6f} detik\n\n"
                            f"{kesimpulan}")
        
        # Tambahkan juga ke Log Output agar terekam
        self.txt_result.insert("end", f"\n[ANALISIS] {kesimpulan.replace('KESIMPULAN:', '')}\n")
        self.txt_result.see("end")

    def show_plot(self):
        if not history_n: return
        plt.figure("Analisis Performa Merge Sort")
        # Sort data berdasarkan n agar garis grafik tidak berantakan
        sn, si, sr = zip(*sorted(zip(history_n, history_time_iter, history_time_rec)))
        plt.plot(sn, si, marker='o', linestyle='-', color='blue', label="Iteratif")
        plt.plot(sn, sr, marker='s', linestyle='-', color='red', label="Rekursif")
        plt.xlabel("Jumlah Data (n)")
        plt.ylabel("Waktu Eksekusi (detik)")
        plt.title("Grafik Perbandingan Waktu: Iteratif vs Rekursif")
        plt.legend()
        plt.grid(True)
        plt.show()

    def open_visualization(self):
        try:
            subprocess.Popen(["python", "merge_sort_side_by_side.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menjalankan file visualisasi: {e}")

    def clear_all(self):
        self.data = []
        self.update_preview()
        self.txt_result.insert("end", "\n[CLEAR] Dataset preview telah dibersihkan.\n")

    def clear_all_full(self):
        self.clear_all()
        self.txt_result.delete("1.0", "end")
        self.entry_gen.delete(0, 'end')
        global history_n, history_time_iter, history_time_rec
        history_n, history_time_iter, history_time_rec = [], [], []

if __name__ == "__main__":
    app = SortingAppModern()
    app.mainloop()