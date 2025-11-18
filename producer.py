from confluent_kafka import Producer
import requests
import json
import time

# Konfigurasi Kafka Producer
conf = {'bootstrap.servers': "localhost:9092", 'debug': 'broker,topic,msg', 'message.timeout.ms': 30000 }
producer = Producer(conf)

# Fungsi callback untuk laporan pengiriman pesan
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# URL API
api_url = "https://ssiot.jlbsd.my.id/api/all"

# Mengirim data ke Kafka
try:
    while True:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Data dari API
            for record in data:
                producer.produce(
                    'sensor-data',  # Nama topic Kafka
                    key=record['sensor'], 
                    value=json.dumps(record), 
                    callback=delivery_report
                )
                producer.flush()  # Pastikan data dikirim
            print(f"Data sent to Kafka: {data}")
        time.sleep(1)  # Sesuai dengan interval API
except KeyboardInterrupt:
    print("Producer stopped by user")
