from confluent_kafka import Consumer
import sqlite3
import json

# Konfigurasi Kafka Consumer
conf = {
    'bootstrap.servers': "localhost:9092",
    'group.id': "sensor-group",
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)
consumer.subscribe(['sensor-data'])

# Koneksi ke database SQLite
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        sensor TEXT,
        value REAL,
        unit TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Membaca data dari Kafka dan menyimpan ke database
try:
    while True:
        msg = consumer.poll(1.0)  # Tunggu 1 detik untuk pesan
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        record = json.loads(msg.value().decode('utf-8'))
        cursor.execute('''
            INSERT INTO sensor_data (sensor, value, unit, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (record['sensor'], record['value'], record['unit'], record['timestamp']))
        conn.commit()
        print(f"Data inserted into database: {record}")
except KeyboardInterrupt:
    print("Consumer stopped by user")
finally:
    consumer.close()
    conn.close()
