"""
############################################
Model building
"""

unit_1_train, unit_1_test = train_test_split(clean_unit1, test_size=0.3)
unit_2_train, unit_2_test = train_test_split(clean_unit2, test_size=0.3)
unit_3_train, unit_3_test = train_test_split(clean_unit3, test_size=0.3)

model1_product = train_model(unit_1_train, ["Raw1"], ["Product1"], "product_1", save_model=False)
model1_byproduct = train_model(unit_1_train, ["Raw1"], ["ByProduct"], "byproduct", save_model=False)
model2_product = train_model(unit_2_train, ["ByProduct_From_1_to_2", "Raw2"], ["Product2"], "product_2", model_type="Non-Linear", save_model=False)
model3_product = train_model(unit_3_train, ["ByProduct_From_1_to_3", "Raw3_1", "Raw3_2"], ["Product3"], "product_3", model_type="Non-Linear", save_model=False)

y_pred_1_product = model1_product.predict(unit_1_test[["Raw1"]])
y_pred_1_byproduct = model1_byproduct.predict(unit_1_test[["Raw1"]])
y_pred_2_product = model2_product.predict(unit_2_test[["ByProduct_From_1_to_2", "Raw2"]])
y_pred_3_product = model3_product.predict(unit_3_test[["ByProduct_From_1_to_3", "Raw3_1", "Raw3_2"]])

unit1_prod_perf = modelperf(y_pred_1_product, unit_1_test[["Product1"]])
unit1_byproduct_perf = modelperf(y_pred_1_byproduct, unit_1_test[["ByProduct"]])
unit2_prod_perf = modelperf(y_pred_2_product, unit_2_test["Product2"])
unit3_prod_perf = modelperf(y_pred_3_product, unit_3_test["Product3"])

print("Unit 1 Product:", unit1_prod_perf)
print("Unit 1 ByProduct:", unit1_byproduct_perf)
print("Unit 2 Product:", unit2_prod_perf)
print("Unit 3 Product:", unit3_prod_perf)

model1_product = train_model(clean_unit1, ["Raw1"], ["Product1"], "product_1", save_model=True)
model1_byproduct = train_model(clean_unit1, ["Raw1"], ["ByProduct"], "byproduct", save_model=True)
model2_product = train_model(clean_unit2, ["ByProduct_From_1_to_2", "Raw2"], ["Product2"], "product_2", model_type="Non-Linear", save_model=True)
model3_product = train_model(clean_unit3, ["ByProduct_From_1_to_3", "Raw3_1", "Raw3_2"], ["Product3"], "product_3", model_type="Non-Linear", save_model=True)

"""
############################################
Corrected Optimizer
"""

def optimizer(
        bounds, 
        opt_params, 
        PRODUCT_SELL_PRICE=PRODUCT_SELL_PRICE, 
        PRODUCT_DEMAND=PRODUCT_DEMAND, 
        PRODUCT_UNMET_DEMAND_PENALTY=PRODUCT_UNMET_DEMAND_PENALTY,
        PRODUCT_STORAGE_COST=PRODUCT_STORAGE_COST, 
        PRODUCT_DISCARD_COST=PRODUCT_DISCARD_COST
        ):
    
    def model(X_in):
        if len(X_in.shape) == 1:
            X_in = X_in.reshape([1,6])
        X_in = pd.DataFrame(X_in, columns=["Raw1","Raw2","Raw3_1","Raw3_2","byproduct_to_unit2","byproduct_to_unit3"])
        if np.isnan(X_in.iloc[0,0]):
            return np.nan
        product1, product2, product3, byproduct = plant(X_in)

        objective = objective_function(product1, product2, product3, byproduct,
                       PRODUCT_SELL_PRICE, PRODUCT_DEMAND, PRODUCT_UNMET_DEMAND_PENALTY,
                       PRODUCT_STORAGE_COST, PRODUCT_DISCARD_COST)

        return -objective.iloc[0]

    result = differential_evolution(model, bounds=bounds, **opt_params)

    return result

"""
############################################
Scenario extraction
"""

def get_scenario_dict():
    all_scenarios = {}

    df = pd.read_excel("scenarios.xlsx", index_col=0, header=[0,1])

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

# Now define which scenarios to run
scenarios_to_run = ['scenario1', 'scenario2', 'scenario3', 'scenario4' ]
scenario_dict = get_scenario_dict()

