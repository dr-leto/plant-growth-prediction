import adafruit_dht
import board
import csv
import time
import picamera2
import os
from libcamera import controls

data_dir = "/home/berry/Documents/project/data"
log_file = f"{data_dir}/logs.csv"
air_file = f"{data_dir}/air.csv"
image_dir = f"{data_dir}/images"
log_header = ["timestamp", "error_type", "message"]
air_header = ["timestamp", "temperature_c", "humidity"]

if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as file:
        csv.writer(file).writerow(log_header)
if not os.path.exists(air_file):
    with open(air_file, "w", newline="") as file:
        csv.writer(file).writerow(air_header)
    
dht_device = adafruit_dht.DHT11(board.D21, use_pulseio=False)
camera = picamera2.Picamera2()
config = camera.create_still_configuration()
camera.configure(config)
camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.01})

camera.start()

interval = 3600

while True:
    timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    image_path = f"{image_dir}/lattuga_{timestamp}.jpg"
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        with open(air_file, "a", newline="") as file:
            csv.writer(file).writerow([timestamp, temperature, humidity])
        with open(log_file, "a", newline="") as file:
            csv.writer(file).writerow([timestamp, "", "success"])
            
        camera.capture_file(image_path)
        time.sleep(interval)
    except RuntimeError as e:
        with open(log_file, "a", newline="") as file:
            csv.writer(file).writerow([timestamp, "runtime_error", e])
        continue
    except Exception as e:
        with open(log_file, "a", newline="") as file:
            csv.writer(file).writerow([timestamp, "exception", e])
        continue
