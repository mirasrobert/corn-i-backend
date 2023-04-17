from __main__ import app

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask import request, jsonify


# load the trained model
model = load_model('my_model.h5')

# define the look-back window and scaler
look_back = 1
scaler = MinMaxScaler(feature_range=(0, 1))

def make_prediction_list(data):
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

    # convert the data to a numpy array and scale it
    data = np.array(data).reshape(-1, 1)
    data = scaler.transform(data)
    
    # create a sequence of data points for the next month
    sequence = data[-look_back:].tolist()
    x = np.array(sequence).reshape(1, look_back, 1)
    y = model.predict(x)[0][0]
    
    # inverse scale the data and return the prediction
    prediction = scaler.inverse_transform([[y]])[0][0]
    return prediction



# define the endpoint for making predictions
@app.route('/multi-predict', methods=['POST'])
def predict_list():
    """
    Endpoint for making a prediction for a single data point.

    Expects a JSON payload with the following structure:
    {
        "data": [35]
    }

    Returns a JSON payload with the following structure:
    {
        "predictions": 36.123
    }

    Raises:
        ValueError: If the input data is not valid.
    """
    try:
        # get the data from the request
        data = request.get_json(force=True)['data']

        # make predictions for each data point
        predictions = []
        for d in data:
            p = make_prediction_list([d])
            predictions.append(p)

        # return the predictions as a json
        return jsonify({'predictions': predictions})
    except ValueError as e:
        # return an error message as json
        return jsonify({'error': str(e)}), 400
    except:
        return jsonify({'error': 'Invalid request. Failed to decode JSON object. Request Data is missing.'}), 400
