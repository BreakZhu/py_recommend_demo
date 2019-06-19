# -*- coding: utf-8 -*-
import time
import os
from model.lfm import LFM, Corpus


def run():
    assert os.path.exists('data/user/user_follows.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if not os.path.exists('data/lfm_model/lfm_items.dict'):
        Corpus.pre_process()
    if not os.path.exists('data/lfm_model/lfm.model'):
        LFM().train()
    uids = [2005098, 6083125955935600644, 6099765861231362052]
    lfm = LFM()
    for uid in uids:
        movies = lfm.predict(user_id=uid)
        for movie in movies:
            print(movie)
        print('Cost time: %f' % (time.time() - start))
