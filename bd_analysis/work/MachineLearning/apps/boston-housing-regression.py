#!/opt/conda/bin/python
# -*- coding: utf-8 -*-
# (1)导入数据
from sklearn.datasets import load_boston
boston = load_boston()

# (2)分割数据
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    boston.data,
    boston.target,
    test_size = 0.3,
    random_state = 0
)

# (3)导入线性回归模型并训练之
from sklearn.linear_model import LinearRegression

LR = LinearRegression()

LR.fit(X_train, y_train)

# (4)在测试集上预测
y_pred = LR.predict(X_test)

# (5)评估模型
from sklearn import metrics
mse = metrics.mean_squared_error(y_test, y_pred)
print('MSE = ', mse)