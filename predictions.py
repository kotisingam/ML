import pickle
import json
import numpy as np
import joblib
__model =None

def knn_predictions(town,street_name,flat_model, floor_area_sqm, flat_type, storey_range,remaining_lease):
    print('in knn_predictions')
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[:]
    #print(__locations)
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

    with open('hdb_knn3.pkl', 'rb') as f:
        __model = joblib.load(f)
        print("Loading saved artifacts...done")
    result =__model.predict([x])
    return round(result[0],2)