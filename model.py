import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
import joblib

data = pd.read_csv("organized_carbon.csv")

X = data.drop(columns= ["CarbonEmission"])
y = data["CarbonEmission"]

X_train , X_test, y_train , y_test = tts(X,y, test_size= 0.2 , random_state= 31)

xgb_model= xgb.XGBRegressor(n_estimators= 450,learning_rate = 0.15,max_depth=3,random_state=3)
xgb_model.fit(X_train,y_train)

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.metrics import r2_score


xgb_train_pred = xgb_model.predict(X_train)
xgb_test_pred = xgb_model.predict(X_test)

print("XGB\n")

xgb_train_r2 = r2_score(y_train, xgb_train_pred)
xgb_test_r2 = r2_score(y_test, xgb_test_pred)
xgb_train_mae = mean_absolute_error(y_train, xgb_train_pred)
xgb_test_mae = mean_absolute_error(y_test, xgb_test_pred)

print("Eğitim Seti MAE Yüzdelik Başarı:","%", 100-(xgb_train_mae/y_train.mean()*100))
print("Test Seti MAE Yüzdelik Başarı:","%", 100-(xgb_test_mae/y_train.mean()*100))
print(50*"*")
print("Eğitim Seti R² Skoru:", xgb_train_r2*100)
print("Test Seti R² Skoru:", xgb_test_r2*100)


# After testing the accuracy with train_test_split, training the model with whole data

final_xgb_model = xgb.XGBRegressor(n_estimators= 450,learning_rate = 0.15,max_depth=3,random_state=3)
final_xgb_model.fit(X,y)

joblib.dump(final_xgb_model, 'final_xgb_model.pkl')



