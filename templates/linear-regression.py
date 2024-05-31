# data manipulation
import pandas as pd
import numpy as np

# data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# model building and diagnostics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import zscore, probplot
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_selection import SelectKBest, f_regression

# sample data
np.random.seed(42)
data = pd.DataFrame({
    'Is Prior Customer': np.random.choice([0, 1], size=1000),
    'Salesperson Tenure': np.random.randint(1, 120, size=1000),
    'Percent of Purchases above $100': np.random.uniform(0, 1, size=1000),
    'Percent of Purchases with Tip': np.random.uniform(0, 1, size=1000),
    'Growth Rate': np.random.uniform(0, 1, size=1000)
})

# EDA
print(data.describe())
print(data.info())
sns.pairplot(data)
plt.show()

# Handling outliers using Z-score
z_scores = np.abs(zscore(data[['Salesperson Tenure', 'Percent of Purchases above $100', 'Percent of Purchases with Tip', 'Growth Rate']]))
data = data[(z_scores < 3).all(axis=1)]

# Balancing the dataset
X = data.drop(columns=['Growth Rate'])
y = data['Growth Rate']

rus = RandomUnderSampler(sampling_strategy='auto', random_state=42)
X_res, y_res = rus.fit_resample(X, y)

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# Define column transformer
numeric_features = ['Salesperson Tenure', 'Percent of Purchases above $100', 'Percent of Purchases with Tip']
categorical_features = ['Is Prior Customer']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Feature Selection
feature_selector = SelectKBest(score_func=f_regression, k='all')

# Define the model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_selection', feature_selector),
    ('regressor', LinearRegression())
])

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Cross-validation
cv_scores = cross_val_score(model, X_res, y_res, cv=5, scoring='neg_mean_squared_error')
print(f'Cross-validated MSE: {-cv_scores.mean()}')

# Feature Importance
# Extracting feature importances from the model
regressor = model.named_steps['regressor']
feature_importances = regressor.coef_

# OneHotEncoder will create multiple columns for 'Is Prior Customer'
feature_names = numeric_features + list(model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_features))

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
})

print(importance_df)

# Plotting the feature importances
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df)
plt.title('Feature Importances')
plt.show()

# Additional Visualizations to Evaluate Model Quality

# Residual vs Fitted Plot
residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
sns.residplot(x=y_pred, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 2})
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted')
plt.show()

# QQ Plot
plt.figure(figsize=(10, 6))
probplot(residuals, dist="norm", plot=plt)
plt.title('QQ Plot')
plt.show()

# Histogram of Residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# Predicting for a new datapoint
new_data_point = pd.DataFrame({
    'Is Prior Customer': [1],  # Change this to 0 to see the impact
    'Salesperson Tenure': [60],
    'Percent of Purchases above $100': [0.5],
    'Percent of Purchases with Tip': [0.3]
})

predicted_growth_rate = model.predict(new_data_point)
print(f'Predicted Growth Rate for new data point: {predicted_growth_rate[0]}')

# Highlighting the impact of "Is Prior Customer"
new_data_point_non_customer = new_data_point.copy()
new_data_point_non_customer['Is Prior Customer'] = 0
predicted_growth_rate_non_customer = model.predict(new_data_point_non_customer)

impact_prior_customer = predicted_growth_rate[0] - predicted_growth_rate_non_customer[0]
print(f'Impact of "Is Prior Customer" on Growth Rate: {impact_prior_customer}')
