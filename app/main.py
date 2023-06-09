import logging


from fastapi import FastAPI, HTTPException, APIRouter
import pandas as pd

from app.internal import helpers
from app.internal.schema import delivery as schema
from app.internal.model import delivery as ml
from fastapi.middleware.cors import CORSMiddleware

# Setup logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s %(message)s")

# Create instance of FastAPI app
app = FastAPI(
    title="Price Estimator Service Documentation",
    description="The Truckly delivery price prediction service provides an estimated order delivery cost based on "
                "several factors, including the distance between the departure and destination points, the presence "
                "of a loader and the type of delivery.",
    version="1.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post("/price", tags=["Price"])
async def get_price(d: schema.Delivery):
    try:
        vec = helpers.convert_vector(d)  # converting input data to model vector
        price = model.predict(vec)  # predicting price
    except:
        raise HTTPException(status_code=500, detail="Internal server error")  # raising error on every server error

    return {
        "price": price
    }
