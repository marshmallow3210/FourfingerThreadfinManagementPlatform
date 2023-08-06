import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor

# input x
days= 210 # 0 to 210 days
step = 30 # interval 30 days
phase = days//step + 1 # phase = 8
x_set = np.linspace(0, days, phase)

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(x_set.reshape(-1, 1))

# input all_set
all_set = np.array([])

# create a figure with a 2x3 grid of subplots
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(2, 3, 1)  # top left
ax2 = fig.add_subplot(2, 3, 2)  # top center
ax3 = fig.add_subplot(2, 3, 3)  # top right
ax4 = fig.add_subplot(2, 3, 4)  # bottom left
ax5 = fig.add_subplot(2, 3, 5)  # bottom center

# CHB
chb = np.array([16, 27, 66, 188, 368, 625, 856, 1077])
chb = chb * 800 / 1336
all_set = np.append(all_set, chb)
chb_model = LinearRegression()
chb_model.fit(X_poly, chb)
chb_pred = chb_model.predict(X_poly)

ax1.scatter(x_set, chb, color='tab:orange')
ax1.plot(x_set, chb_pred, color='tab:blue')
ax1.set_xticks(np.arange(0, 270, 30))
ax1.set_yticks(np.arange(0, 900, 100))
ax1.set_title('CHB chart')
ax1.set_xlabel('Age(d)')
ax1.set_ylabel('Body weight(g)')

# CHP
chp = np.array([16, 27, 77, 208, 379, 606, 862, 1102])
chp = chp * 800 / 1336
all_set = np.append(all_set, chp)
chp_model = LinearRegression()
chp_model.fit(X_poly, chp)
chp_pred = chp_model.predict(X_poly)

ax2.scatter(x_set, chp, color='tab:orange')
ax2.plot(x_set, chp_pred, color='tab:blue')
ax2.set_xticks(np.arange(0, 270, 30))
ax2.set_yticks(np.arange(0, 900, 100))
ax2.set_title('CHP chart')
ax2.set_xlabel('Age(d)')
ax2.set_ylabel('Body weight(g)')

# CHS
chs = np.array([16, 48, 108, 246, 425, 717, 904, 1180])
chs = chs * 800 / 1336
all_set = np.append(all_set, chs)
chs_model = LinearRegression()
chs_model.fit(X_poly, chs)
chs_pred = chs_model.predict(X_poly)

ax3.scatter(x_set, chs, color='tab:orange')
ax3.plot(x_set, chs_pred, color='tab:blue')
ax3.set_xticks(np.arange(0, 270, 30))
ax3.set_yticks(np.arange(0, 900, 100))
ax3.set_title('CHS chart')
ax3.set_xlabel('Age(d)')
ax3.set_ylabel('Body weight(g)')

# SMS
sms = np.array([16, 42, 106, 276, 477, 754, 991, 1202])
sms = sms * 800 / 1336
all_set = np.append(all_set, sms)
sms_model = LinearRegression()
sms_model.fit(X_poly, sms)
sms_pred = sms_model.predict(X_poly)

ax4.scatter(x_set, sms, color='tab:orange')
ax4.plot(x_set, sms_pred, color='tab:blue')
ax4.set_xticks(np.arange(0, 270, 30))
ax4.set_yticks(np.arange(0, 900, 100))
ax4.set_title('SMS chart')
ax4.set_xlabel('Age(d)')
ax4.set_ylabel('Body weight(g)')

# all
all_x = np.array([])
for i in range(0, 4):
    x = np.linspace(0, days, phase)
    all_x = np.append(all_x, x)

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(all_x.reshape(-1, 1))
all_model = LinearRegression()
all_model.fit(X_poly, all_x)
all_pred = all_model.predict(X_poly)

# 建立KNN Regression模型，K值設為3
k = 3
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(all_x.reshape(-1, 1), all_set)

# 預測在x=60時y的值
x_new = np.array([60])
print("input Age(d):", x_new)
y_pred = knn.predict(x_new.reshape(-1, 1))

# 印出預測結果
print("predicted Body weight(g):", y_pred)

ax5.scatter(all_x, all_set, color='tab:gray', s=3)
ax5.plot(x_set, chb_pred, color='tab:red', linewidth=2)
ax5.plot(x_set, chp_pred, color='tab:green', linewidth=2)
ax5.plot(x_set, chs_pred, color='tab:orange', linewidth=2)
ax5.plot(x_set, sms_pred, color='tab:blue', linewidth=2)
ax5.set_xticks(np.arange(0, 270, 30))
ax5.set_yticks(np.arange(0, 900, 100))
ax5.set_title('Four strains of sea bass')
ax5.set_xlabel('Age(d)')
ax5.set_ylabel('Body weight(g)')


fig.tight_layout()
# plt.subplot_tool()
plt.show()