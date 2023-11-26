import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


abalone = fetch_ucirepo(id=1)
X = abalone.data.features
y = abalone.data.targets

# One hot encoding for categorical variable
df = X.copy()
df = pd.concat([df.drop("Sex", axis=1), pd.get_dummies(df["Sex"])], axis=1)
X = df.copy()

# Non-linear transformation
X["Length^2"] = X["Length"] ** 2
X["Diameter^2"] = X["Diameter"] ** 2
X["Height^2"] = X["Height"] ** 2
X["Whole weight^2"] = X["Whole_weight"] ** 2
X["Shucked weight^2"] = X["Shucked_weight"] ** 2
X["Viscera weight^2"] = X["Viscera_weight"] ** 2
X["Shell weight^2"] = X["Shell_weight"] ** 2

# Model on full dataset
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
score = r2_score(y, y_pred)
print("Full dataset train and eval R2 score:", round(score, 2))

# 70-15-15 Cross-validation
repeats = 100
r2 = np.zeros(repeats)
for i in range(repeats):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=i)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=i)
    model.fit(X_train, y_train)
    r2[i] = r2_score(y_test, model.predict(X_test))
print(f"70-15-15 Cross-validation boxplot: mean={r2.mean():.2f}, std={r2.std():.2f}")

# Creating Box Plot
plt.boxplot(r2)
plt.title("70-15-15 Cross-validation boxplot")
plt.ylabel("R2 score Distribution")
plt.show()