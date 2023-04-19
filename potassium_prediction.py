from __main__ import app
#from app import app

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask import request, jsonify
from joblib import load
import traceback


import os

# Get the path to the current file
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define the path to the trained model
model_path = os.path.join(base_dir, 'models', 'model_K.h5')

# load the trained model
TRAINED_MODEL_K = load_model(model_path)

# define the look-back window and scaler
look_back = 1

# Define the path to the scaler object
scaler_path = os.path.join(base_dir, 'scaler', 'scaler_K.joblib')

# Load the scaler object from the file
scaler = load(scaler_path)


def make_prediction_potassium(data):
    """
    Make a prediction for a single data point using the loaded model.

    Args:
        data (list): A list of numerical values representing the input data point.

    Returns:
        float: The predicted value for the input data point.

    Raises:
        ValueError: If the input data is not valid.
    """

    # check if data is valid
    if not isinstance(data, list):
        raise ValueError("Data must be a list.")
    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Data must contain only numbers.")
    if len(data) < look_back:
        raise ValueError(f"Data must contain at least {look_back} values.")

	# prepare new data for prediction
    new_data = np.array([data]) # replace with your own new data
    new_data = scaler.transform(new_data)
    new_data = np.reshape(new_data, (1, 1, 1)) # reshape input to be [samples, time steps, features]

    # generate predictions for new data
    predictions = TRAINED_MODEL_K.predict(new_data)

    # convert predictions back to original scale
    predictions = scaler.inverse_transform(predictions)
    return predictions[0][0] # returns [[63.44638]]
 

# define the endpoint for making predictions
@app.route('/predict/potassium', methods=['POST'])
def predict_K():
    """
    Endpoint for making a prediction for a single data point.

    Expects a JSON payload with the following structure:
    {
        "data": [69]
    }

    Returns a JSON payload with the following structure:
    {
        "predictions": "64.92"
    }

    Raises:
        ValueError: If the input data is not valid.
    """
    try:
        # get the data from the request
        data = request.get_json(force=True)['data']
        
        pred_result = make_prediction_potassium(data)

        # return the predictions as a json
        return jsonify({'predictions': str(pred_result)})
    except ValueError as e:
        # return an error message as json
        return jsonify({'error': str(e)}), 400
    except:
        return jsonify({'error': traceback.format_exc()}), 500
