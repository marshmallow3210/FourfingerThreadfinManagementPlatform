import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

# 午仔魚
# 9 months
date1 = datetime.date(2015,4,1)
date2 = datetime.date(2016,11,30)
days_count = (date2-date1).days
x_set = np.arange(0, days_count-29, 30)
x_set = x_set[:, np.newaxis]
y_set = np.array([0, 2, 15, 47, 73, 81, 116, 157, 178, 193, 190, 195, 199, 202, 208, 215, 230, 238, 250, 260])
y_set = y_set * 600 / 328

# X_train, X_test, y_train, y_test = train_test_split(x_set, y_set, test_size=0.2, random_state=32)
knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(x_set.reshape(-1, 1), y_set)
y_pred = knn.predict(x_set)

mae = mean_absolute_error(y_set, y_pred)
print("Mean Absolute Error:", mae)
mse = mean_squared_error(y_set, y_pred)
print("Mean Squared Error:", mse)

# Sort the data for plotting
X_sorted = np.sort(x_set, axis=0)
y_pred_sorted = knn.predict(X_sorted)

plt.figure(figsize=(12,8))
plt.scatter(x_set, y_set, color='tab:green', s=12)
plt.plot(X_sorted, y_pred_sorted, color='tab:blue', label='Regression Line', linewidth=4.0)
plt.xticks(np.arange(0, days_count, 30), fontsize=20)
plt.yticks(np.arange(0, 700, 100), fontsize=20)
plt.xlabel('Age(d)', fontsize=24, weight='bold')
plt.ylabel('Body weight(g)', fontsize=24, weight='bold')
plt.title('The growth curve of four finger threadfin', fontsize=24, weight='bold')
plt.grid(linestyle = '--', linewidth = 0.5)
plt.show()