from flask import Flask, request, jsonify
import json
#import numpy as np
import joblib
#from flask-cors import cross_origin
import predictions
app = Flask(__name__)

#@cross_origin()

@app.route('/test', methods=['GET'])
def test():
    return 'Pinging Model Application!!'

@app.route('/get_street_names', methods=['GET'])
def get_street_names():
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[:]
        
    response = jsonify({
        'locations':__data_columns
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/get_predictions', methods=['GET','POST'])
#@cross_origin()
def get_predictions():
    print('in getParams ')
    #requested_data=request.get_json(force=True)
    #print(f'requested data: {requested_data}')
    town = request.form['town']#requested_data['town']
    street_name =  request.form['street_name']#requested_data['street_name']
    flat_model =  request.form['flat_model']#requested_data['flat_model']
    floor_area_sqm =  request.form['floor_area']#requested_data['floor_area']
    flat_type =  request.form['flat_type']#requested_data['flat_type']
    storey_range =  request.form['storey_range']#requested_data['storey_range']
    remaining_lease = request.form['remaining_lease']#requested_data['remaining_lease']
    print(f'town: {town}')
    
    #response= predictions.knn_predictions(town,street_name,flat_model, floor_area_sqm, flat_type, storey_range,remaining_lease)
    response = jsonify({
        'estimated_price': predictions.knn_predictions(town,street_name,flat_model, floor_area_sqm, flat_type, storey_range,remaining_lease)
    })
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server")
    print("Loading saved model...")
    global __data_columns
    global __locations
    global __model
    
    with open('hdb_knn3.pkl', 'rb') as f:
        __model = joblib.load(f)
        print("Loading saved artifacts...done")
    #response.headers.add('Access-Control-Allow-Origin', '*')
    app.run(debug=True, host='0.0.0.0', port=5000)
    

    


