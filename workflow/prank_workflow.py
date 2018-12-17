# -*- coding: utf-8 -*-
import time
import os
from model.prank import Graph, PersonalRank


def run():
    assert os.path.exists('D:\\recommend_data\\user\\user_follows.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if not os.path.exists('data/prank_model/prank.graph'):
        Graph.gen_graph()
        print("构建全图时间是:  %f" % (time.time() - start))
    if not os.path.exists('data/prank_model/prank_6074385586808946692.model'):
        build_start = time.time()
        PersonalRank().train(user_id=6074385586808946692)
        print("构建用户 6074385586808946692 需要时间 %s" % (time.time() - build_start))
    movies = PersonalRank().predict(user_id=6074385586808946692)
    for movie in movies:
        print(movie)
    print('Cost time: %f' % (time.time() - start))
