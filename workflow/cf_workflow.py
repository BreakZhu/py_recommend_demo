# -*- coding: utf-8 -*-
import time
import os
from model.cf import UserCf


def run(uid):
    assert os.path.exists('data/user/user_follows.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    movies = UserCf().calculate(uid)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))
