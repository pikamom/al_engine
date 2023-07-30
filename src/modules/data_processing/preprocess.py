from src.modules.base import Module
import requests
import pandas as pd
from datetime import datetime, timedelta
from src.utils.saver import Saver
import logging
import os

logger = logging.getLogger()

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

        print(al_price.head(5))

        print(al_price.shape)