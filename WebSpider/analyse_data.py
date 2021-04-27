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
    """
    # is_prov
    @Description:
    a level judge function.
    to see if a line of record is referred to a province
    ---------
    @Param:
    a line of record in StatData.txt
    -------
    @Returns:
    a bool value if it's a province
    -------
    """
    return True if line[0] != '\t' else False


def is_base(line: str) -> bool:
    """
    # is_base
    @Description:
    a level judge function.
    to see if a line of record is referred to a childest node
    ---------
    @Param:
    a line of record in StatData.txt
    -------
    @Returns:
    a bool value if it's a grassroot unit
    -------
    """
    return True if (line[-4:-1]).isdigit() else False


def place_name(line: str) -> str:
    """
    # place_name
    @Description:
    extract the name of place in a line of record in StatData.txt
    ---------
    @Param:
    a line of record in StatData.txt
    -------
    @Returns:
    a Chinese word str: name of place
    -------
    """
    valid_char_beg = line.rfind('\t') + 1
    return line[valid_char_beg+12:-4] if is_base(line) else line[valid_char_beg+12:-1]


if __name__ == "__main__":
    # temporary tool-use data structures
    dt1 = pd.DataFrame(columns=["111", "112", "121",
                                "122", "123", "210",
                                "220"])
    task1 = {}
    task2 = {"河南省": {}, "内蒙古自治区": {}}
    f = open("assets/family_name.json") # the 100 family names are transferred by familyname2json.py
    task3 = json.load(f)
    f.close()

    # task2 prov_name filter tools
    prov_name = ""
    prov_cnt = False

    # task3 level filter tools: to see if it's the last but one level
    last_name = ""
    sub_base_flag = True

    with open("StatData.txt", encoding='utf-8') as f:
        for line in f.readlines():
            if is_prov(line):
                # task1 started to count kinds of different id codes
                if task1:  # to see if the dict is empty
                    dt1 = dt1.append(pd.Series(task1, name=prov_name))
                task1 = {"111": 0, "112": 0, "121": 0,
                         "122": 0, "123": 0, "210": 0, "220": 0}
                
                # task2 started to select the henan and inner mongolia
                prov_name = place_name(line)
                if prov_name == "河南省" or prov_name == "内蒙古自治区":
                    prov_cnt = True
                else:
                    prov_cnt = False
            elif is_base(line):
                # task1: in order to get the id codes of grassroot units
                task1[line[-4:-1]] = task1.get(line[-4:-1], 0) + 1

                # task2: if the current units belong to henan or inner mongolia
                if prov_cnt:
                    base_name = place_name(line)
                    if base_name[-3:] == "村委会":
                        for item in base_name[:-3]:
                            task2[prov_name][item] = task2[prov_name].get(
                                item, 0) + 1

                # task3: count the last but one levels
                if sub_base_flag:
                    sub_base_flag = False
                    if last_name[0] in task3:
                        task3[last_name[0]] = task3[last_name[0]] + 1
                # task3: count the grassroot units
                name3 = place_name(line)
                if name3[0] in task3:
                    task3[name3[0]] = task3[name3[0]] + 1
            else:
                sub_base_flag = True
            last_name = place_name(line)

    # prepare to output
    # task1
    if task1:  # to see if the dict is empty
        dt1 = dt1.append(pd.Series(task1, name=prov_name))
    dt1.rename(columns={"111": "主城区（111）", "112": "城乡结合区（112）", "121": "镇中心区（121）",
                        "122": "镇乡结合区（122）", "123": "特殊区域（123）", "210": "乡中心区（210）", "220": "村庄（220）"}, inplace=True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 100)  # set the print width of pands.DataFrame
    pd.set_option('expand_frame_repr', False)  # if the columns are too many for display

    # task2 to output
    inn_mongo = sorted(task2["内蒙古自治区"].items(),
                       key=lambda x: x[1], reverse=True)
    henan = sorted(task2["河南省"].items(), key=lambda x: x[1], reverse=True)

    # task3 to output
    # familyname = sorted(task3.items(), key=lambda x: x[1], reverse=True)
    familyname = task3.items()

    with open("ComputingData.txt", 'w', encoding='utf-8') as f:
        # task1: print to file
        print("分析任务1：", file=f)
        print(dt1, file=f)

        # task2: print to file
        print("\n分析任务2：", file=f)
        print("内蒙古自治区：", file=f)
        for key, value in inn_mongo[:100]:
            print(key, sep=',', end='', file=f)
        print("\n河南省：", file=f)
        for key, value in henan[:100]:
            print(key, sep=',', end='', file=f)

        # task3: print to file
        print("\n\n分析任务3：", file=f)
        for key, value in familyname:
            print(key + '\t', value, sep='', file=f)
