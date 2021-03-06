#!/usr/bin/env python
# coding:utf-8


"""
择排序：
    对于一个有n个数的数列，
    第一次我们从第一个数开始选出所有数中最小的，和第一个数交换数值，这样保证第一个数是最小的
    第二次我们从第二个数开始选出第一个数之后最小的数和第二个数交换数值，这样前两个数都在正确位置
    。。。
    最后一次 我们拿倒数第二个数跟最后一个数比较，把小的放在前面
    第一次我们从第1个数开始一直到最后找最小的数
    第二次我们从第2个数开始到最后找最小的数
    。。。
    第i次我们从第i个数开始向后找最小的数
    最优时间复杂度:O(n^2)
    最坏时间复杂度:O(n^2)
    稳定性：不稳定的排序      例如： 5 8 5 2   第一趟排序5和2互换，那么两个5顺序就改变了
"""


def select_sort(li):
    n = len(li)  # li列表中有n个数，下标从0到n-1
    # i从0到n-1 ，我们每次拿下标为i的数跟后面数比较 标记最小的数
    for i in range(n):
        temp = i  # 用temp做临时标记，没遇见比下标temp更小的数，就用temp标记更小的数的下表
        # 从temp开始向后找到最后 找最小的数
        for j in range(temp, n):
            # 如果我们遇到比temp标记的数更小的，tamp就标记更小的数的下标
            if li[temp] > li[j]:
                li[temp], li[j] = li[j], li[temp]
        # 这次for循环之后 temp一定标记了i之后的最小的数的下标，我们把最小的数和i位置进行呼唤
        li[i], li[temp] = li[temp], li[i]


if __name__ == '__main__':
    li = [5, 4, 3, 2, 1]
    select_sort(li)
    print(li
)