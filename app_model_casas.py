from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
import pandas as pd
import sqlite3


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a nuestra API de casas"

#1
@app.route('/predict', methods=['GET'])
def predict():
    
    model = pickle.load(open('./models/model.pkl','rb'))

    surface = request.args.get('surface', None)
    bedrooms = request.args.get('bedrooms', None)
    restrooms = request.args.get('restrooms', None)
    # Planta = request.args.get('Planta', None)
    # Ascensor = request.args.get('Ascensor', None)
    # Terraza = request.args.get('Terraza', None)
    # Balcón = request.args.get('Balcón', None)
    # Parking = request.args.get('Parking', None)
    # location = request.args.get('location', None)

    # dict = {'surface': surface, 'bedrooms': bedrooms, 'restrooms': restrooms, 'Planta': Planta, 'Ascensor': Ascensor,
    #         'Terraza': Terraza, 'Balcón': Balcón, 'Parking': Parking, 'location': location}
    # dict = {'surface': surface, 'bedrooms': bedrooms, 'restrooms': restrooms}
    # df = pd.DataFrame.from_dict(dict)
    # df_dummies = pd.get_dummies(df['location_name'], prefix='location')
    # df_dummies = df_dummies.astype(bool).astype(int)
    # df = pd.concat([df, df_dummies], axis=1)
    #X = pd.DataFrame(data= [int(surface), int(bedrooms), int(restrooms)], columns= ['surface', 'bedrooms', 'restrooms'])

    # prediction = model.predict(X)
    # return "El precio predicho para esa vivienda es: " + str(round(prediction[0],2)) + '€'
    return 'hello kitty'
    

# app.run()

#2
@app.route("/v2/insert_data", methods=['POST'])
def insert_data():
    
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get('sales', None)

    if tv is None or radio is None or newspaper is None or sales is None:
        return "Missing args, the input values are needed."
    else:
        connection = sqlite3.connect('./data/advertising.db')
        cursor = connection.cursor()
        update_db = "INSERT INTO campañas (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?)"
        cursor.execute(update_db, (tv, radio, newspaper, sales,))
        connection.commit()
        connection.close()
        
        return 'Database updated succesfully'

# app.run()


#3
@app.route('/v2/retrain', methods=['PUT'])
def retrain():
    model = pickle.load(open('./data/advertising_model','rb'))
    
    connection = sqlite3.connect('./data/advertising.db')
    cursor = connection.cursor()
    
    query_all = '''SELECT * FROM campañas'''
    
    df = pd.DataFrame(data= cursor.execute(query_all).fetchall(), columns= ['TV', 'radio', 'newspaper', 'sales'])
    
    connection.close()
    
    X = df.drop(columns= 'sales')
    Y = df['sales']
    
    mae1 = mean_absolute_error(model.predict(X), Y)
    
    model.fit(X, Y)
    
    mae2 = mean_absolute_error(model.predict(X), Y)
    
    if mae1 <= mae2:
        return 'No changes made'
    else:
        pickle.dump(model, open('./data/advertising_model', 'wb'))
        return 'Model retrained and saved'


app.run()