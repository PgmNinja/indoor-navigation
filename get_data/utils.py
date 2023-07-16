import os
import json

ALLOWED_BSSID = ['BC:62:D2:48:94:F0']

def ensure_str(output):
    try:
        output = output.decode("utf8",errors='ignore')
    except UnicodeDecodeError:
        output = output.decode("utf16",errors='ignore')
    except AttributeError:
        pass
    return output


def split_escaped(string, separator):
    """Split a string on separator, ignoring ones escaped by backslashes."""

    result = []
    current = ''
    escaped = False
    for char in string:
        if not escaped:
            if char == '\\':
                escaped = True
                continue
            elif char == separator:
                result.append(current)
                current = ''
                continue
        escaped = False
        current += char
    result.append(current)
    return result


def access_pts_to_dict(access_points, device_type):
    if device_type == 'wifi':
        return {ap['ssid'] + " " + ap['bssid']: ap['quality'] for ap in access_points if ap['bssid'] in ALLOWED_BSSID}
    elif device_type == 'ble':
        return {ap['name'] + " " + ap['address']: ap['rssi'] for ap in access_points}


def write_data(label_path, data):
    with open(label_path, "a") as f:
        f.write(json.dumps(data))
        f.write("\n")


def get_data_path(path=None):
    if path is None:
        path = os.path.join('./', "locations")
    return os.path.expanduser(path)

def ensure_data_path():
    path = get_data_path()
    if not os.path.exists(path):  # pragma: no cover
        os.makedirs(path)
    return path


def get_label_file(path, label):
    return os.path.join(get_data_path(path), label)