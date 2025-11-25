import sqlite3
import tkinter as tk 
import tkinter.messagebox as msg

# ==== SETUP FATABASE ===
conn = conn = sqlite3.connect("data_siswa.db")
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS nilai_siswa(
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
    )
    """)
conn.commit()

root = tk.Tk()
root.title("Input Nilai Siswa")
root.geometry("350x420")

judul = tk.Label(root, text="Forum Input")
judul.pack(side="top")


label_nama = tk.Label(root, text="Nama siswa")
label_nama.pack()
ne = tk.Entry()
ne.pack(pady=3)

label_bio = tk.Label(root, text="Nilai Biologi")
label_bio.pack()
be = tk.Entry(root)
be.pack(pady=3)

label_fis = tk.Label(root, text="Nilai Fisika")
label_fis.pack()
fe = tk.Entry(root)
fe.pack(pady=3)

label_ing = tk.Label(root, text="Nilai Bahasa Inggris")
label_ing.pack()
ie = tk.Entry(root,)
ie.pack(pady=3)

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

    
    conn.execute("INSERT INTO nilai_siswa VALUES (?, ?, ?, ?, ?)",
              (nama, bio, fis, ing, prediksi))
    conn.commit()

    msg.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {prediksi}")

submit_btn = tk.Button(root, text="Submit Nilai", command=Prediksi)
submit_btn.pack(pady=10)

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
        e_nama = tk.Entry(frm, width=40)
        e_nama.grid(row=0, column=1, pady=6)
        e_nama.insert(0, nama)

        tk.Label(frm, text='Biologi:').grid(row=1, column=0, sticky='w')
        e_bio = tk.Entry(frm, width=12)
        e_bio.grid(row=1, column=1, sticky='w', pady=6)
        e_bio.insert(0, bio)

    import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ───────────────────────────
#  KONEKSI DATABASE
# ───────────────────────────
def koneksi():
    return sqlite3.connect("prediksi.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            bio INTEGER,
            fis INTEGER,
            ing INTEGER,
            prediksi TEXT
        )
    """)
    con.commit()
    con.close()


# ───────────────────────────
#  FUNGSI PREDIKSI PRODI
# ───────────────────────────
def prediksi_prodi(bio, fis, ing):
    nilai = {
        "Kedokteran": bio,
        "Teknik": fis,
        "Bahasa": ing
    }
    return max(nilai, key=nilai.get)  # pilih berdasarkan nilai tertinggi


# ───────────────────────────
#  FUNGSI CRUD
# ───────────────────────────
def insert_data():
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    hasil = prediksi_prodi(bio, fis, ing)

    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO students (nama, bio, fis, ing, prediksi) VALUES (?, ?, ?, ?, ?)",
                (nama, bio, fis, ing, hasil))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", f"Data berhasil ditambahkan\nPrediksi: {hasil}")


def update_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data di tabel!")
        return

    values = tree.item(selected, "values")
    id_data = values[0]

    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    hasil = prediksi_prodi(bio, fis, ing)

    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE students 
        SET nama=?, bio=?, fis=?, ing=?, prediksi=? 
        WHERE id=?
    """, (nama, bio, fis, ing, hasil, id_data))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", "Data berhasil diupdate")


def delete_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return

    values = tree.item(selected, "values")
    id_data = values[0]

    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id_data,))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", "Data berhasil dihapus")


# ───────────────────────────
#  LOAD DATA KE TREEVIEW
# ───────────────────────────
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    con.close()


# ───────────────────────────
#  AMBIL DATA SAAT DIKLIK
# ───────────────────────────
def pilih_data(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, values[1])

    entry_bio.delete(0, tk.END)
    entry_bio.insert(0, values[2])

    entry_fis.delete(0, tk.END)
    entry_fis.insert(0, values[3])

    entry_ing.delete(0, tk.END)
    entry_ing.insert(0, values[4])


# ───────────────────────────
#  GUI TKINTER
# ───────────────────────────
root = tk.Tk()
root.title("Prediksi Prodi")

create_table()

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nama").grid(row=0, column=0)
tk.Label(frame, text="Biologi").grid(row=1, column=0)
tk.Label(frame, text="Fisika").grid(row=2, column=0)
tk.Label(frame, text="Inggris").grid(row=3, column=0)

entry_nama = tk.Entry(frame)
entry_bio = tk.Entry(frame)
entry_fis = tk.Entry(frame)
entry_ing = tk.Entry(frame)

entry_nama.grid(row=0, column=1)
entry_bio.grid(row=1, column=1)
entry_fis.grid(row=2, column=1)
entry_ing.grid(row=3, column=1)

# Tombol
tk.Button(root, text="Submit Nilai", command=insert_data).pack(pady=3)
tk.Button(root, text="Update Data", command=update_data).pack(pady=3)
tk.Button(root, text="Delete Data", command=delete_data).pack(pady=3)

# Tabel
tree = ttk.Treeview(root, columns=("id", "nama", "bio", "fis", "ing", "prediksi"), show="headings")
for col in ("id", "nama", "bio", "fis", "ing", "prediksi"):
    tree.heading(col, text=col)
tree.pack(pady=10)

# Binding klik baris
tree.bind("<ButtonRelease-1>", pilih_data)

load_data()
root.mainloop()import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ───────────────────────────
#  KONEKSI + TABEL
# ───────────────────────────
def koneksi():
    return sqlite3.connect("prediksi.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            bio INTEGER,
            fis INTEGER,
            ing INTEGER,
            prediksi TEXT
        )
    """)
    con.commit()
    con.close()


# ───────────────────────────
#  PREDIKSI
# ───────────────────────────
def prediksi_prodi(bio, fis, ing):
    nilai = {
        "Kedokteran": bio,
        "Teknik": fis,
        "Bahasa": ing
    }
    return max(nilai, key=nilai.get)


# ───────────────────────────
#  INSERT
# ───────────────────────────
def insert_data():
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    hasil = prediksi_prodi(bio, fis, ing)

    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO students (nama, bio, fis, ing, prediksi) VALUES (?, ?, ?, ?, ?)",
                (nama, bio, fis, ing, hasil))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", f"Data berhasil ditambahkan\nPrediksi: {hasil}")


# ───────────────────────────
#  UPDATE
# ───────────────────────────
def update_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data di tabel!")
        return

    values = tree.item(selected, "values")
    id_data = values[0]  # penting!

    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    hasil = prediksi_prodi(bio, fis, ing)

    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE students 
        SET nama=?, bio=?, fis=?, ing=?, prediksi=? 
        WHERE id=?
    """, (nama, bio, fis, ing, hasil, id_data))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", "Data berhasil diupdate")


# ───────────────────────────
#  DELETE
# ───────────────────────────
def delete_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return

    values = tree.item(selected, "values")
    id_data = values[0]

    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id_data,))
    con.commit()
    con.close()

    load_data()
    messagebox.showinfo("Sukses", "Data berhasil dihapus")


# ───────────────────────────
#  LOAD DATA KE TABLE
# ───────────────────────────
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    con.close()


# ───────────────────────────
#  PILIH DATA UNTUK EDIT
# ───────────────────────────
def pilih_data(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, values[1])

    entry_bio.delete(0, tk.END)
    entry_bio.insert(0, values[2])

    entry_fis.delete(0, tk.END)
    entry_fis.insert(0, values[3])

    entry_ing.delete(0, tk.END)
    entry_ing.insert(0, values[4])
