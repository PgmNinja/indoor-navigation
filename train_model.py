import os
from get_data.utils import ensure_data_path
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
import pickle


def get_pipeline(clf=RandomForestClassifier(n_estimators=100, class_weight="balanced")):
    return make_pipeline(DictVectorizer(sparse=False), clf)


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


def train_model(path=None):
    X, y = get_train_data(path)
    if len(X) == 0:
        raise ValueError("No wifi access points have been found during training")
    lp = get_pipeline()
    lp.fit(X, y)
    with open('saved_model.pkl', "wb") as f:
        pickle.dump(lp, f)
    return lp

def main():
    train_model()

if __name__ == '__main__':
    main()