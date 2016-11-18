import pandas as pd
from sqlalchemy import create_engine
xl = pd.ExcelFile("2014aadt.xlsx")
print(xl.sheet_names)
df = xl.parse(xl.sheet_names[0])
df = pandas.read_excel(open('your_xls_xlsx_filename','rb'), sheetname=0)
print(df.head())
parsed = pd.io.parsers.ExcelFile.parse(xl, "Sheet1")
parsed = pd.io.excel.ExcelFile.parse(xl, "Sheet1")
parsed.columns

def connection(user,passwd,dbname):
    str1 = ('postgresql+pg8000://' + user +':' + passw + '@switch-db2.erg.berkeley.edu:5432/'
            + dbname + '?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory')
    engine = create_engine(str1)
    return engine

user = ''
passw = ''
dbname = 'switch_cr'
engine_switch_cr = connection(user,passw,dbname)

table_name = 'test_data'
schema_for_upload = 'sandbox'
pd_data.to_sql(table_name, engine_switch_cr, schema=schema_for_upload)

#get data from another db
#in this case I am connecting to a different db.
engine_switch_chile = connection(user,passw,'switch_chile')
schema = 'chile_new'
table = 'energy_sources'
#The query can be modified to get a particular piece of the data, in this case is a simple *
# to get everything.
string_query = 'select * from ' + schema + '.' + table
pd_data = pd.read_sql_query(string_query,engine_switch_chile)
pd_data

table_name = 'test_data2'
schema_for_upload = 'sandbox'
pd_data.to_sql(table_name, engine_switch_cr, schema=schema_for_upload)
