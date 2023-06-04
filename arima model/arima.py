import pandas as pd
from pmdarima.arima import auto_arima
from statsmodels.tsa.stattools import adfuller

dataset = pd.read_csv('nike_stock_data.csv', index_col = 'Date')
data = dataset['Close'].dropna()

# Perform Dickey-Fuller test for differencing
result = adfuller(data)
if result[1] < 0.05: # result[1] is the p-value
    print('The data is stationary and does not require differencing.')
else:
    print('The data is not stationary and requires differencing.')

    # Find the best order using auto_arima
    model = auto_arima(data, seasonal = False, trace = True)
    order = model.order

    # Perform differencing
    differenced_data = data.diff().dropna()

    # Perform Dickey-Fuller test on differenced data
    result_diff = adfuller(differenced_data)
    if result_diff[1] < 0.05:
        print('Differencing was successful. The differenced data is stationary.')
        data = differenced_data
        print('New order:', order)
    else:
        print('Differencing was not successful. Please review the data.')

# Check for seasonality
seasonal_model = auto_arima(data, seasonal = True, m = 12, trace=True, error_action = 'ignore', suppress_warnings = True)
if seasonal_model.order != (0, 0, 0) or seasonal_model.seasonal_order != (0, 0, 0, 0):
    print('The data has seasonality.')
    print('Seasonal order:', seasonal_model.seasonal_order)
    model = seasonal_model
else:
    print('The data does not have seasonality.')
    model = auto_arima(data, seasonal = False, trace = True, error_action = 'ignore', suppress_warnings = True)

# Fit ARIMA model with the selected order
model.fit(data)

# Print model summary
print(model.summary())