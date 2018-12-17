# -*- coding: utf-8 -*-
import time
import os
from model.lfm import LFM, Corpus


def run(uid):
    assert os.path.exists('data/user/user_follows.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if not os.path.exists('data/lfm_model/lfm_items.dict'):
        Corpus.pre_process()
    if not os.path.exists('data/lfm_model/lfm.model'):
        LFM().train()
    movies = LFM().predict(user_id=uid)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))
