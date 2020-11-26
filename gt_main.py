import pandas as pd
from pytrends.request import TrendReq

# Data import
data = pd.read_excel('keywords_trends.xlsx', index_col=False)
dl = data['Keyword'].to_list()
final_excel = 'google_trends_kw.xlsx'
print('Number of keywords: ', len(dl))

# Data preprocessing
# tz = Area Code (for Hamburg = 040) !!!
pt = TrendReq(hl='de-DE', tz='040', timeout=(10, 25), retries=3)

kw_list = []
kw_list_region = []

for x in dl:
    keywords = [x]
    print(keywords)
    pt.build_payload(kw_list=keywords, cat=0, timeframe='today 12-m', geo='DE', gprop='')
    iot = pt.interest_over_time()

    if not iot.empty:
        iot = iot.drop(labels=['isPartial'], axis='columns')
        kw_list.append(iot)

    ibr = pt.interest_by_region()

    if not ibr.empty:
        kw_list_region.append(ibr)

# Dataframes
kw_df = pd.concat(kw_list, axis=1)
kw_df_region = pd.concat(kw_list_region, axis=1)

# Fine tuning of dfs
kw_df.index = pd.to_datetime(kw_df.index, format='%m/%d/%Y').strftime('%Y-%m-%d')


# Writing to excel
writer = pd.ExcelWriter(final_excel, engine='xlsxwriter')
kw_df.to_excel(excel_writer=writer, sheet_name='Datenbasis (Interest over time)')
kw_df_region.to_excel(excel_writer=writer, sheet_name='Datenbasis (By region)')
writer.save()
writer.close()
