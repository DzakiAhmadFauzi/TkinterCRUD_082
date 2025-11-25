def koneksi():
    con = sqlite3.connect("tutorial.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

root = tk.Tk()
root.title("Input Nilai Siswa")
root.geometry("400x500")

judul = tk.Label(root, text="Forum Input Nilai Siswa", font=("Arial", 14))
judul.pack(pady=10)

label_nama = tk.Label(root, text="Nama Siswa:")
label_nama.pack()
ne = tk.Entry(root)
ne.pack(pady=3)

label_bio = tk.Label(root, text="Nilai Biologi:")
label_bio.pack()
be = tk.Entry(root)
be.pack(pady=3)

label_fis = tk.Label(root, text="Nilai Fisika:")
label_fis.pack()
fe = tk.Entry(root)
fe.pack(pady=3)

label_ing = tk.Label(root, text="Nilai Bahasa Inggris:")
label_ing.pack()
ie = tk.Entry(root)
ie.pack(pady=3)

cols = ("Nama", "Biologi", "Fisika", "Inggris", "Prediksi")
tree = ttk.Treeview(root, columns=cols, show="headings", height=8)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=70, anchor="center")
tree.pack(pady=10, fill="both", expand=True)

def baca_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    for r in cursor.fetchall():
        tree.insert("", tk.END, values=r)

def Prediksi():
    try:
        nama = ne.get()
        bio = int(be.get())
        fis = int(fe.get())
        ing = int(ie.get())
    except ValueError:
        msg.showerror("Error", "Masukkan nilai angka yang valid!")
        return
    
    if bio > fis and bio > ing:
        prediksi = "Kedokteran"
    elif fis > bio and fis > ing:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    conn.execute("INSERT INTO nilai_siswa VALUES (?, ?, ?, ?, ?, ?)", (nama, bio, fis, ing, prediksi))
    conn.commit()
    msg.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {prediksi}")

    ne.delete(0, tk.END)
    be.delete(0, tk.END)
    fe.delete(0, tk.END)
    ie.delete(0, tk.END)

    baca_data()

    submit_btn = tk.Button(root, text="Submit Nilai", command=Prediksi)
    submit_btn.pack(pady=10)

    baca_data()

    root.mainloop()

class NilaiApp:
    def edit_selected(self):
        sel = self.get_selected()
        if not sel:
            return
        record_id, nama, bio, fis, ing, prediksi = sel

        win = tk.Toplevel(self.root)
        win.title(f'Edit Entri ID {record_id}')
        win.transient(self.root)
        win.grab_set()
        win.geometry('420x220')
        tk.Label(win, text=f'Edit data ID {record_id}', style='Header.TLabel').pack(anchor='w', padx=12, pady=(8,4))

        frm = tk.Frame(win, paddning=12)
        frm.pack(fill='both', expand=True)

        tk.Label(frm, text='Nama:').grid(row=0, column=0, sticky='w')
        n_nama = tk.Entry(frm, width=40)
        n_nama.grid(row=0, column=1, pady=6)
        n_nama.insert(0, nama)

        tk.Label(frm, text='Biologi:').grid(row=1, column=0, sticky='w')
        n_bio = tk.Entry(frm, width=12)
        n_bio.grid(row=1, column=1, sticky='w', pady=6)
        n_bio.insert(0, bio)