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