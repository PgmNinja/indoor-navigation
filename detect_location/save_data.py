
import sys
from get_data.utils import ensure_data_path, get_label_file, write_data


def learn(label, data):
    path = ensure_data_path()
    label_path = get_label_file(path, label + ".txt")
    if data:
        write_data(label_path, data)


def main():
    location = sys.argv[1]
    from get_data.bluetooth_devices import get_bluetooth_scanner
    from get_data.wifi_devices import get_wifi_scanner

    wifi_scanner = get_wifi_scanner()
    bluetooth_scanner = get_bluetooth_scanner()

    bluetooth_devices = bluetooth_scanner.get_connected_device_and_rssi()
    wifi_devices = wifi_scanner.get_access_points()

    data_to_write = {**wifi_devices, **bluetooth_devices}

    learn(location, data_to_write)



if __name__ == '__main__':
    main()
