#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:analyse_data.py
@author: Honour-Van: fhn037@126.com
@date:2021/04/27 15:48:18
@description:analyse the data we have gotten, with 3 tasks
@version:1.0
'''

import pandas as pd
from collections import OrderedDict


def is_prov(line: str) -> bool:
    return True if line[0] != '\t' else False


def is_base(line: str) -> bool:
    return True if (line[-4:-1]).isdigit() else False


def place_name(line: str) -> str:
    valid_char_beg = line.rfind('\t') + 1
    return line[valid_char_beg+12:-4] if is_base(line) else line[valid_char_beg+12:-1]


if __name__ == "__main__":
    dt1 = pd.DataFrame(columns=["111", "112", "121",
                                "122", "123", "210",
                                "220"])
    task1 = {}
    prov_name = ""
    with open("StatData.txt", encoding='utf-8') as f:
        for line in f.readlines():
            if is_prov(line):
                if task1:  # 判断词典是否为空
                    dt1 = dt1.append(pd.Series(task1, name=prov_name))
                task1 = {"111": 0, "112": 0, "121": 0,
                         "122": 0, "123": 0, "210": 0, "220": 0}
                prov_name = place_name(line)
            elif is_base(line):
                task1[line[-4:-1]] = task1.get(line[-4:-1], 0) + 1
        if task1:  # 判断词典是否为空
            dt1 = dt1.append(pd.Series(task1, name=prov_name))

    dt1.rename(columns={"111": "主城区（111）", "112": "城乡结合区（112）", "121": "镇中心区（121）",
                        "122": "镇乡结合区（122）", "123": "特殊区域（123）", "210": "乡中心区（210）", "220": "村庄（220）"}, inplace=True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 100)  # 设置打印宽度(**重要**)
    pd.set_option('expand_frame_repr', False)  # 数据超过总宽度后，是否折叠显示
    with open("ComputingData.txt", 'w', encoding='utf-8') as f:
        print(dt1, file=f)
