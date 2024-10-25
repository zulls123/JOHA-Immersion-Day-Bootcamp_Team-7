from fastapi import FastAPI
import pandas as pd
from typing import List

app = FastAPI()

# Load the CSV data
csv_file_path = 'Data_Inputs.csv'  # Ensure the path to the CSV is correct
data = pd.read_csv(csv_file_path)

# Define a route for the API to return the CSV data as JSON
@app.get("/api/data")
async def get_data():
    return data.to_dict(orient='records')

# Run the server: You can run the app using `uvicorn main:app --reload`
