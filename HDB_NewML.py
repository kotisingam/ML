import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split
import math

#import xgboost as xg

hdb = pd.read_csv('hdb.csv')
hdb_df = hdb.copy()

hdb_df['remaining_lease']=99-(2021-hdb_df["lease_commence_date"])
hdb_df['floor_area']=hdb_df['floor_area_sqm'].astype(int)

all_street_model = pd.get_dummies(hdb_df['street_name'])
all_town_model = pd.get_dummies(hdb_df['town'])
all_flat_model = pd.get_dummies(hdb_df['flat_model'])
all_flat_type_model = pd.get_dummies(hdb_df['flat_type'])
all_storey_model = pd.get_dummies(hdb_df['storey_range'])

hdb_df = pd.concat((hdb_df,all_town_model,all_flat_model,all_flat_type_model,all_storey_model,all_street_model), axis=1)
hdb_clean_df=hdb_df.drop(columns=['town','month','floor_area_sqm','lease_commence_date','tyear','tmonth','tdate','flat_model','flat_type','storey_range','block','street_name'])

X = hdb_clean_df.drop('resale_price', axis=1)
Y = hdb_clean_df['resale_price']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.6, random_state=42)

import json
columns = {
    'data_columns': [col.lower() for col in X.columns]
}
with open('columns.json', 'w') as f:
    f.write(json.dumps(columns))

def RMSE(actual,predict):
    base = math.sqrt(((y_test - y_test.mean()) ** 2).mean())
    x = math.sqrt(((actual - predict) ** 2).mean())
    return x/base

knn3 = neighbors.KNeighborsRegressor(n_neighbors = 3)
knn3.fit(x_train, y_train)

pred_knn3=knn3.predict(x_test)
RMSE(y_test, pred_knn3)
knn3_score=knn3.score(x_train,y_train)

def fillin_columns(town,street_name,flat_model, floor_area_sqm, flat_type, storey_range,remaining_lease):
    stn_index = np.where(X.columns==street_name)[0][0]
    twn_index = np.where(X.columns==town)[0][0]
    flm_index = np.where(X.columns==flat_model)[0][0]
    flr_index = np.where(X.columns=='floor_area')[0][0]
    flt_index = np.where(X.columns==flat_type)[0][0]
    sra_index = np.where(X.columns==storey_range)[0][0]
    rml_index = np.where(X.columns=='remaining_lease')[0][0]
    
    x = np.zeros(len(X.columns))

    x[twn_index]=1
    x[stn_index]=1
    x[flm_index]=1
    x[flr_index]=floor_area_sqm
    x[flt_index]=1
    x[sra_index]=1
    x[rml_index]=remaining_lease

    pred_knn3 = knn3.predict([x])
    
    return f'KNN3: {pred_knn3[0]}'
fillin_columns('ANG MO KIO','ANG MO KIO AVE 6','New Generation',92,'4 ROOM','10 TO 12',57)
fillin_columns('BEDOK','BEDOK CTRL','Improved',112,'5 ROOM','13 TO 15',87)
fillin_columns('CENTRAL AREA','CANTONMENT RD','Type S2',107,'5 ROOM','46 TO 48',88)
fillin_columns('CHOA CHU KANG','TECK WHYE LANE','New Generation',92,'4 ROOM','07 TO 09',56)
fillin_columns('WOODLANDS','WOODLANDS CRES','Apartment',140,'EXECUTIVE','04 TO 06',76)

import joblib
joblib.dump(knn3,'HDB_KNN3.pkl')

