#!/usr/bin/python
import random


def loadfmap(fname):
    fmap = {}
    nmap = {}
    for l in open(fname):
        # 空格切分数据
        arr = l.split()
        if arr[0].find('.') != -1:  # 通过idx 表示特征下标
            idx = int(arr[0].strip('.'))
            assert idx not in fmap
            fmap[idx] = {}
            ftype = arr[1].strip(':')  # 切分类别
            content = arr[2]  # 内容
        else:
            content = arr[0]
        # 切分内容
        for it in content.split(','):
            if it.strip() == '':
                continue
            k, v = it.split('=')
            fmap[idx][v] = len(nmap)
            nmap[len(nmap)] = ftype + '=' + k
    return fmap, nmap


def write_nmap(fo, nmap):
    for i in range(len(nmap)):
        fo.write('%d\t%s\ti\n' % (i, nmap[i]))


# start here
fmap, nmap = loadfmap('agaricus-lepiota.fmap')
fo = open('featmap.txt', 'w')
write_nmap(fo, nmap)
fo.close()
fo = open('agaricus.txt', 'w')
for l in open('agaricus-lepiota.data'):
    arr = l.split(',')
    if arr[0] == 'p':
        fo.write('1')
    else:
        assert arr[0] == 'e'
        fo.write('0')
    for i in range(1, len(arr)):
        fo.write(' %d:1' % fmap[i][arr[i].strip()])
    fo.write('\n')
fo.close()

# 拆分测试集 训练集
fi = open('agaricus.txt', 'r')
ftr = open('agaricus.txt.train', 'w')
fte = open('agaricus.txt.test', 'w')
for l in fi:
    if random.randint(1, 5) == 1:
        fte.write(l)
    else:
        ftr.write(l)
fi.close()
ftr.close()
fte.close()
