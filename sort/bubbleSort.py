#!/usr/bin/env python
# coding:utf-8
"""
冒泡排序的时间复杂度是O(N^2)
冒泡排序的思想: 每次比较两个相邻的元素, 如果他们的顺序错误就把他们交换位置
比如有五个数: 12, 35, 99, 18, 76, 从大到小排序, 对相邻的两位进行比较
第一趟:
第一次比较: 35, 12, 99, 18, 76
第二次比较: 35, 99, 12, 18, 76
第三次比较: 35, 99, 18, 12, 76
第四次比较: 35, 99, 18, 76, 12
经过第一趟比较后, 五个数中最小的数已经在最后面了, 接下来只比较前四个数, 依次类推
第二趟
99, 35, 76, 18, 12
第三趟
99, 76, 35, 18, 12
第四趟
99, 76, 35, 18, 12
比较完成
冒泡排序原理: 每一趟只能将一个数归位, 如果有n个数进行排序,只需将n-1个数归位,
 也就是说要进行n-1趟操作(已经归位的数不用再比较)
"""


def bubble_sort(numbers):
    print("原数组 :{}".format(numbers))
    for i in range(len(numbers)-1):    # 这个循环负责设置冒泡排序进行的次数
        for j in range(len(numbers)-i-1):  # ｊ为列表下标
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
        print("第 {} 次排序:{}".format(i + 1, numbers))
    return numbers

nums = [5, 2, 45, 6, 8, 2, 1]

print(bubble_sort(nums))