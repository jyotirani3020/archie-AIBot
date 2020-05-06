import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pickle



company_data = {'bosch' : 'test/data/bosch.csv', }

def prediction(file):
    df = pd.read_csv(file)
    # Filter records for store 1 and item 1 -> to be able to scale to other items in the future
    df = df[df['store'] == 1]
    df = df[df['item'] == 1]

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d') # convert date column to datatime object

    # Create Date-related Features to be used for EDA and Supervised ML: Regression
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday
    df['weekday'] = np.where(df.weekday == 0, 7, df.weekday)
    reg_df = df
    for i in range(1,8):
        lag_i = 'lag_' + str(i)
        reg_df[lag_i] = reg_df.sales.shift(i)

    # Rolling window
    reg_df['rolling_mean'] = reg_df.sales.rolling(window=7).mean()
    reg_df['rolling_max'] = reg_df.sales.rolling(window=7).max()
    reg_df['rolling_min'] = reg_df.sales.rolling(window=7).min()

    reg_df = reg_df.dropna(how='any', inplace=False)
    reg_df = reg_df.drop(['store', 'item'], axis=1)

    # Split the series to predict the last 3 months of 2017
    reg_df = reg_df.set_index('date')
    reg_test_df = reg_df.loc['2017-10-01':]


    X_test = reg_test_df.drop(['sales'], axis=1)
    y_test = reg_test_df['sales'].values

    #Univariate SelectKBest class to extract top 5 best features

    X_test = X_test[['rolling_mean', 'rolling_max', 'rolling_min', 'lag_7', 'lag_1']]

    # fit model
    model = pickle.load(open('test/models/market_model.pkl','rb'))

    preds = model.predict(X_test)
    errors_df = reg_test_df[['sales']]
    errors_df['pred_sales'] = preds
    errors_df['errors'] = preds - y_test
    errors_df.insert(0, 'model', 'LinearRegression')
    result_df_lr = errors_df.groupby('model').agg(total_pred_sales=('pred_sales', 'sum'))
    arr = np.array(result_df_lr['total_pred_sales'])
    return int(arr)


def market_demand_function(demand, company):
    data_path = company_data[company]
    predicted_sale = prediction(data_path)
    diff = predicted_sale - demand
    if diff>0:
        return "you may need to produce more bearings, according to my analysis bearings sale would increase by {} bearings.".format(''.join(str(abs(diff))))
    else:
        return "you may need to reduce the production, according to my analysis bearings sale would reduced by {} bearings.".format(''.join(str(abs(diff))))