# Iterate and run the scenarios
for scenario in scenarios_to_run:
    print(f"Running {scenario}...")
    scenario_data = update_scenario(scenario, scenario_dict)
    
    print(f"PRODUCT_DEMAND: {scenario_data['PRODUCT_DEMAND']}")
    print(f"PRODUCT_SELL_PRICE: {scenario_data['PRODUCT_SELL_PRICE']}")
    print(f"PRODUCT_STORAGE_COST: {scenario_data['PRODUCT_STORAGE_COST']}")
    print(f"PRODUCT_DISCARD_COST: {scenario_data['PRODUCT_DISCARD_COST']}")
    print(f"PRODUCT_UNMET_DEMAND_PENALTY: {scenario_data['PRODUCT_UNMET_DEMAND_PENALTY']}")
    print("-------------------")

"""
############################################
Running the optimizer
"""
scenario_dict = get_scenario_dict()

scenario_results = {}
# Run the optimizer for each of these scenarios
for scenario in scenario_dict.keys():
    print(f"Running {scenario}...")
    scenario_data = update_scenario(scenario, scenario_dict)

    PRODUCT_SELL_PRICE = scenario_data.get('PRODUCT_SELL_PRICE', {})
    PRODUCT_DEMAND = scenario_data.get('PRODUCT_DEMAND', {})
    PRODUCT_UNMET_DEMAND_PENALTY = scenario_data.get('PRODUCT_UNMET_DEMAND_PENALTY', {})
    PRODUCT_STORAGE_COST = scenario_data.get('PRODUCT_STORAGE_COST', {})
    PRODUCT_DISCARD_COST = scenario_data.get('PRODUCT_DISCARD_COST', {})

    result = optimizer(BOUNDS, OPT_PARAMS, PRODUCT_SELL_PRICE, PRODUCT_DEMAND,PRODUCT_UNMET_DEMAND_PENALTY,PRODUCT_STORAGE_COST, PRODUCT_DISCARD_COST)

    scenario_results[scenario] = {
        "fun": -result.fun,  
        "x": result.x,      
        
    }

    print(f"Result for {scenario}: {-result.fun}")

"""
############################################
Output Results
"""

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
# Saving the scenarios into CSV's
k=1

scenario_dict = get_scenario_dict()

for scenario in scenario_dict.keys():
    print(f"Running {scenario} with iteration {k}...")
    scenario_data = update_scenario(scenario, scenario_dict)
    result_x = scenario_results[scenario]["x"] 

    PRODUCT_SELL_PRICE = scenario_data.get('PRODUCT_SELL_PRICE', {})
    PRODUCT_DEMAND = scenario_data.get('PRODUCT_DEMAND', {})
    PRODUCT_UNMET_DEMAND_PENALTY = scenario_data.get('PRODUCT_UNMET_DEMAND_PENALTY', {})
    PRODUCT_STORAGE_COST = scenario_data.get('PRODUCT_STORAGE_COST', {})
    PRODUCT_DISCARD_COST = scenario_data.get('PRODUCT_DISCARD_COST', {})

    
    df = model_for_output(result_x, scenario, PRODUCT_SELL_PRICE, PRODUCT_DEMAND,PRODUCT_UNMET_DEMAND_PENALTY,PRODUCT_STORAGE_COST, PRODUCT_DISCARD_COST)
    df.to_csv(f"scenario_output_{k}.csv")
    k = k+1


"""
############################################
Some analysis
"""

#Change number of scenarios to run here
scenario_dict = get_scenario_dict()
scenarios_to_run = list(scenario_dict.keys())
csv_files = [f"scenario_output_{i}.csv" for i in range(1, len(scenarios_to_run) + 1)]

total_revenues = []
scenario_labels = []

for scenario, csv_file in zip(scenarios_to_run, csv_files):

    df = pd.read_csv(csv_file)
    total_revenue = df["Total Revenue"].iloc[0]  
    print(total_revenue)
    total_revenues.append(total_revenue)
    scenario_labels.append(scenario)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=scenario_labels,  
    y=total_revenues,   
    name="Total Revenue",
    marker_color='lightblue'
))

fig.update_layout(
    title="Total Revenue Comparison Across Scenarios",
    xaxis_title="Scenario",
    yaxis_title="Total Revenue",
    barmode="group",
    template="plotly_white"
)

fig.show()

from tabulate import tabulate

