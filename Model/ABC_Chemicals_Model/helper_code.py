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
    
def get_scenario_dict(scenario_file_name):
    all_scenarios = {}

    df = pd.read_excel(scenario_file_name, index_col=0, header=[0,1])

    for ii in range(df.shape[0]):
        for jj in range(5):
            all_scenarios[df.index[ii]] = {
                "PRODUCT_SELL_PRICE": {
                    "Product1": df.iloc[ii,0], 
                    "Product2": df.iloc[ii,1], 
                    "Product3": df.iloc[ii,2]
                    },
                "PRODUCT_DEMAND": {
                    "Product1": df.iloc[ii,3], 
                    "Product2": df.iloc[ii,4], 
                    "Product3": df.iloc[ii,5]
                    },
                "PRODUCT_UNMET_DEMAND_PENALTY": {
                    "Product1": df.iloc[ii,14], 
                    "Product2": df.iloc[ii,15], 
                    "Product3": df.iloc[ii,16]
                    },
                "PRODUCT_STORAGE_COST": {
                    "Product1": df.iloc[ii,6], 
                    "Product2": df.iloc[ii,7], 
                    "Product3": df.iloc[ii,8], 
                    "byproduct": df.iloc[ii,9]
                    },
                "PRODUCT_DISCARD_COST": {
                    "Product1": df.iloc[ii,10], 
                    "Product2": df.iloc[ii,11], 
                    "Product3": df.iloc[ii,12], 
                    "byproduct": df.iloc[ii,13]
                    }
                }

    return all_scenarios

# Define a function to handle scenario updates dynamically
def update_scenario(
        scenario_key,
        scenario_dict
    ):

    return {
        'PRODUCT_SELL_PRICE': scenario_dict[scenario_key]['PRODUCT_SELL_PRICE'],
        'PRODUCT_DEMAND': scenario_dict[scenario_key]['PRODUCT_DEMAND'],
        'PRODUCT_UNMET_DEMAND_PENALTY': scenario_dict[scenario_key]['PRODUCT_UNMET_DEMAND_PENALTY'],
        'PRODUCT_STORAGE_COST': scenario_dict[scenario_key]['PRODUCT_STORAGE_COST'],
        'PRODUCT_DISCARD_COST': scenario_dict[scenario_key]['PRODUCT_DISCARD_COST']
    }

def model_for_output(
        X_in, 
        scenario, 
        PRODUCT_SELL_PRICE, 
        PRODUCT_DEMAND, 
        PRODUCT_UNMET_DEMAND_PENALTY,
        PRODUCT_STORAGE_COST, 
        PRODUCT_DISCARD_COST
    ):
    if len(X_in.shape) == 1:
        X_in = X_in.reshape([1,6])
    X_in = pd.DataFrame(X_in, columns=["Raw1","Raw2","Raw3_1","Raw3_2","byproduct_to_unit2","byproduct_to_unit3"])
    if np.isnan(X_in.iloc[0,0]):
        return np.nan
    product1, product2, product3, byproduct = plant(X_in)

    print(product1, product2, product3, byproduct)
    (objective, Product1_revenue, Product1_over_production_cost, Product1_under_production_cost, 
     Product2_revenue, Product2_over_production_cost, Product2_under_production_cost, Product3_revenue, 
     Product3_over_production_cost, Product3_under_production_cost, excess_byproduct_cost) = objective_function(product1, product2, product3, byproduct,
                    PRODUCT_SELL_PRICE, PRODUCT_DEMAND, PRODUCT_UNMET_DEMAND_PENALTY,
                    PRODUCT_STORAGE_COST, PRODUCT_DISCARD_COST, True)

    output_df_dict = {
        "Scenario": [scenario],
        "Raw1": [X_in.loc[0,"Raw1"]],
        "Raw2": [X_in.loc[0,"Raw2"]],
        "Raw3_1": [X_in.loc[0,"Raw3_1"]],
        "Raw3_2": [X_in.loc[0,"Raw3_2"]],
        "Weight_byproduct_to_unit2": [X_in.loc[0,"byproduct_to_unit2"]],
        "Weight_byproduct_to_unit3": [X_in.loc[0,"byproduct_to_unit3"]],
        "Product1_production": [product1[0]],
        "Product2_production": [product2[0]],
        "Product3_production": [product3[0]],
        "Byproduct_production": [byproduct[0]],
        "Total Revenue": [objective.iloc[0]],
        "Product1_Revenue": [Product1_revenue[0]],
        "Product1_Over_Production_cost": [Product1_over_production_cost[0]],
        "Product1_Under_Production_cost": [Product1_under_production_cost[0]],
        "Product2_Revenue": [Product2_revenue[0]],
        "Product2_Over_Production_cost": [Product2_over_production_cost[0]],
        "Product2_Under_Production_cost": [Product2_under_production_cost[0]],
        "Product3_Revenue": [Product3_revenue[0]],
        "Product3_Over_Production_cost": [Product3_over_production_cost[0]],
        "Product3_Under_Production_cost": [Product3_under_production_cost[0]],
        "Excess_byproduct_cost": [excess_byproduct_cost[0]],
    }
    return pd.DataFrame(output_df_dict)