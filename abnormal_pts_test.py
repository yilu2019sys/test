import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
from read_json_point_citrus_test import find_ndvi
from read_json_point_citrus_test import figure_curve
from deltadate_to_int import caltime
from w_pts_json import save_json


def abnormpt(pts: dict):
    result = find_ndvi(pts)
    result_ab = {}
    coresult = []
    klabel = []

    for k, v in result.items():
        v = sorted(v[0])      # sorted by date
        result_x = [tmp[0] for tmp in v]  # date
        result_y = [tmp[1] for tmp in v]  # ndvi
        dates = result_x
        ndvi = result_y

        rm_date_list = []
        rm_ndvi_list = []

        for i in range(len(dates)):               # # delete the snow effect in 11,12,01,02, delete allthe ndvi <0.1 pts
            # if dates[i].find('12', 4) == 4 or dates[i].find('11', 4) == 4 or dates[i].find('01', 4) == 4 or dates[i].find('02', 4) == 4:
            #     if ndvi[i] < 0.1:
            #         rm_date_list.append(dates[i])
            #         rm_ndvi_list.append(ndvi[i])
            if ndvi[i] < 0.1:
                rm_date_list.append(dates[i])
                rm_ndvi_list.append(ndvi[i])

        for i in rm_date_list:
            if len(rm_date_list) > 0:
                dates.remove(i)
        for j in rm_ndvi_list:
            if len(rm_ndvi_list) > 0:
                ndvi.remove(j)

        new_ndvi = sorted(ndvi)     # # sort ndvi
        index = []
        ab_pt_list = []
        ab_dates_list = []

        if new_ndvi[0] < 0.4:   #  if all the pts.ndvi>0.4 then, always tree
            for i in range(5):         # # return to the index of the minimum value of ndvi
                for tmp in range(len(ndvi)):
                    if ndvi[tmp] == new_ndvi[i]:
                        index.append(tmp)
            for ii in index:
                if ii != 0 and ii != len(ndvi)-1:             # # add the pts into abnormal list
                    deltatime = abs(caltime(dates[ii], dates[ii-1]))
                    if (ndvi[ii+1]-ndvi[ii])/deltatime > 0 and ndvi[ii] < 0.3 and (ndvi[ii+1]-ndvi[ii])/deltatime < 0.0005:
                        ab_pt_list.append(ndvi[ii])
                        ab_dates_list.append(dates[ii])
                    elif (ndvi[ii]-ndvi[ii-1])/deltatime < - 0.003 and ndvi[ii] < 0.3 and abs((ndvi[ii+1]-ndvi[ii])/deltatime) < 0.0005:  #  # tree to soil
                        ab_pt_list.append(ndvi[ii])
                        ab_dates_list.append(dates[ii])

        if len(ab_dates_list):
            result_ab.setdefault(k, []).append([ab_dates_list[-1], ab_pt_list[-1]])
        else:
            result_ab.setdefault(k, []).append('')

        plt.xlabel('dates')
        plt.ylabel('ndvi')

        dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates]
        plt.xticks(pd.date_range('2014-01-01', '2018-12-31', freq='120d'))
        colabel, = plt.plot(dates, ndvi)
        coresult.append(colabel)
        klabel.append(k)

    plt.legend(handles=coresult, labels=klabel, loc='best')
    print(result_ab)
    return result_ab


def plot_abnormpt(result_ab: dict):
    plt.xlabel('dates')
    plt.ylabel('ndvi')
    x = [value[0][0] for value in result_ab.values() if value[0] != '']
    y = [value[0][1] for value in result_ab.values() if value[0] != '']
    x = [datetime.strptime(d, '%Y%m%d').date() for d in x]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(pd.date_range('2014-01-01', '2018-12-31', freq='120d'))
    plt.scatter(x, y, s=20, c='black', marker='o')


if __name__ == "__main__":

    with open('/home/tq/yee19/test/test1.json') as ff:  # load the json file
        pts = json.load(ff)
    # # plot the abnormal points
    fig = plt.figure(num='test', figsize=(20, 10))
    fig.add_subplot(2,1,1)
    plt.title('Origin')
    figure_curve(pts)
    post = fig.add_subplot(2,1,2)
    ab_pts = abnormpt(pts)
    plt.title('Post')
    plot_abnormpt(ab_pts)
    plt.show()

    file_name = "result.json"
    save_json(file_name, ab_pts)
    print('fin')  