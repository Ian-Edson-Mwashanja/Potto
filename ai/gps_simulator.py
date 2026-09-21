import random
import time
from datetime import datetime
# Starting GPS position
latitude = -18.1234
longitude = 31.0567
# Generate a simulated GPS location
def generate_gps_location():
    global latitude
    global longitude
    # Simulate the vehicle moving
    latitude += random.uniform(-0.0001, 0.0001)
    longitude += random.uniform(-0.0001, 0.0001)
    return latitude, longitude
# Test the GPS simulator
print("       POTTO GPS SIMULATOR")
print("Starting GPS simulation...\n")
try:
    while True:
        lat, lon = generate_gps_location()
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        print(
            f"Latitude: {lat:.6f} | "
            f"Longitude: {lon:.6f} | "
            f"Time: {timestamp}"
        )
        time.sleep(1)
except KeyboardInterrupt:
    print("\nGPS simulation stopped.")