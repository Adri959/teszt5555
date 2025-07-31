import pandas as pd
import datetime as dt
data = {
    'Név': ['Anna', 'Béla', 'Cecília'],
    'Kor': [23, 35, 29]
}

df = pd.DataFrame(data)
print(df)

maidatum = dt.date.today()
tegnapidatum = maidatum - dt.timedelta(days=1)
print(maidatum)
print(tegnapidatum)