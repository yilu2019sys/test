# # summarize the tree age (1,2,3,4,5) according to the adm_id
import copy
import json
import os
import pprint
import re
import sys
from w_pts_json import save_json

script_path = os.path.abspath(__file__)
package_path = re.findall(".*/waterwheel", script_path)[0]
sys.path.append(os.path.dirname(package_path))
HOME_DIR = os.path.expanduser("~")
printer = pprint.PrettyPrinter(indent=3)

from waterwheel.python_tools.vividict import Vividict

def age_info_adm(age_info: dict):
    sum_info = {}
    adm_list = []
    for key, value in age_info.items():
        adm_id = age_info[key]['adm_id']
        tmp = age_info[key]["age of tree"]
        if adm_id not in adm_list:
            adm_list.append(adm_id)
        else:
            pass
        sum_info.setdefault(adm_id[0][0], []).append(tmp)  # #
#     return sum_info


# def summary_info(sum_info: dict):
    summary = Vividict()
    for k, v in sum_info.items():
        adm = k
        num_pts = len(v)
        no_age1 = 0
        no_age2 = 0
        no_age3 = 0
        no_age4 = 0
        no_age5 = 0
        no_age6 = 0
        for i in range(num_pts):
            if v[i][0] == 5:
                no_age5 += 1
            elif v[i][0] == 4:
                no_age4 += 1
            elif v[i][0] == 3:
                no_age3 += 1
            elif v[i][0] == 2:
                no_age2 += 1
            elif v[i][0] == 1:
                no_age1 += 1
        
        summary[adm]['ratio_age1'] = format(no_age1/num_pts, '0.5f')
        summary[adm]['ratio_age2'] = format(no_age2/num_pts, '0.5f')
        summary[adm]['ratio_age3'] = format(no_age3/num_pts, '0.5f')
        summary[adm]['ratio_age4'] = format(no_age4/num_pts, '0.5f')
        summary[adm]['ratio_age5'] = format(no_age5/num_pts, '0.5f')
        summary[adm]['total points'' number'] = num_pts

    return summary


if __name__ == "__main__":
    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all_ly.ndvi-bp.json" 
    with open(json_path) as ff:  # load the json file  /home/tq/yee19/test
        age_info = json.load(ff)
    result = age_info_adm(age_info)
    out_name = json_path.replace(".json", ".tree_age_summary.json")
    # result = summary_info(sum_info)
    save_json(out_name, result)
    print('f')
  
