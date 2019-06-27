import os
import sys
import re
import pprint
import json, copy
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
from deltadate_to_int import caltime
from w_pts_json import save_json
from age_of_tree import age_of_tree
from Summary_citrus_age import age_info_adm


script_path = os.path.abspath(__file__)
package_path = re.findall(".*/waterwheel", script_path)[0]
sys.path.append(os.path.dirname(package_path))
HOME_DIR = os.path.expanduser("~")
printer = pprint.PrettyPrinter(indent=3)

from waterwheel.python_tools.vividict import Vividict


def abnormpt(pts: dict, *, selected=[0]):
    result_ab = Vividict()
    selected_result = {}
    time_n=0
    sum_none=0
    coresult = []
    klabel = []
    for key, value in pts.items():
        ndvilist = pts[key]['LC08_ndvi']
        adm = pts[key]['adm_id']

        ndvilist = sorted(ndvilist)      # sorted by date
        result_x = [tmp[0] for tmp in ndvilist]  # date
        result_y = [tmp[1] for tmp in ndvilist]  # ndvi
        dates0 = result_x
        ndvi0 = result_y

        dates = []
        ndvi = []

        for i in range(len(dates0)):               # # delete the snow effect in 11,12,01,02, delete allthe ndvi <0.1 pts
            if ndvi0[i] > 0.1:
                dates.append(dates0[i])
                ndvi.append(ndvi0[i])

        new_ndvi = sorted(ndvi)     # # sort ndvi
        index = []
        ab_pt_list = []
        ab_dates_list = []
        if len(ndvi) > 5:
            if new_ndvi[0] < 0.4:   #  if all the pts.ndvi>0.4 then, always tree
                for i in range(5):         # # return to the index of the minimum value of ndvi
                    for tmp in range(len(ndvi)):
                        if ndvi[tmp] == new_ndvi[i]:
                            index.append(tmp)
                index.sort()
                for ii in index:
                    if ii != 0 and ii != len(ndvi)-1:             # # add the pts into abnormal list
                        deltatime = abs(caltime(dates[ii], dates[ii-1]))
                        if (ndvi[ii+1]-ndvi[ii])/deltatime > 0 and ndvi[ii] < 0.3 and (ndvi[ii+1]-ndvi[ii])/deltatime < 0.0015:
                            ab_pt_list.append(ndvi[ii])
                            ab_dates_list.append(dates[ii])
                        elif (ndvi[ii]-ndvi[ii-1])/deltatime < - 0.004 and ndvi[ii] < 0.3 and 0 <((ndvi[ii+1]-ndvi[ii])/deltatime) < 0.0015:  #  # tree to soil
                            ab_pt_list.append(ndvi[ii])
                            ab_dates_list.append(dates[ii])



        if len(ab_dates_list):
            result_ab[key]['ndvi_breakpoint'] = [ab_dates_list[-1], ab_pt_list[-1]]
            age = age_of_tree(ab_dates_list[-1])
            result_ab[key]['age of tree'] = [age]
            result_ab[key]['adm_id'] = [adm]
            result_ab[key][ "LC08_ndvi"]= copy.deepcopy(pts[key][ "LC08_ndvi"])  ##
        else:
            result_ab[key]['ndvi_breakpoint'] = ['']
            result_ab[key]['age of tree'] = [5]
            result_ab[key]['adm_id'] = [adm]
            result_ab[key][ "LC08_ndvi"]= copy.deepcopy(pts[key][ "LC08_ndvi"])  ##
            sum_none += 1
        
        # put some points into selected result to plot figures
        if time_n in selected:
            selected_result[key] = copy.deepcopy(result_ab[key])
            selected_result[key]["ndvi"] = ndvi
            selected_result[key]["dates"] = dates
        time_n += 1   
        print(time_n)
        print(key)
        print('None_count: ', sum_none)

    return result_ab, selected_result


def plot_abnormpt(result_ab: dict):
    plt.xlabel('dates')
    plt.ylabel('ndvi')
    x = []
    y = []
    coresult=[]
    klabel=[]
    
    for k, v in result_ab.items():
        ndvi = v["ndvi"]
        dates_list = v["dates"]

        dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates_list]
        plt.xticks(pd.date_range('2014-01-01', '2018-12-31', freq='120d'))
        colabel, = plt.plot(dates, ndvi)
        coresult.append(colabel)
        klabel.append(k)
        vv = result_ab[k]['ndvi_breakpoint']
        if len(vv) > 1:
            x.append(result_ab[k]['ndvi_breakpoint'][0])
            y.append(result_ab[k]['ndvi_breakpoint'][1])
    
    x = [datetime.strptime(d, '%Y%m%d').date() for d in x]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(pd.date_range('2014-01-01', '2018-12-31', freq='120d'))
    plt.scatter(x, y, s=20, c='black', marker='o')
    plt.legend(handles=coresult, labels=klabel, loc='best')
    plt.show()


if __name__ == "__main__":
    json_path = "/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all_ly.json"  
    with open(json_path) as ff:  # load the json file
        pts = json.load(ff)

    sl_pts = list(range(50,55))
    ab_pts, s_pts = abnormpt(pts, selected=sl_pts)  # # line

    plot_abnormpt(s_pts)   # # abnormal points

    out_name = json_path.replace(".json", ".ndvi-bp.json")
    save_json(out_name, ab_pts)

    # # generate summary txt  the ratio of different ages
    with open(out_name) as ff:  # load the json file  /home/tq/yee19/test
        age_info = json.load(ff)
    
    result = age_info_adm(age_info)
    out_name2 = json_path.replace(".json", ".tree_age_summary.json")
    save_json(out_name2, result)

    print('fin')