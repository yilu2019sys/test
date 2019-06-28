import os
import sys
import re
import pprint
import json, copy
from w_pts_json import save_json

def merge_dicts(d1, d2, d3, d4, d5, d6, d7, d8, d9 ,d10, d11,d12 ,d13): ## when the keys are different
    dic_merge = d1.copy()
    dic_merge.update(d2)
    dic_merge.update(d3)
    dic_merge.update(d4)
    dic_merge.update(d5)
    dic_merge.update(d6)
    dic_merge.update(d7)
    dic_merge.update(d8)
    dic_merge.update(d9)
    dic_merge.update(d10)
    dic_merge.update(d11)
    dic_merge.update(d12)
    dic_merge.update(d13)

    return dic_merge



if __name__== "__main__":

    json_path = '/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.1.json'
    with open(json_path) as ff:  # load the json file
        d1 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.2.json"
    with open(json_path) as ff:  # load the json file
        d2 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.3.json"
    with open(json_path) as ff:  # load the json file
        d3 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.4.json"
    with open(json_path) as ff:  # load the json file
        d4 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.5.json"
    with open(json_path) as ff:  # load the json file
        d5 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.6.json"
    with open(json_path) as ff:  # load the json file
        d6 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.7.json"
    with open(json_path) as ff:  # load the json file
        d7 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.8.json"
    with open(json_path) as ff:  # load the json file
        d8 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.9.json"
    with open(json_path) as ff:  # load the json file
        d9 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.10.json"
    with open(json_path) as ff:  # load the json file
        d10 = json.load(ff)

    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.11.json"
    with open(json_path) as ff:  # load the json file
        d11 = json.load(ff)


    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.12.json"
    with open(json_path) as ff:  # load the json file
        d12 = json.load(ff)
        
    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.ndvi-bp-rm_tree.13.json"
    with open(json_path) as ff:  # load the json file
        d13 = json.load(ff)

    dic_merge = merge_dicts(d1, d2, d3, d4, d5, d6, d7, d8, d9 ,d10, d11,d12 ,d13)
    out_name4 = json_path.replace("all.ndvi-bp.ndvi-bp-rm_tree.13.json", "all_ly.json")
    save_json(out_name4, dic_merge)
    print('f')



