import pandas as pd
xl = pd.ExcelFile("2014aadt.xlsx")
print(xl.sheet_names)
df = xl.parse(xl.sheet_names[0])
print(df.head())
