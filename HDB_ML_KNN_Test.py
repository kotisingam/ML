import pandas as pd
import joblib
import numpy as np

df1 = pd.read_csv('5 test flats.csv')

df1['remaining_lease']=99-(2021-df1["lease_commence_date"])
df1['floor_area']=df1['floor_area_sqm'].astype(int)
df1.drop(columns=["month","block","lease_commence_date"],inplace=True)

def knn_predictions(town,street_name,flat_model, floor_area_sqm, flat_type, storey_range,remaining_lease):
    import json
    global __data_columns
    global __locations
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[:]
    x = np.zeros(len(__locations))
    stn_index =__locations.index(street_name.lower())
    twn_index =__locations.index(town.lower())
    flm_index =__locations.index(flat_model.lower())
    flr_index =__data_columns.index('floor_area')
    flt_index =__locations.index(flat_type.lower())
    sra_index =__locations.index(storey_range.lower())
    rml_index =__data_columns.index('remaining_lease')
    
    x[twn_index]=1
    x[stn_index]=1
    x[flm_index]=1
    x[flr_index]=floor_area_sqm
    x[flt_index]=1
    x[sra_index]=1
    x[rml_index]=remaining_lease
    columns = {
        'data_columns': [col for col in x]
    }
    with open('columns.json', 'w') as f:
        f.write(json.dumps(columns))
        
    knn3=joblib.load('HDB_KNN3.pkl')
    result = knn3.predict([x])
    
    return result

