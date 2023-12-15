import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Read in data (containing weather data)
data = pd.read_excel("/Users/tammy/Documents/CWRU/xLab/Penske_F23/data/Cleveland_Data.xlsx")
cols = ['RATE DAY','RATE MILE','High','Low','Category','Utilization Rate']

seed = 43
df = data[cols]

x = df.drop('Utilization Rate', axis=1)
y = df['Utilization Rate']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 28)

#### Random Forest ####
# Resource: https://medium.com/@theclickreader/random-forest-regression-explained-with-implementation-in-python-3dad88caf165
rf = RandomForestRegressor(n_estimators = 100, random_state = seed)

rf.fit(x_train, y_train)

y_pred = rf.predict(x_test)

rmse = float(format(np.sqrt(mean_squared_error(y_test, y_pred)), '.3f'))
print("Random Forest")
print("RMSE: ", rmse)
errors = y_pred - y_test
mape = 100 * (errors / y_test)
accuracy = 100 - np.mean(mape)
print("Accuracy: {}%".format(round(accuracy, 2)))
print("r-squared:{}".format(r2_score(y_test, y_pred)))
print("mean absolute error: {}".format(round(mean_absolute_error(y_test, y_pred),2)))

# Assuming features are statistically independent
# Note that DATE OUT may simply be important because variance is a factor
feature_importance = rf.feature_importances_
importance_df = pd.DataFrame({"features" : x_train.columns, 'importance': feature_importance})
importance_df.sort_values(by="importance", ascending=False, inplace=True)
print(importance_df)


### RF Plots ###
plt.scatter(y_test, y_pred, color='red', alpha=0.5, label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', label='Ideal Relationship')
plt.title('Predictions vs Actual Utilization Rates using Random Forest Regressor')
plt.xlabel('Actual Utilization Rates')
plt.ylabel('Predicted Utilization Rates')
plt.legend()
plt.show()

#### Gradient Boosting ####
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = seed)
 
gbc = GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, random_state=seed)

gbc.fit(x_train, y_train)

gbc_pred_y = gbc.predict(x_test)

print("\nGradient Boosting")
rmse = float(format(np.sqrt(mean_squared_error(y_test, gbc_pred_y)), '.3f'))
print("RMSE: ", rmse)
errors = gbc_pred_y - y_test
mape = 100 * (errors / y_test)
accuracy = 100 - np.mean(mape)
print("Accuracy: {}%".format(round(accuracy, 2)))
print("r-squared:{}".format(r2_score(y_test, gbc_pred_y)))
print("mean absolute error: {}".format(round(mean_absolute_error(y_test, gbc_pred_y),2)))
feature_importance = gbc.feature_importances_
importance_df = pd.DataFrame({"features" : x_train.columns, 'importance': feature_importance})
importance_df.sort_values(by="importance", ascending=False, inplace=True)
print(importance_df)

plt.scatter(y_test, gbc_pred_y, color='red', alpha=0.5, label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', label='Ideal Relationship')
plt.title('Predictions vs Actual Utilization Rates using Gradient Boosting')
plt.xlabel('Actual Utilization Rates')
plt.ylabel('Predicted Utilization Rates')
plt.legend()
plt.show()

#### Linear Regression ####
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = seed)
reg = LinearRegression().fit(x_train, y_train)
reg_pred_y = reg.predict(x_test)

print("\nLinear Regression")
rmse = float(format(np.sqrt(mean_squared_error(y_test, reg_pred_y)), '.3f'))
print("RMSE: ", rmse)
errors = reg_pred_y - y_test
mape = 100 * (errors / y_test)
accuracy = 100 - np.mean(mape) # accuracy could be high because maybe randomly guessing in a small range
print("Accuracy: {}%".format(round(accuracy, 2)))
print("r-squared:{}".format(r2_score(y_test, reg_pred_y)))
print("mean absolute error: {}".format(round(mean_absolute_error(y_test, reg_pred_y),2)))
feature_importance = reg.coef_
importance_df = pd.DataFrame({"features" : x_train.columns, 'importance': feature_importance})
importance_df.sort_values(by="importance", ascending=False, inplace=True)
print(importance_df)

plt.scatter(y_test, reg_pred_y, color='red', alpha=0.5, label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', label='Ideal Relationship')
plt.title('Predictions vs Actual Utilization Rates using Linear Regressor')
plt.xlabel('Actual Utilization Rates')
plt.ylabel('Predicted Utilization Rates')
plt.legend()
plt.show()
 