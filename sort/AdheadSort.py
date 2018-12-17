#!/usr/bin/env python
# coding:utf-8

from collections import deque


def swap_param(L, i, j):
    L[i], L[j] = L[j], L[i]
    return L


def heap_adjust(L, start, end):
    """
    :param L:
    :param start:
    :param end:
    :return:
    """
    temp = L[start]
    i = start
    j = 2 * i

    while j <= end:
        if (j < end) and (L[j] < L[j + 1]):
            j += 1
        if temp < L[j]:
            L[i] = L[j]
            i = j
            j = 2 * i
        else:
            break
    L[i] = temp


def heap_sort(L):
    """
    因为引入了一个辅助空间，所以使L_length = len(L) - 1
    第一个循环做的事情是把序列调整为一个大根堆(heap_adjust函数)
    第二个循环是把堆顶元素和堆末尾的元素交换(swap_param函数)，然后把剩下的元素调整为一个大根堆(heap_adjust函数)
    :param L:
    :return:
    """
    L_length = len(L) - 1
    # 有孩子的节点
    first_sort_count = L_length // 2
    for i in range(first_sort_count):
        heap_adjust(L, first_sort_count - i, L_length)

    for i in range(L_length - 1):
        L = swap_param(L, 1, L_length - i)
        heap_adjust(L, 1, L_length - i - 1)

    return [L[i] for i in range(1, len(L))]


def main():
    """
    collections库里提供了链表结构deque，我们先使用它初始化一个无序序
    :return:
    """
    L = deque([50, 16, 30, 10, 60,  90,  2, 80, 70])
    L.appendleft(0)
    print(heap_sort(L))

if __name__ == '__main__':
    main()