from functools import partial
import os

import numpy as np
from sklearn.preprocessing import LabelEncoder

from .. import SDC, NuSDC, Features

data_dir = os.path.join(os.path.dirname(__file__), 'data')


################################################################################
# TODO: add *real* tests

def _check_acc(acc):
    assert acc >= .85, "accuracy is only {}".format(acc)


def test_simple():
    div_funcs = ['hellinger', 'kl', 'l2',
                 'renyi:0.7', 'renyi:0.9', 'renyi:0.99']
    Ks = [3, 8]
    for name in ['gaussian-2d-mean0-std1,2']:  # , 'gaussian-20d-mean0-std1,2']:
        feats = Features.load_from_hdf5(os.path.join(data_dir, name + '.h5'))
        le = LabelEncoder()
        y = le.fit_transform(feats.categories)

        for div_func in div_funcs:
            for K in Ks:
                for cls in [SDC, NuSDC]:
                    for wts in [None, np.random.uniform(.7, 1.3, len(feats))]:
                        clf = cls(div_func=div_func, K=K, n_proc=1)
                        acc, preds = clf.crossvalidate(
                            feats, y, sample_weight=wts, num_folds=3)
                        fn = partial(_check_acc, acc)
                        fn.description = "CV: {} - {}, K={}".format(
                            name, div_func, K)
                        yield fn



################################################################################

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('error', module='sdm')

    import nose
    nose.main()
