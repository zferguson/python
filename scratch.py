import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA

# Load your dataset
data = pd.read_csv('your_dataset.csv')

# Separate features and target variable
X = data.drop('target', axis=1)
y = data['target']

# Perform one-hot encoding on categorical features
categorical_features = ['feature1', 'feature2']  # Add your categorical feature names here
X_encoded = pd.get_dummies(X, columns=categorical_features)

# Scale the numerical features
numerical_features = ['numerical1', 'numerical2']  # Add your numerical feature names here
scaler = StandardScaler()
X_encoded[numerical_features] = scaler.fit_transform(X_encoded[numerical_features])

# Reduce dimensionality using PCA
pca = PCA(n_components=0.95)  # Adjust the desired explained variance ratio as needed
X_reduced = pca.fit_transform(X_encoded)

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_reduced, y, test_size=0.2, random_state=42)

# Create ElasticNetCV model
model = ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, .99, 1], cv=5)

# Fit the model
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")

# Perform nested cross-validation to find best lambda and L1 ratio
param_grid = {'alpha': [0.001, 0.01, 0.1, 1.0, 10.0], 'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9]}  # Adjust the range of lambda and L1 ratio values as needed
nested_cv = GridSearchCV(model, param_grid, cv=5)
nested_cv.fit(X_reduced, y)

best_lambda = nested_cv.best_params_['alpha']
best_l1_ratio = nested_cv.best_params_['l1_ratio']
print(f"Best lambda value: {best_lambda}")
print(f"Best L1 ratio: {best_l1_ratio}")

# Refit the model with the best lambda and L1 ratio
best_model = ElasticNetCV(l1_ratio=[best_l1_ratio], cv=5, alpha=best_lambda)
best_model.fit(X_train, y_train)

# Evaluate the best model
best_accuracy = best_model.score(X_test, y_test)
print(f"Accuracy with best lambda and L1 ratio: {best_accuracy}")