total_revenues = []
scenario_labels = []
product1_production = []
product2_production = []
product3_production = []
raw1_values = []
raw2_values = []
raw3_1_values = []
raw3_2_values = []
byproduct_unit2 = []
byproduct_unit3 = []
for scenario, csv_file in zip(scenarios_to_run, csv_files):

    df = pd.read_csv(csv_file)
    total_revenue = df["Total Revenue"]

    product1 = df["Product1_production"].iloc[0]  
    product2 = df["Product2_production"].iloc[0]  
    product3 = df["Product3_production"].iloc[0]

    raw1 = df["Raw1"].iloc[0]
    raw2 = df["Raw2"].iloc[0]
    raw3_1 = df["Raw3_1"].iloc[0]
    raw3_2 = df["Raw3_2"].iloc[0]
    Weight_byproduct_to_unit2 = df["Weight_byproduct_to_unit2"].iloc[0]
    Weight_byproduct_to_unit3 = df["Weight_byproduct_to_unit3"].iloc[0]

    
    product1_production.append(product1)
    product2_production.append(product2)
    product3_production.append(product3)

    raw1_values.append(raw1)
    raw2_values.append(raw2)
    raw3_1_values.append(raw3_1)
    raw3_2_values.append(raw3_2)
    byproduct_unit2.append(Weight_byproduct_to_unit2)
    byproduct_unit3.append(Weight_byproduct_to_unit3)
    scenario_labels.append(scenario)

# Create a summary DataFrame to print the comparison
summary_df = pd.DataFrame({
    "Scenario": scenario_labels,
    "Raw1": raw1_values,
    "Raw2": raw2_values,
    "Raw3_1": raw3_1_values,
    "Raw3_2": raw3_2_values,
    "Product1_Production": product1_production,
    "Product2_Production": product2_production,
    "Product3_Production": product3_production,
    "Weight_byproduct_to_unit2": byproduct_unit2,
    "Weight_byproduct_to_unit3": byproduct_unit3,
    
})
headers = ["Scenario", "Product1_Production", "Product2_Production", "Product3_Production", 
           "Raw1", "Raw2", "Raw3_1", "Raw3_2", "Weight_byproduct_to_unit2", "Weight_byproduct_to_unit3"]

print("\nSummary of All Scenarios:\n")
print(tabulate(summary_df, headers, tablefmt="fancy_grid", numalign="center", stralign="center"))


# Create the bar chart
fig = go.Figure()

# Adding Product1 Production
fig.add_trace(go.Bar(
    x=scenario_labels,  
    y=product1_production,  
    name="Product1 Production",
    marker_color='lightblue'
))

fig.add_trace(go.Bar(
    x=scenario_labels,
    y=product2_production,
    name="Product2 Production",
    marker_color='lightgreen'
))

# Adding Product3 Production
fig.add_trace(go.Bar(
    x=scenario_labels,
    y=product3_production,
    name="Product3 Production",
    marker_color='palevioletred'
))

# Adding Raw1 as a Line Graph
fig.add_trace(go.Scatter(
    x=scenario_labels,
    y=raw1_values,
    name="Raw1",
    mode='lines+markers',
    line=dict(color='black', width=2),
    yaxis="y2"  # Use secondary y-axis
))

# Adding Raw2 as a Line Graph
fig.add_trace(go.Scatter(
    x=scenario_labels,
    y=raw2_values,
    name="Raw2",
    mode='lines+markers',
    line=dict(color='orange', width=2),
    yaxis="y2"  # Use secondary y-axis
))

# Adding Raw3_1 as a Line Graph
fig.add_trace(go.Scatter(
    x=scenario_labels,
    y=raw3_1_values,
    name="Raw3_1",
    mode='lines+markers',
    line=dict(color='purple', width=2),
    yaxis="y2"  
))

# Adding Raw3_2 as a Line Graph
fig.add_trace(go.Scatter(
    x=scenario_labels,
    y=raw3_2_values,
    name="Raw3_2",
    mode='lines+markers',
    line=dict(color='pink', width=2),
    yaxis="y2"  
))

# Update layout to include a secondary y-axis
fig.update_layout(
    title="Product Production and Raw Material Values Across Scenarios",
    xaxis_title="Scenarios",
    yaxis_title="Product Production",
    yaxis2=dict(
        title="Raw Values",
        overlaying="y",
        side="right"
    ),
    barmode="group"
)


fig.show()