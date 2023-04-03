import logging


from fastapi import FastAPI, HTTPException
import pandas as pd

from app.internal import helpers
from app.internal.schema import delivery as schema
from app.internal.model import delivery as ml


# Setup logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s %(message)s")

# Create instance of FastAPI app
app = FastAPI()

# Reading train data from file
df_train = pd.read_csv("app/internal/model/train_df.csv").drop(columns='Unnamed: 0')

# Create instance of Machine Learning Linear Regression model
model = ml.DeliveryML(df_train)


# Startup event
@app.on_event("startup")
async def startup_event():
    model.preprocess()  # preprocessing train dataframe
    model.fit()  # fitting model
    logging.info("Мachine Learning model is ready")
    logging.info("App is ready")


# Endpoint for estimating price for delivery
@app.get("/price")
async def get_price(d: schema.Delivery):
    try:
        vec = helpers.convert_vector(d)  # converting input data to model vector
        price = model.predict(vec)  # predicting price
    except:
        raise HTTPException(status_code=500, detail="Internal server error")  # raising error on every server error

    return {
        "price": price
    }
