# using fbprophet to decompose the ndvi time series
# based on pixel level

import os
import sys
import re
import pprint
import time
import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet
from pandas import DataFrame, Series
import json, copy
from fbprophet.plot import add_changepoints_to_plot


json_path = '/home/tq/data2/citrus/tree_age/samples-0624/adm-100-ad1138.bm.1-2465.20140101-20181231.json'
with open(json_path) as ff:  # load the json file
    pts = json.load(ff)
for key, value in pts.items():
    ds=[]
    if key == '(25.590939637924237, 111.43227291222988)':
        df = pd.DataFrame(columns=["ds", "y"])
        ndvilist = pts[key]['LC08_ndvi']
        ndvilist = sorted(ndvilist)      # sorted by date
        date = [tmp[0] for tmp in ndvilist]  # date
        ndvi = [tmp[1] for tmp in ndvilist]  # ndvi
        dates = date
        y= ndvi
        for i in range(len(dates)):
            dates[i] = time.strptime(dates[i], '%Y%m%d')
            ds.append(time.strftime('%Y-%m-%d', dates[i]))

        # add data into df
        dss = Series(ds)
        df['ds'] = dss
        ys = Series(y)
        df['y'] = ys

        # threshold
        df['cap']=1
        df['floor']=0.1
        m = Prophet(growth='logistic',holidays=None,  yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False, seasonality_prior_scale=5, changepoint_prior_scale=1)
        # m = Prophet()
        m.fit(df)
        
      
        future = m.make_future_dataframe(periods=30,freq='d')
        future.tail()
        # htreshold
        future['cap']=1
        future['floor']=0.1

        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


        fig1 = m.plot(forecast)
        a = add_changepoints_to_plot(fig1.gca(), m, forecast)
        
        fig2 = m.plot_components(forecast)
        # plt.show()

