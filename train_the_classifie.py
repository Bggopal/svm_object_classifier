import numpy as np
import glob
from os.path import basename
from sklearn.ensemble import RandomForestClassifier
from micromlgen import port

def load_features(folder):
    dataset = None
    classmap = {}

    for class_idx, filename in enumerate(glob.glob('%s/*.csv' % folder)):
        print("in for loop")
        class_name = basename(filename)[:-4]
        classmap[class_idx] = class_name
        samples = np.loadtxt(filename, dtype=float, delimiter=',')
        labels = np.ones((len(samples), 1)) * class_idx
        samples = np.hstack((samples, labels))
        dataset = samples if dataset is None else np.vstack((dataset, samples))
    return dataset, classmap

def get_classifier(features):
    X, y = features[:, :-1], features[:, -1]

    return RandomForestClassifier(20, max_depth=10).fit(X, y)



if __name__ == '__main__':
    features, classmap = load_features('/dataset')
    classifier = get_classifier(features)
    c_code = port(classifier, classmap=classmap)
    print(c_code)
