import pandas as pd
import requests

url = 'https://secure.splitwise.com/api/v3.0/get_expenses'
header = {'Authorization':'Bearer xxxx'}
params = {'limit':2000,
          'friend_id':xxx or 'xxx'}  #3036417, 48188656
data = requests.get(url=url, headers = header, params=params).json()
expense_df = pd.DataFrame.from_dict(data)
print(expense_df)
expense_df.to_csv('Expenses_data.csv')
