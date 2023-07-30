import logging
import os
from datetime import datetime, timedelta

import pandas as pd
import requests

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")

class PreProcess(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        futures = pd.read_csv("data/raw/futures prices.csv")


        # merged_11 fully joined, cleaned
        # merged scaled: merged_11 + standardised


        # re-organise the dataframe
        futures["DATE"]= pd.to_datetime(futures['date'], format='%d/%m/%Y')
        futures = futures.set_index('DATE')
        futures = futures.drop(['TRADINGDAY','id','Unnamed: 0'],axis=1)
        # Re-order columns for better reading
        futures=futures.iloc[:,[0,2,1,3,4]]
        # Extract the Main Contract at each time and re-build a dataframe consisting of continous main contracts
        al_price = futures[futures.INSTRUMENTID.str.startswith("al")].reset_index()
        al_price["exec_year"] = "20"+al_price.INSTRUMENTID.str[2:4]
        al_price["exec_month"] = al_price.INSTRUMENTID.str[-2:]
        al_price["exec_date"] = al_price["exec_year"]+"-"+al_price["exec_month"]+"-"+ "15"
        al_price["exec_date"] = pd.to_datetime(al_price["exec_date"])
        al_price["exec_begin_date"] = al_price["exec_date"] - pd.DateOffset(months =1)
        al_price = al_price[(al_price["DATE"] > al_price["exec_begin_date"]) & (al_price["DATE"] <= al_price["exec_date"])]
        al_price = al_price.reset_index(drop=True).sort_values("DATE").drop(["exec_year","exec_month","exec_date","exec_begin_date"], axis =1)
        al_price = al_price[al_price.SETTLEMENTPRICE.isnull()==False].reset_index(drop=True)

        al_price=al_price[['DATE','SETTLEMENTPRICE']]

        # Extract the Main Contract at each time and re-build a dataframe consisting of continous main contracts
        cu_price = futures[futures.INSTRUMENTID.str.startswith("cu")].reset_index()
        cu_price["exec_year"] = "20"+cu_price.INSTRUMENTID.str[2:4]
        cu_price["exec_month"] = cu_price.INSTRUMENTID.str[-2:]
        cu_price["exec_date"] = cu_price["exec_year"]+"-"+cu_price["exec_month"]+"-"+ "15"
        cu_price["exec_date"] = pd.to_datetime(cu_price["exec_date"])
        cu_price["exec_begin_date"] = cu_price["exec_date"] - pd.DateOffset(months =1)
        cu_price =cu_price[(cu_price["DATE"] > cu_price["exec_begin_date"]) & (cu_price["DATE"] <= cu_price["exec_date"])]
        cu_price = cu_price.reset_index(drop=True).sort_values("DATE").drop(["exec_year","exec_month","exec_date","exec_begin_date"], axis =1)
        cu_price = cu_price[cu_price.SETTLEMENTPRICE.isnull()==False].reset_index(drop=True)

        cu_price=cu_price[['DATE','SETTLEMENTPRICE']]


        oil = pd.read_csv("data/raw/crude oil price.csv")
        coal = pd.read_csv('data/raw/Coal_05_19_23-04_02_13.csv')
        ccfi=pd.read_csv('data/raw/ccfi.csv')
        scfi = pd.read_csv('data/raw/scfi.csv')
        US=pd.read_csv('data/raw/us-dollar-yuan-exchange-rate-historical-chart.csv')
        AUS = pd.read_csv('data/raw/australian-us-dollar-exchange-rate-historical-chart.csv')
        london = pd.read_csv('data/raw/London Aluminium Historical Data.csv')
        industry = pd.read_csv('data/raw/industrial-production-historical-chart.csv')
        acc =  pd.read_csv('data/raw/AL_corporation_of_china.csv', header=1)


        #oil
        oil["DATE"]= pd.to_datetime(oil['date'], format='%Y/%m/%d')
        oil = oil.drop(['date'],axis=1)
        oil.sort_values(by=['DATE'], inplace=True, ascending=True)
        oil.rename(columns={' value': 'PRICE'}, inplace=True)

        #scfi
        scfi["DATE"]= pd.to_datetime(scfi['date'], format='%Y/%m/%d')
        scfi = scfi.drop(['date'],axis=1)
        scfi.sort_values(by=['DATE'], inplace=True, ascending=True)
        scfi.rename(columns={'scfi_index': 'SCFI_INDEX'}, inplace=True)

        #ccfi
        ccfi["DATE"]= pd.to_datetime(ccfi['date'], format='%Y/%m/%d')
        ccfi = ccfi.drop(['date','Unnamed: 0'],axis=1)
        ccfi.sort_values(by=['DATE'], inplace=True, ascending=True)
        ccfi.rename(columns={'ccfi_index': 'CCFI_INDEX'}, inplace=True)

        #coal
        coal["DATE"]= pd.to_datetime(coal['Date'], format='%m/%d/%y')
        ##only preserve the column 'Close'
        coal = coal.drop(['Date','Volume','Low','High','Open'],axis=1)
        coal.sort_values(by=['DATE'], inplace=True, ascending=True)
        ##which is then renamed as 'Coal'
        coal.rename(columns={'Close': 'COAL'}, inplace=True)

        #US
        US["DATE"]= pd.to_datetime(US['date'], format='%Y/%m/%d')
        US = US.drop(['date'],axis=1)
        US.sort_values(by=['DATE'], inplace=True, ascending=True)
        US.rename(columns={' value': 'US_DOLLAR'}, inplace=True)

        #AUS
        AUS["DATE"]= pd.to_datetime(AUS['date'], format='%Y/%m/%d')
        AUS = AUS.drop(['date'],axis=1)
        AUS.sort_values(by=['DATE'], inplace=True, ascending=True)
        AUS.rename(columns={' value': 'AUS_DOLLAR'}, inplace=True)

        #london
        london["DATE"]= pd.to_datetime(london['Date'], format='%d/%m/%Y')
        london = london.drop(['Date','Open','High','Low','Change %'],axis=1)
        london.sort_values(by=['DATE'], inplace=True, ascending=True)
        london.rename(columns={'Price': 'LONDON_AL_PRICE','Vol.': 'LONDON_AL_VOL'}, inplace=True)
        ## convert types of Price and Volume to be float from being object
        london['LONDON_AL_PRICE'] = london['LONDON_AL_PRICE'].str.replace(',', '', regex=True).astype(float)
        london['LONDON_AL_VOL'] = london['LONDON_AL_VOL'].str.replace('K', '', regex=True).astype(float)

        #industry
        industry["DATE"]= pd.to_datetime(industry['date'], format='%Y/%m/%d')
        industry = industry.drop(['date'],axis=1)
        industry.sort_values(by=['DATE'], inplace=True, ascending=True)
        industry.rename(columns={' value': 'INDUSTRIAL_INDEX'}, inplace=True)

        #acc
        acc["DATE"]= pd.to_datetime(acc['   Date'], format='%Y/%m/%d')
        acc = acc.drop(['   Date','    High','    Low'],axis=1)
        acc.sort_values(by=['DATE'], inplace=True, ascending=True)
        acc.columns = [i.lstrip() for i in acc.columns]
        acc.rename(columns={'Open': 'ACC_OPEN','Close':'ACC_CLOSE','Volume':'ACC_VOLUME'}, inplace=True)

        #merge oil and al
        merged_2 = pd.merge(al_price, oil, on='DATE', how='left')
        merged_2.rename(columns={'PRICE': 'OIL_PRICE'}, inplace=True)

        #with scfi_index
        merged_3 = pd.merge(merged_2, scfi, on='DATE', how='left')
        merged_3.drop('Unnamed: 0', axis=1, inplace=True)

        #with ccfi_index
        merged_4 = pd.merge(merged_3, ccfi, on='DATE', how='left')

        #with coal price
        merged_5 = pd.merge(merged_4, coal, on='DATE', how='left')

        #with the exchange rate yuan/US dollar
        merged_6 = pd.merge(merged_5, US, on='DATE', how='left')

        #merge merged_6 and the exchange rate Australian dollar/yuan
        merged_7 = pd.merge(merged_6, AUS, on='DATE', how='left')

        #merge merged_6 and the copper prices
        merged_8 = pd.merge(merged_7, cu_price, on='DATE', how='left')

        #merge merged_6 and the exchange rate Australian dollar/yuan
        merged_9 = pd.merge(merged_8, london, on='DATE', how='left')

        #merge merged_6 and the Industrial Index
        merged_10 = pd.merge(merged_9, industry, on='DATE', how='left')

        #merge merged_6 and information of Aluminium Corporation of China
        merged_11 = pd.merge(merged_10, acc, on='DATE', how='left')


        import matplotlib.pyplot as plt
        from matplotlib.pyplot import figure
        merged_11.rename(columns={'SETTLEMENTPRICE_x': 'AL_PRICE','SETTLEMENTPRICE_y':'CU_PRICE'}, inplace=True)
        merged_11["INDUSTRIAL_INDEX"] = merged_11["INDUSTRIAL_INDEX"].bfill()
        figure(figsize=(12, 5), dpi=80, linewidth=10)
        plt.plot(merged_11['DATE'], merged_11['INDUSTRIAL_INDEX'])
        plt.title('INDUSTRIAL_INDEX Raw Data with Missing Values')
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Index', fontsize=14)
        
        Saver.save_plots("pikamom is stupid")

        print(merged_11.head(5))