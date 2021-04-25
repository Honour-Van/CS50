#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file:parco.py
@author: Honour-Van(fhn037@126.com)
@date:2021/04/21 22:26:04
@description: link PARser&COllector, get 
@version:2.0
        expand the table collect functions
'''

import requests
from bs4 import BeautifulSoup

def get_html(url):
    """
    
    """
    while True:
        try:
            r = requests.get(url, timeout=1)
            r.encoding="gb2312"
            if r.status_code == 200:
                return BeautifulSoup(r.text.replace('<br/>', ''), "html.parser")
            else:
                continue
        except:
            continue

def collect(site_link: str) -> dict:
    """spider into a website, and traverse all the hyperlink there
    ---------
    @Param:
    site_link: string, the website hyperlink about to spider in.
    -------
    @Returns:
    a dict: links
        key:link text
        value: hyperlink
    -------
    """
    soup = get_html(site_link)

    def _tr_avail(tr_class):
        return tr_class == "provincetr" \
            or tr_class == "citytr"\
            or tr_class == "countytr"
    tag_found = soup.find_all(class_=_tr_avail)

    sub_link = {}
    for tr in tag_found:
        tdata = tr.find_all('td')
        for td in tdata:
            link = td.find('a')
            if td.string != None:
                if link != None:
                    sub_link[td.string] = link.attrs['href']
                else:
                    sub_link[td.string] = ""
    return sub_link


if __name__ == "__main__":
    base_link = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/"
    cur_link = "13/1304.html"
    print(collect(base_link + cur_link))
