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
base_dir_n = os.path.abspath(os.path.dirname(__file__))

# Define the path to the trained model
model_path_nitrogen = os.path.join(base_dir_n, 'models', 'model_N.h5')

# load the trained model
TRAINED_MODEL_N = load_model(model_path_nitrogen)

# define the look-back window and scaler
look_back_n = 1

# Define the path to the scaler object
scaler_path_n = os.path.join(base_dir_n, 'scaler', 'scaler_N.joblib')

# Load the scaler object from the file
scaler_nitrogen = load(scaler_path_n)


def make_prediction_nitrogen(data):
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
    if len(data) < look_back_n:
        raise ValueError(f"Data must contain at least {look_back_n} values.")

	# prepare new data for prediction
    new_data = np.array([data]) # replace with your own new data
    new_data = scaler_nitrogen.transform(new_data)
    new_data = np.reshape(new_data, (1, 1, 1)) # reshape input to be [samples, time steps, features]

    # generate predictions for new data
    predictions = TRAINED_MODEL_N.predict(new_data)

    # convert predictions back to original scale
    predictions = scaler_nitrogen.inverse_transform(predictions)
    return predictions[0][0] # returns [[63.44638]]
 

# define the endpoint for making predictions
@app.route('/predict/nitrogen', methods=['POST'])
def predict_N():
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
        
        pred_result = make_prediction_nitrogen(data)

        # return the predictions as a json
        return jsonify({'predictions': str(pred_result)})
    except ValueError as e:
        # return an error message as json
        return jsonify({'error': str(e)}), 400
    except:
        return jsonify({'error': traceback.format_exc()}), 500



## PHOSPHORUS

# Get the path to the current file
base_dir_p = os.path.abspath(os.path.dirname(__file__))

# Define the path to the trained model
model_path_phosphorus = os.path.join(base_dir_p, 'models', 'model_P.h5')

# load the trained model
TRAINED_MODEL_P = load_model(model_path_phosphorus)

# define the look-back window and scaler
look_back_p = 1

# Define the path to the scaler object
scaler_path_p = os.path.join(base_dir_p, 'scaler', 'scaler_P.joblib')

# Load the scaler object from the file
scaler_phosphorus = load(scaler_path_p)


def make_prediction_phosphorus(data):
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
    if len(data) < look_back_p:
        raise ValueError(f"Data must contain at least {look_back_p} values.")

	# prepare new data for prediction
    new_data = np.array([data]) # replace with your own new data
    new_data = scaler_phosphorus.transform(new_data)
    new_data = np.reshape(new_data, (1, 1, 1)) # reshape input to be [samples, time steps, features]

    # generate predictions for new data
    predictions = TRAINED_MODEL_P.predict(new_data)

    # convert predictions back to original scale
    predictions = scaler_phosphorus.inverse_transform(predictions)
    return predictions[0][0] # returns [[63.44638]]
 

# define the endpoint for making predictions
@app.route('/predict/phosphorus', methods=['POST'])
def predict_P():
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
        
        pred_result = make_prediction_phosphorus(data)

        # return the predictions as a json
        return jsonify({'predictions': str(pred_result)})
    except ValueError as e:
        # return an error message as json
        return jsonify({'error': str(e)}), 400
    except:
        return jsonify({'error': traceback.format_exc()}), 500





### POTASSIUM
# Get the path to the current file
base_dir_k = os.path.abspath(os.path.dirname(__file__))

# Define the path to the trained model
model_path_k = os.path.join(base_dir_k, 'models', 'model_K.h5')

# load the trained model
TRAINED_MODEL_K = load_model(model_path_k)

# define the look-back window and scaler
look_back_k = 1

# Define the path to the scaler object
scaler_path_k = os.path.join(base_dir_k, 'scaler', 'scaler_K.joblib')

# Load the scaler object from the file
scaler_k = load(scaler_path_k)


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
    if len(data) < look_back_k:
        raise ValueError(f"Data must contain at least {look_back_k} values.")

	# prepare new data for prediction
    new_data = np.array([data]) # replace with your own new data
    new_data = scaler_k.transform(new_data)
    new_data = np.reshape(new_data, (1, 1, 1)) # reshape input to be [samples, time steps, features]

    # generate predictions for new data
    predictions = TRAINED_MODEL_K.predict(new_data)

    # convert predictions back to original scale
    predictions = scaler_k.inverse_transform(predictions)
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






### PH LEVEL

# Get the path to the current file
base_dir_ph = os.path.abspath(os.path.dirname(__file__))

# Define the path to the trained model
model_path_ph = os.path.join(base_dir_ph, 'models', 'model_pH.h5')

# load the trained model
TRAINED_MODEL_PH = load_model(model_path_ph)

# define the look-back window and scaler
look_back_ph = 1

# Define the path to the scaler object
scaler_path_ph = os.path.join(base_dir_ph, 'scaler', 'scaler_pH.joblib')

# Load the scaler object from the file
scaler_ph = load(scaler_path_ph)


def make_prediction_ph(data):
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
    if len(data) < look_back_ph:
        raise ValueError(f"Data must contain at least {look_back_ph} values.")

	# prepare new data for prediction
    new_data = np.array([data]) # replace with your own new data
    new_data = scaler_ph.transform(new_data)
    new_data = np.reshape(new_data, (1, 1, 1)) # reshape input to be [samples, time steps, features]

    # generate predictions for new data
    predictions = TRAINED_MODEL_PH.predict(new_data)

    # convert predictions back to original scale
    predictions = scaler_ph.inverse_transform(predictions)
    return predictions[0][0] # returns [[63.44638]]
 

# define the endpoint for making predictions
@app.route('/predict/ph_level', methods=['POST'])
def predict_pH():
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
        
        pred_result = make_prediction_ph(data)

        # return the predictions as a json
        return jsonify({'predictions': str(pred_result)})
    except ValueError as e:
        # return an error message as json
        return jsonify({'error': str(e)}), 400
    except:
        return jsonify({'error': traceback.format_exc()}), 500
