from get_data.bluetooth_devices import get_bluetooth_scanner
from get_data.wifi_devices import get_wifi_scanner
import pickle


def predict():
    wifi_scanner = get_wifi_scanner()
    bluetooth_scanner = get_bluetooth_scanner()

    bluetooth_devices = bluetooth_scanner.get_connected_device_and_rssi()
    wifi_devices = wifi_scanner.get_access_points()

    current_data = {**wifi_devices, **bluetooth_devices}

    with open('./detect_location/saved_model.pkl', "rb") as f:
        lp = pickle.load(f)
    return lp.predict(current_data)[0]
