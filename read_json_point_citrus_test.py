from pprint import pprint
import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates


# def print_k(pts, i=0):  # # read the dict content
#     for k in pts:
#         print('---'*i, k, sep='')
#         if isinstance(pts[k], dict):
#             print_k(pts[k], i+1)


def find_ndvi(pts):      # # return points' coordinate and  dates and ndvi value
    result = {}
    for key, value in pts.items():
        for k, v in value.items():
            if "ndvi" in k:
                result.setdefault(key, []).append(v)
    return result


def figure_curve(pts: dict):

    result = find_ndvi(pts)
    plt.xlabel('dates')
    plt.ylabel('ndvi')
    coresult = []
    klabel = []
    
    for k, v in result.items():
        v = sorted(v[0])      # sorted by date
        result_x = [tmp[0] for tmp in v]  # date
        result_y = [tmp[1] for tmp in v]  # ndvi

        dates = result_x
        ndvi = result_y
        dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates]

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(pd.date_range('2014-01-01', '2018-12-31', freq='120d'))
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        colabel, = plt.plot(dates, ndvi)
        coresult.append(colabel)
        klabel.append(k)

#
    plt.legend(handles=coresult, labels=klabel, loc='best')
    
    # plt.show()
    # plt.close()
    # return fig




if __name__ == "__main__":

    with open('/home/tq/yee19/test/test1.json') as ff:  # load the json file
        pts = json.load(ff)

    # pprint(pts)
    # print_k(pts)
    fig = plt.figure(num='none', figsize=(20, 10))
    result_ndvi = find_ndvi(pts)

    figure_curve(pts)
    plt.show()

