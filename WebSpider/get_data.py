#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:get_data.py
@author: Honour-Van: fhn037@126.com
@date:2021/04/23 09:33:16
@description:get stat data
@version:1.0
'''


from bs4 import BeautifulSoup
import requests
import parco

base_link = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/"

prov_visted = 0


def traverse(depth,  link):
    """
    docstring
    """

    def _print_leaf(leaf):
        """
        docstring
        """
        vill = parco.get_html(leaf).find_all(class_="villagetr")
        num_vill = len(vill)
        for i in range(num_vill):
            vill_info = []
            for td in vill[i]:
                vill_info.append(td.string)
            print(4*'\t'+vill_info[0]+vill_info[2]+vill_info[1])

    if depth == 4:
        _print_leaf()
    res = parco.collect(base_link + link)
    name = ""
    link = ""
    for key, val in res.items():
        if key.isdigit():
            name = key
        else:
            name += key
            print(depth * '\t' + name)
            if val != "":
                traverse(depth=depth+1, link=val)


if __name__ == "__main__":
    provs = parco.collect(base_link + "index.html")
    for prov, prov_link in provs.items():
        layer_id = prov_link[:2]
        print(layer_id.ljust(12, '0') + prov)
        traverse(1, prov_link)
