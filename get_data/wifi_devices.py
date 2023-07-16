# https://github.com/kootenpv/access_points/tree/f3272c5ec3326143a0170f2355e83575cd3f3437

import platform
import subprocess

from .utils import ensure_str, split_escaped, access_pts_to_dict



class AccessPoint(dict):

    def __init__(self, ssid, bssid, quality, security):
        dict.__init__(self, ssid=ssid, bssid=bssid, quality=quality, security=security)

    def __getattr__(self, attr):
        return self.get(attr)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __repr__(self):
        args = ", ".join([f"{k}={v}" for k, v in self.items()])
        return f"AccessPoint({args})"


class WifiScanner(object):

    def __init__(self, device=""):
        self.device = device
        self.cmd = self.get_cmd()

    def get_cmd(self):
        raise NotImplementedError

    def parse_output(self, output):
        raise NotImplementedError

    def get_access_points(self):
        out = self.call_subprocess(self.cmd)
        results = self.parse_output(ensure_str(out))
        return access_pts_to_dict(results, 'wifi')

    @staticmethod
    def call_subprocess(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, _) = proc.communicate()
        return out


class DataFromWifiScanner(WifiScanner):

    def get_cmd(self):
        return "nmcli -t -f ssid,bssid,signal,security device wifi list"

    def parse_output(self, output):
        results = []

        for line in output.strip().split('\n'):
            try:
                ssid, bssid, quality, security = split_escaped(line, ':')
            except ValueError:
                continue
            access_point = AccessPoint(ssid, bssid, int(quality), security)
            results.append(access_point)

        return results


def get_wifi_scanner(device=""):
    operating_system = platform.system()
    if operating_system == 'Linux':
        return DataFromWifiScanner(device)
    else:
        'Do something else'



