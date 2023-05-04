import pandas as pd

# from sklearn import preprocessing
from sklearn import linear_model


# Class for Delivery Machine Learning model
class DeliveryML:
    def __init__(self, df):
        self.df = df  # uploading dataframe for fitting
        self.reg = linear_model.Lasso(alpha=0.1)  # init linear regression model

    # Preprocess uploaded dataframe
    def preprocess(self):
        df_dum_type = pd.get_dummies(self.df['Вид доставки'])
        df_dum_time = pd.get_dummies(self.df['Время суток'])
        self.df = pd.concat([self.df["Количество км"], df_dum_type, df_dum_time, self.df["Наличие грузчика"], self.df["Стоимость"]], axis=1)
    # Fitting model
    def fit(self):
        self.reg.fit(X=self.df[["Количество км", "Пеший", "Легковой", "Минивэн", "Газель", "Удлиненная газель",
                         "Ночь", "Рабочее время", "Раннее утро/поздний вечер", "Наличие грузчика"]], y=self.df["Стоимость"])

    # Predicting price with input vector
    def predict(self, vec):
        return self.reg.predict([vec])[0] // 10 * 10
