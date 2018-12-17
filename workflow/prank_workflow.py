# -*- coding: utf-8 -*-
import time
import os
from model.prank import Graph, PersonalRank


def run(uid):
    assert os.path.exists('data/user/user_follows.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if not os.path.exists('data/prank_model/prank.graph'):
        Graph.gen_graph()
        print("构建全图时间是:  %f" % (time.time() - start))
    if not os.path.exists('data/prank_model/prank_{}.model'.format(uid)):
        build_start = time.time()
        PersonalRank().train(user_id=uid)
        print("构建用户 2073000 需要时间 %s" % (time.time() - build_start))
    movies = PersonalRank().predict(user_id=uid)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))
