import os
from get_data.utils import ensure_data_path
import json


def get_train_data(folder=None):
    if folder is None:
        folder = ensure_data_path()
    X = []
    y = []
    for fname in os.listdir(folder):
        if fname.endswith(".txt"):
            data = []
            with open(os.path.join(folder, fname)) as f:
                for line in f:
                    data.append(json.loads(line))
            X.extend(data)
            y.extend([fname.rstrip(".txt")] * len(data))
    return X, y

def main():
    get_train_data()

if __name__ == '__main__':
    main()