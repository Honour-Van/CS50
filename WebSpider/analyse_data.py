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
import json


def is_prov(line: str) -> bool:
    return True if line[0] != '\t' else False


def is_base(line: str) -> bool:
    return True if (line[-4:-1]).isdigit() else False

def is_sub_base(line:str)->bool:
    return True if line[0] == '\t' and line[1] == '\t' else False 

def place_name(line: str) -> str:
    valid_char_beg = line.rfind('\t') + 1
    return line[valid_char_beg+12:-4] if is_base(line) else line[valid_char_beg+12:-1]


if __name__ == "__main__":
    dt1 = pd.DataFrame(columns=["111", "112", "121",
                                "122", "123", "210",
                                "220"])
    task1 = {}
    task2 = {"河南省": {}, "内蒙古自治区": {}}
    f = open("assets/family_name.json")
    task3 = json.load(f)
    f.close()

    prov_name = ""
    prov_cnt = False

    last_name = ""
    sub_base_flag = True
    with open("StatData.txt", encoding='utf-8') as f:
        for line in f.readlines():
            if is_prov(line):
                if task1:  # 判断词典是否为空
                    dt1 = dt1.append(pd.Series(task1, name=prov_name))
                task1 = {"111": 0, "112": 0, "121": 0,
                         "122": 0, "123": 0, "210": 0, "220": 0}
                prov_name = place_name(line)
                if prov_name == "河南省" or prov_name == "内蒙古自治区":
                    prov_cnt = True
                else:
                    prov_cnt = False
            elif is_base(line):
                task1[line[-4:-1]] = task1.get(line[-4:-1], 0) + 1
                if sub_base_flag:
                    sub_base_flag = False
                    if last_name[0] in task3:
                        task3[last_name[0]] = task3[last_name[0]] + 1
                if prov_cnt:
                    base_name = place_name(line)
                    if base_name[-3:] == "村委会":
                        for item in base_name[:-3]:
                            task2[prov_name][item] = task2[prov_name].get(
                                item, 0) + 1
                    if base_name[0] in task3:
                        task3[base_name[0]] = task3[base_name[0]] + 1
            else:
                sub_base_flag = True
            last_name = place_name(line)
            # elif is_sub_base(line):
            #     sub_base = place_name(line)
            #     if sub_base[0] in task3:
            #         task3[sub_base[0]] = task3[sub_base[0]] + 1

    if task1:  # 判断词典是否为空
        dt1 = dt1.append(pd.Series(task1, name=prov_name))
    dt1.rename(columns={"111": "主城区（111）", "112": "城乡结合区（112）", "121": "镇中心区（121）",
                        "122": "镇乡结合区（122）", "123": "特殊区域（123）", "210": "乡中心区（210）", "220": "村庄（220）"}, inplace=True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 100)  # 设置打印宽度(**重要**)
    pd.set_option('expand_frame_repr', False)  # 数据超过总宽度后，是否折叠显示

    inn_mongo = sorted(task2["内蒙古自治区"].items(),
                       key=lambda x: x[1], reverse=True)
    henan = sorted(task2["河南省"].items(), key=lambda x: x[1], reverse=True)

    # familyname = sorted(task3.items(), key=lambda x: x[1], reverse=True)
    familyname = task3.items()

    with open("ComputingData.txt", 'w', encoding='utf-8') as f:
        print("分析任务1：", file=f)
        print(dt1, file=f)

        print("\n分析任务2：", file=f)
        print("内蒙古自治区：", file=f)
        for key, value in inn_mongo[:100]:
            print(key, sep=',', end='', file=f)
        print("\n河南省：", file=f)
        for key, value in henan[:100]:
            print(key, sep=',', end='', file=f)

        print("\n\n分析任务3：", file=f)
        for key, value in familyname:
            print(key + '\t', value, sep='', file=f)
