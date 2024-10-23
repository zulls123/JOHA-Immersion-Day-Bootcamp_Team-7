import pandas as pd
import numpy as np
from scipy.stats import chi2
import lightgbm as lgb
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit, train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pickle
import joblib
import yaml


with open('parameters.yaml', 'rt') as f:
    params = yaml.safe_load(f.read())

OPT_PARAMS = params["opt_params"]
BOUNDS = params["bounds"]
PRODUCT_SELL_PRICE = params["product_sell_prices"]
PRODUCT_DEMAND = params["product_demand"]
PRODUCT_STORAGE_COST = params["storage_costs"]
PRODUCT_DISCARD_COST = params["discard_costs"]
PRODUCT_UNMET_DEMAND_PENALTY = params["unmet_demand_penalty"]


def mahalanobis_outlier_removal(df, significance_level=0.01):
    """
    Detects and removes multivariate outliers from a DataFrame of time series signals using the Mahalanobis Distance method.

    Parameters:
    - df: pandas DataFrame containing the time series signals.
    - significance_level: The significance level for outlier detection (default is 0.01).

    Returns:
    - A DataFrame with outliers removed.
    """
    # Calculate the mean and covariance matrix of the data
    mean_vector = np.mean(df, axis=0)
    cov_matrix = np.cov(df, rowvar=False)

    # Calculate the inverse of the covariance matrix
    cov_inv = np.linalg.inv(cov_matrix)

    # Calculate the Mahalanobis distance for each data point
    mahalanobis_dist = []
    for _, row in df.iterrows():
        diff = row - mean_vector
        dist = np.sqrt(np.dot(np.dot(diff, cov_inv), diff))
        mahalanobis_dist.append(dist)

    # Calculate the Chi-Square threshold for the given significance level
    chi2_threshold = chi2.ppf(1 - significance_level, df.shape[1])

    # Identify outliers based on Mahalanobis distance and the Chi-Square threshold
    outliers = np.array(mahalanobis_dist) > np.sqrt(chi2_threshold)

    # Remove rows corresponding to outliers
    cleaned_df = df[~outliers]

    return cleaned_df

def modelperf(y_pred,y_test):
    mse = mean_squared_error(y_test,y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score( y_test,y_pred)

    # Calculate Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((y_test-y_pred) / y_pred)) * 100
    rmse = np.sqrt(mse)

    return {"MSE": mse,
            "MAE": mae,
            "R2": r2,
            "MAPE": mape,
            "RMSE": rmse}

def train_model(df, input_vars, output_vars, model_name, random_seed=20, model_type="Linear", save_model=False):   
    cleanX = df[input_vars] 
    cleany = df[output_vars]

    if model_type == "Linear":
        model = LinearRegression()
        model.fit(cleanX, cleany)
    elif model_type == "Non-Linear":
        model = lgb.LGBMRegressor(random_state=random_seed,verbose=0)
        model.fit(cleanX, cleany)
    
    if save_model:
        with open("unit_models/{}.pkl".format(model_name), 'wb') as f:
            pickle.dump(model, f)
        joblib.dump(model, "unit_models/{}.joblib".format(model_name))
    
    return model
    
