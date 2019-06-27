import os
import sys
import re
import pprint
import json, copy
import pandas as pd
import numpy as np

def update_excel_pd(xls_path, statlist: dict, *, crop_codes=[1]):
    """
    pandas version of excel update
    """
    
    # =============================================
    d = pd.read_excel(xls_path, sheetname=0)

    d1 = pd.DataFrame(statlist)
    d1 = d1.T
 
    d["OBJECTID_1"] = pd.to_numeric(d["OBJECTID_1"], errors="coerce")
    d1["OBJECTID_1"] = pd.to_numeric(d1["OBJECTID_1"], errors="coerce")
    d2 = pd.merge(d, d1, on="OBJECTID_1")
    d.head()

    out_path = xls_path.replace(".xls", ".stat0626.xls")
    writer = pd.ExcelWriter(out_path)
    d2.to_excel(writer, "Sheet1")
    writer.save()

if __name__ == "__main__":
    json_path = '/home/tq/data2/citrus/tree_age/samples-0626/adm-40w.bm.1-2465.all2.tree_age_summary.json'
    with open(json_path) as ff:  # load the json file
        result = json.load(ff)
    for k, v in result.items():
        result[k]['OBJECTID_1'] = int(k)
    update_excel_pd('/home/tq/data_pool/diva-gis/全国乡镇边界/test/attribute-xls/hunan.xls', result)
    print('fin')
