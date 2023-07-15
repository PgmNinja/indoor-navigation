# https://github.com/IanHarvey/bluepy

import platform
import subprocess
import re
from bluepy.btle import Scanner, DefaultDelegate

from .utils import ensure_str, access_pts_to_dict





class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.connectable and dev.rssi != 0:
            print("Connected device:", dev.addr)
            print("RSSI:", dev.rssi)


scanner = Scanner().withDelegate(ScanDelegate())
all_devices = scanner.scan(10)


class BluetoothScanner(object):
    bluetoothctl = "bluetoothctl"

    def __init__(self, device=""):
        self.device = device

    def get_address_list(self, output):
        result = []
        output =  output.split('\n')
        for op in output:
            ops = op.split(' ')
            if len(ops) > 1:
                result.append(ops[1])
        return result

    def get_address_info(self, output):
        info = {}
        lines = output.strip().split('\n')
        for line in lines[1:]:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                info[key] = value
        return info

    def get_connected_devices(self):
        connected_device = []
        out = self.call_subprocess(f"{self.bluetoothctl} paired-devices")
        addr_list = self.get_address_list(ensure_str(out))
        for addr in addr_list:
            command = f"{self.bluetoothctl} info {addr}"
            info = ensure_str(self.call_subprocess(command))
            parsed_info = self.get_address_info(info)
            if parsed_info.get('Connected') == 'yes':
                parsed_info['address'] = addr
                connected_device.append(parsed_info)
        return connected_device

    def get_signal_strength(self, connected_device):
        rssi = 0
        for dev in all_devices:
            for (adtype, desc, value) in dev.getScanData():
                if desc == 'Complete Local Name' and value.split("-")[0].strip() == connected_device.strip():
                    rssi = dev.rssi
        return rssi

    def get_connected_device_and_rssi(self):
        devices_and_rssi = []
        connected_devices = self.get_connected_devices()
        for device_info in connected_devices:
            name = device_info['Name']
            rssi = self.get_signal_strength(name)
            data = {'name': name, 'address': device_info['address'], 'rssi': rssi}
            devices_and_rssi.append(data)
        return access_pts_to_dict(devices_and_rssi, 'ble')

    def call_subprocess(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, _) = proc.communicate()
        return out

def get_bluetooth_scanner(device=""):
    operating_system = platform.system()
    if operating_system == 'Linux':
        return BluetoothScanner(device)
    else:
        "Do something else"


