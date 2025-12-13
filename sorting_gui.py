import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import tracemalloc
import csv
import matplotlib.pyplot as plt
from dataset_generator import generate_room_names

# Sorting algorithms

def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def merge_sort_iterative(arr):
    n = len(arr)
    if n <= 1:
        return arr[:]
    result = arr[:]
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = result[i:i+width]
            right = result[i+width:i+2*width]
            li = ri = 0
            merged = []
            while li < len(left) and ri < len(right):
                if left[li] <= right[ri]:
                    merged.append(left[li]); li += 1
                else:
                    merged.append(right[ri]); ri += 1
            merged.extend(left[li:])
            merged.extend(right[ri:])
            result[i:i+2*width] = merged
        width *= 2
    return result


# Globals for experiment history

history_n = []
history_time_iter = []
history_time_rec = []


# Measurement helper

def measure_function(func, *args, **kwargs):
    """
    Returns tuple (result, elapsed_seconds, peak_kb).
    Uses tracemalloc to measure peak memory during function execution.
    """
    tracemalloc.start()
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024.0
    return result, elapsed, peak_kb


# Plot & Analysis functions (module-level)

def show_plot():
    if not history_n:
        messagebox.showerror("Error", "Belum ada data perbandingan. Jalankan Compare Both terlebih dahulu.")
        return
    plt.figure(figsize=(8,4.5))
    plt.plot(history_n, history_time_iter, marker='o', label="Iteratif (Merge Sort)")
    plt.plot(history_n, history_time_rec, marker='o', label="Rekursif (Merge Sort)")
    plt.title("Perbandingan Running Time")
    plt.xlabel("Jumlah Data (n)")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def show_analysis():
    if not history_n:
        messagebox.showerror("Error", "Belum ada data untuk dianalisis.")
        return

    avg_iter = sum(history_time_iter) / len(history_time_iter)
    avg_rec = sum(history_time_rec) / len(history_time_rec)

    if avg_rec < avg_iter:
        faster = "Rekursif Merge Sort lebih cepat rata-rata."
    elif avg_rec > avg_iter:
        faster = "Iteratif Merge Sort lebih cepat rata-rata."
    else:
        faster = "Keduanya memiliki kecepatan rata-rata yang sama."

    analysis_text = (
        f"Jumlah percobaan : {len(history_n)} kali\n\n"
        f"Rata-rata waktu Iteratif : {avg_iter:.6f} detik\n"
        f"Rata-rata waktu Rekursif : {avg_rec:.6f} detik\n\n"
        f"Kesimpulan:\n{faster}\n\n"
        f"Catatan: perbedaan cenderung meningkat seiring bertambahnya n."
    )
    messagebox.showinfo("Analisis Perbandingan", analysis_text)

# reset histori perbandingan (module-level)
def reset_history():
    global history_n, history_time_iter, history_time_rec
    history_n.clear()
    history_time_iter.clear()
    history_time_rec.clear()
    # Try clearing the textbox if app exists
    try:
        app.txt_result.delete("1.0", tk.END)
    except Exception:
        pass
    messagebox.showinfo("Reset History", "History running time dan analisis sudah direset.\nSilakan mulai eksperimen dari awal.")

# GUI App

