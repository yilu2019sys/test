import os
import sys
import re
import pprint
import pandas as pd
from pandas import DataFrame, Series
import json, copy
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from matplotlib import pyplot
import time
import matplotlib.pyplot as plt
from w_pts_json import save_json


def de_seasonal(pts: dict, selected=[0]):
    sum_na=0
    ttime = 0
    result_pts= {}

    for key, value in pts.items():
        ds = []
        ttime += 1

        if ttime in selected:
            print(ttime)
            if pts[key]["age of tree"] == [5]:
                df = pd.DataFrame(columns=["ds", "y"])
                ndvilist = pts[key]['LC08_ndvi']
                ndvilist = sorted(ndvilist)      # sorted by date
                date = [tmp[0] for tmp in ndvilist]  # date
                ndvi = [tmp[1] for tmp in ndvilist]  # ndvi
                dates = []
                ndvis = []
                for i in range(len(date)):               # # delete the snow effect in 11,12,01,02, delete allthe ndvi <0.1 pts
                    if ndvi[i] > 0.1:
                        dates.append(date[i])
                        ndvis.append(ndvi[i])
                for i in range(len(dates)):
                    dates[i] = time.strptime(dates[i], '%Y%m%d')
                    ds.append(time.strftime('%Y-%m-%d', dates[i]))
                y = ndvis

                # add data into df
                dss = Series(ds)
                df['ds'] = dss
                ys = Series(y)
                df['y'] = ys
                df['ds'] = pd.to_datetime(df['ds'])
        
                helper = pd.DataFrame({'ds': pd.date_range(df['ds'].min(), df['ds'].max())})
                d = pd.merge(df, helper, on='ds', how='outer').sort_values('ds')
                d['y'] = d['y'].interpolate(method='linear')
                d['y'].index = range(len(d))
                y_inp = d['y']
        
                # # series = [dss,ys]
                result = seasonal_decompose(y_inp, model='additive', freq=365)
                season_max = result.seasonal.max()
                season_min = result.seasonal.min()

                if abs(season_max-season_min) < 0.15:
                    sum_na += 1
                else:
                    result_pts[key] = copy.deepcopy(pts[key])
        
            else:
                result_pts[key] = copy.deepcopy(pts[key])

    print("NA: ", sum_na)
    return result_pts


if __name__ == "__main__":
    json_path = '/home/tq/data2/citrus/tree_age/samples-0625/adm-40w.bm.1-2465.all.ndvi-bp.json'
    with open(json_path) as ff:  # load the json file
        pts = json.load(ff)
    selected = list(range(120000, 140000))
    result = de_seasonal(pts, selected)
    out_name3 = json_path.replace(".json", ".ndvi-bp-rm_tree.13.json")
    save_json(out_name3, result)
    print('f')

