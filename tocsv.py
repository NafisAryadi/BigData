import sqlite3
import pandas as pd

# Buka koneksi ke database SQLite
conn = sqlite3.connect('sensor_data.db')

# Baca data dari database
query = "SELECT * FROM sensor_data"
df = pd.read_sql_query(query, conn)

# Simpan ke file CSV
df.to_csv('sensor_data.csv', index=False)
print("Data exported to sensor_data.csv")

# Tutup koneksi
conn.close()