class SortingApp:
    def __init__(self, root):
        self.root = root
        root.title("Analisis Efisiensi: Iteratif vs Rekursif (Sorting)")
        root.geometry("920x640")

        # Frame input
        frm_input = ttk.LabelFrame(root, text="Input Data Nama Ruangan")
        frm_input.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm_input, text="Masukkan (pisah koma):").grid(row=0, column=0, sticky="w")
        self.entry = ttk.Entry(frm_input, width=88)
        self.entry.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        ttk.Button(frm_input, text="Add (entry)", command=self.add_from_entry).grid(row=0, column=2, padx=4)
        ttk.Button(frm_input, text="Load from file...", command=self.load_from_file).grid(row=0, column=3, padx=4)
        ttk.Button(frm_input, text="Clear all", command=self.clear_all).grid(row=0, column=4, padx=4)

        # Frame list & CRUD
        frm_list = ttk.LabelFrame(root, text="Data (List)")
        frm_list.pack(fill="both", expand=True, padx=8, pady=6)

        columns = ("#1",)
        self.tree = ttk.Treeview(frm_list, columns=columns, show="headings", height=16)
        self.tree.heading("#1", text="Nama Ruangan")
        self.tree.pack(side="left", fill="both", expand=True, padx=(6,0), pady=6)

        vsb = ttk.Scrollbar(frm_list, orient="vertical", command=self.tree.yview)
        vsb.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        frm_buttons = ttk.Frame(frm_list)
        frm_buttons.pack(side="left", fill="y", padx=6)
        ttk.Button(frm_buttons, text="Delete selected", command=self.delete_selected).pack(fill="x", pady=4)
        ttk.Button(frm_buttons, text="Count", command=self.show_count).pack(fill="x", pady=4)

        # Frame sorting controls
        frm_sort = ttk.LabelFrame(root, text="Sorting & Pengukuran")
        frm_sort.pack(fill="x", padx=8, pady=6)

        ttk.Button(frm_sort, text="Run Iteratif (Merge Sort)", command=self.run_iterative).grid(row=0, column=0, padx=6, pady=6)
        ttk.Button(frm_sort, text="Run Rekursif (Merge Sort)", command=self.run_recursive).grid(row=0, column=1, padx=6, pady=6)
        ttk.Button(frm_sort, text="Compare Both (single run)", command=self.compare_both).grid(row=0, column=2, padx=6, pady=6)
        ttk.Button(frm_sort, text="Export results to CSV", command=self.export_csv).grid(row=0, column=3, padx=6, pady=6)

        # quick access for plot, analysis, reset
        frm_extra = ttk.Frame(root)
        frm_extra.pack(fill="x", padx=8, pady=(0,6))
        ttk.Button(frm_extra, text="Tampilkan Grafik Running Time", command=show_plot).pack(side="left", padx=6)
        ttk.Button(frm_extra, text="Tampilkan Analisis Perbandingan", command=show_analysis).pack(side="left", padx=6)
        ttk.Button(frm_extra, text="Reset History", command=reset_history).pack(side="left", padx=6)
        ttk.Button(frm_extra, text="Clear Hasil", command=self.clear_results).pack(side="left", padx=6)
        ttk.Button(frm_extra, text="Reset TOTAL", command=self.clear_all_full).pack(side="left", padx=6)

        # Frame generate dataset
        frm_generate = ttk.LabelFrame(root, text="Generate Dataset Otomatis")
        frm_generate.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm_generate, text="Jumlah data:").pack(side="left", padx=4)
        self.entry_generate = ttk.Entry(frm_generate, width=12)
        self.entry_generate.pack(side="left", padx=4)
        ttk.Button(frm_generate, text="Generate", command=self.generate_dataset).pack(side="left", padx=4)

        # Frame results
        frm_result = ttk.LabelFrame(root, text="Hasil")
        frm_result.pack(fill="both", expand=True, padx=8, pady=6)

        self.txt_result = tk.Text(frm_result, height=14)
        self.txt_result.pack(fill="both", expand=True, padx=6, pady=6)

        # internal state
        self.data = []

    # Methods

    def generate_dataset(self):
        try:
            n = int(self.entry_generate.get())
            if n < 0:
                raise ValueError
            data = generate_room_names(n)
            self.clear_all()
            for item in data:
                self.add_item(item)
            messagebox.showinfo("Success", f"Dataset {n} item berhasil dibuat.")
        except ValueError:
            messagebox.showerror("Error", "Input harus berupa bilangan bulat positif.")

    def add_from_entry(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Isi dulu entry.")
            return
        items = [s.strip() for s in text.split(",") if s.strip()]
        for it in items:
            self.add_item(it)
        self.entry.delete(0, tk.END)

    def add_item(self, item):
        self.data.append(item)
        self.tree.insert("", "end", values=(item,))

    def load_from_file(self):
        path = filedialog.askopenfilename(title="Pilih file txt/CSV", filetypes=[("Text files","*.txt *.csv"), ("All files","*.*")])
        if not path:
            return
        loaded = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "," in line:
                    parts = [p.strip() for p in line.split(",") if p.strip()]
                    loaded.extend(parts)
                else:
                    loaded.append(line)
        for it in loaded:
            self.add_item(it)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih item dulu.")
            return
        for s in sel:
            val = self.tree.item(s)["values"][0]
            try:
                self.data.remove(val)
            except ValueError:
                pass
            self.tree.delete(s)

    def clear_all(self):
        self.data = []
        for row in self.tree.get_children():
            self.tree.delete(row)

    def clear_results(self):
        """Clear only the results textbox."""
        self.txt_result.delete("1.0", tk.END)

    def clear_all_full(self):
        """Clear dataset, results textbox, and history (full reset)."""
        self.clear_all()
        self.clear_results()
        reset_history()

    def show_count(self):
        messagebox.showinfo("Count", f"Jumlah item: {len(self.data)}")

    # Sorting runs
    def run_iterative(self):
        if not self.data:
            messagebox.showwarning("Warning", "Data kosong.")
            return
        arr = self.data[:]
        result, elapsed, peak_kb = measure_function(merge_sort_iterative, arr)
        self.show_result("Iteratif (Merge Sort)", arr, result, elapsed, peak_kb)

    def run_recursive(self):
        if not self.data:
            messagebox.showwarning("Warning", "Data kosong.")
            return
        arr = self.data[:]
        result, elapsed, peak_kb = measure_function(merge_sort, arr)
        self.show_result("Rekursif (Merge Sort)", arr, result, elapsed, peak_kb)

    def compare_both(self):
        if not self.data:
            messagebox.showwarning("Warning", "Data kosong.")
            return
        arr = self.data[:]
        r1, t1, m1 = measure_function(merge_sort_iterative, arr)
        r2, t2, m2 = measure_function(merge_sort, arr)

        self.txt_result.insert(tk.END, f"--- Comparison (n={len(arr)}) ---\n")
        self.txt_result.insert(tk.END, f"Iteratif (Merge Sort) -> time: {t1:.6f}s, peak mem: {m1:.2f} KB\n")
        self.txt_result.insert(tk.END, f"Result sample: {r1[:10]}\n")
        self.txt_result.insert(tk.END, f"Rekursif (Merge)      -> time: {t2:.6f}s, peak mem: {m2:.2f} KB\n")
        self.txt_result.insert(tk.END, f"Result sample: {r2[:10]}\n\n")
        self.txt_result.see(tk.END)

        # save to history (for plotting / analysis)
        history_n.append(len(arr))
        history_time_iter.append(t1)
        history_time_rec.append(t2)

    def show_result(self, method_name, original, sorted_result, elapsed, peak_kb):
        self.txt_result.insert(tk.END, f"--- {method_name} ---\n")
        self.txt_result.insert(tk.END, f"Input ({len(original)}): {original[:20]}\n")
        self.txt_result.insert(tk.END, f"Sorted ({len(sorted_result)}): {sorted_result[:50]}\n")
        self.txt_result.insert(tk.END, f"Waktu eksekusi: {elapsed:.6f} detik\n")
        self.txt_result.insert(tk.END, f"Peak memory: {peak_kb:.2f} KB\n\n")
        self.txt_result.see(tk.END)

    def export_csv(self):
        if not self.data:
            messagebox.showwarning("Warning", "Data kosong — tidak ada hasil untuk diekspor.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv"), ("All files","*.*")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nama_ruangan"])
            for it in self.data:
                writer.writerow([it])
        messagebox.showinfo("Export", f"Data disimpan ke {path}")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()
