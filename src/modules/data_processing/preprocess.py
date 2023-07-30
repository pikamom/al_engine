import logging
import os
from datetime import datetime, timedelta
from typing import Dict

import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import requests
from matplotlib.pyplot import figure

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class PreProcess(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def _extract_metal_price(self, metal: str) -> Dict:
        all_metal_futures = pd.read_csv("data/raw/futures prices.csv")
        all_metal_futures["DATE"] = pd.to_datetime(
            all_metal_futures["date"], format="%d/%m/%Y"
        )
        all_metal_futures = all_metal_futures.drop(
            ["TRADINGDAY", "id", "Unnamed: 0"], axis=1
        )
        metal_prices = all_metal_futures[
            all_metal_futures.INSTRUMENTID.str.startswith(metal)
        ].reset_index()
        metal_prices["exec_year"] = "20" + metal_prices.INSTRUMENTID.str[2:4]
        metal_prices["exec_month"] = metal_prices.INSTRUMENTID.str[-2:]
        metal_prices["exec_date"] = (
            metal_prices["exec_year"] + "-" + metal_prices["exec_month"] + "-" + "15"
        )
        metal_prices["exec_date"] = pd.to_datetime(metal_prices["exec_date"])
        metal_prices["exec_begin_date"] = metal_prices["exec_date"] - pd.DateOffset(
            months=1
        )
        metal_prices = metal_prices[
            (metal_prices["DATE"] > metal_prices["exec_begin_date"])
            & (metal_prices["DATE"] <= metal_prices["exec_date"])
        ]
        metal_prices = (
            metal_prices.reset_index(drop=True)
            .sort_values("DATE")
            .drop(["exec_year", "exec_month", "exec_date", "exec_begin_date"], axis=1)
        )
        metal_prices = metal_prices[
            metal_prices.SETTLEMENTPRICE.isnull() == False
        ].reset_index(drop=True)
        metal_prices = metal_prices[["DATE", "SETTLEMENTPRICE"]]

        return metal_prices

    def run(self):
        logger.info("Starting to extract metal futures prices...")
        logger.debug("Extracting Aluminium metal future prices...")
        al_price = self._extract_metal_price("al")
        logger.debug("Extracting Copper metal future prices...")
        cu_price = self._extract_metal_price("cu")
        logger.info("Metal futures prices extract complete!")

        logger.info("Reading in additional data...")

        logger.debug("Reading in oil prices...")
        oil = pd.read_csv("data/raw/crude oil price.csv")
        oil["DATE"] = pd.to_datetime(oil["date"], format="%Y/%m/%d")
        oil = oil.drop(["date"], axis=1)
        oil.sort_values(by=["DATE"], inplace=True, ascending=True)
        oil.rename(columns={" value": "OIL_PRICE"}, inplace=True)

        logger.debug("Reading in coal prices...")
        coal = pd.read_csv("data/raw/Coal_05_19_23-04_02_13.csv")
        coal["DATE"] = pd.to_datetime(coal["Date"], format="%m/%d/%y")
        coal = coal.drop(["Date", "Volume", "Low", "High", "Open"], axis=1)
        coal.sort_values(by=["DATE"], inplace=True, ascending=True)
        coal.rename(columns={"Close": "COAL"}, inplace=True)

        logger.debug("Reading in CCFI...")
        ccfi = pd.read_csv("data/raw/ccfi.csv")

        ccfi["DATE"] = pd.to_datetime(ccfi["date"], format="%Y/%m/%d")
        ccfi = ccfi.drop(["date", "Unnamed: 0"], axis=1)
        ccfi.sort_values(by=["DATE"], inplace=True, ascending=True)
        ccfi.rename(columns={"ccfi_index": "CCFI_INDEX"}, inplace=True)

        logger.debug("Reading in SCFI prices...")
        scfi = pd.read_csv("data/raw/scfi.csv")
        scfi["DATE"] = pd.to_datetime(scfi["date"], format="%Y/%m/%d")
        scfi = scfi.drop(["date", "Unnamed: 0"], axis=1)
        scfi.sort_values(by=["DATE"], inplace=True, ascending=True)
        scfi.rename(columns={"scfi_index": "SCFI_INDEX"}, inplace=True)

        logger.debug("Reading in exchange rates...")
        usd_to_yuan_exchange = pd.read_csv(
            "data/raw/us-dollar-yuan-exchange-rate-historical-chart.csv"
        )
        aud_to_yuan_exchange = pd.read_csv(
            "data/raw/australian-us-dollar-exchange-rate-historical-chart.csv"
        )

        usd_to_yuan_exchange["DATE"] = pd.to_datetime(
            usd_to_yuan_exchange["date"], format="%Y/%m/%d"
        )
        usd_to_yuan_exchange = usd_to_yuan_exchange.drop(["date"], axis=1)
        usd_to_yuan_exchange.sort_values(by=["DATE"], inplace=True, ascending=True)
        usd_to_yuan_exchange.rename(columns={" value": "US_DOLLAR"}, inplace=True)
        aud_to_yuan_exchange["DATE"] = pd.to_datetime(
            aud_to_yuan_exchange["date"], format="%Y/%m/%d"
        )
        aud_to_yuan_exchange = aud_to_yuan_exchange.drop(["date"], axis=1)
        aud_to_yuan_exchange.sort_values(by=["DATE"], inplace=True, ascending=True)
        aud_to_yuan_exchange.rename(columns={" value": "AUS_DOLLAR"}, inplace=True)

        logger.debug("Reading in london AL prices...")
        london = pd.read_csv("data/raw/London Aluminium Historical Data.csv")
        london["DATE"] = pd.to_datetime(london["Date"], format="%d/%m/%Y")
        london = london.drop(["Date", "Open", "High", "Low", "Change %"], axis=1)
        london.sort_values(by=["DATE"], inplace=True, ascending=True)
        london.rename(
            columns={"Price": "LONDON_AL_PRICE", "Vol.": "LONDON_AL_VOL"}, inplace=True
        )
        london["LONDON_AL_PRICE"] = (
            london["LONDON_AL_PRICE"].str.replace(",", "", regex=True).astype(float)
        )
        london["LONDON_AL_VOL"] = (
            london["LONDON_AL_VOL"].str.replace("K", "", regex=True).astype(float)
        )

        logger.debug("Reading in industry data...")
        industry = pd.read_csv("data/raw/industrial-production-historical-chart.csv")
        industry["DATE"] = pd.to_datetime(industry["date"], format="%Y/%m/%d")
        industry = industry.drop(["date"], axis=1)
        industry.sort_values(by=["DATE"], inplace=True, ascending=True)
        industry.rename(columns={" value": "INDUSTRIAL_INDEX"}, inplace=True)

        logger.debug("Reading in ACC company stocks...")
        acc = pd.read_csv("data/raw/AL_corporation_of_china.csv", header=1)
        acc["DATE"] = pd.to_datetime(acc["   Date"], format="%Y/%m/%d")
        acc = acc.drop(["   Date", "    High", "    Low"], axis=1)
        acc.sort_values(by=["DATE"], inplace=True, ascending=True)
        acc.columns = [i.lstrip() for i in acc.columns]
        acc.rename(
            columns={"Open": "ACC_OPEN", "Close": "ACC_CLOSE", "Volume": "ACC_VOLUME"},
            inplace=True,
        )
        logger.info("Additional data elements reading process complete!")

        logger.info("Merging all dataframes...")
        df_merged = al_price
        for table in [
            oil,
            scfi,
            ccfi,
            coal,
            usd_to_yuan_exchange,
            aud_to_yuan_exchange,
            cu_price,
            london,
            industry,
            acc,
        ]:
            logger.info(f"Merging Additional tables into [df_merged]...")
            df_merged = df_merged.merge(table, on="DATE", how="left")

        logger.info("Renaming columns...")
        df_merged.rename(
            columns={"SETTLEMENTPRICE_x": "AL_PRICE", "SETTLEMENTPRICE_y": "CU_PRICE"},
            inplace=True,
        )

        logger.info("Plotting missing values indication plot...")
        msno.matrix(df_merged)
        Saver.save_plots("missing_value_indication")

        logger.info("Filling in industrial index...")
        df_merged["INDUSTRIAL_INDEX"] = df_merged["INDUSTRIAL_INDEX"].bfill()

        logger.info("Filling in industrial index...")
        figure(figsize=(12, 5), dpi=80, linewidth=10)
        plt.plot(df_merged["DATE"], df_merged["INDUSTRIAL_INDEX"])
        plt.title("INDUSTRIAL_INDEX Raw Data with Missing Values")
        plt.xlabel("Time", fontsize=14)
        plt.ylabel("Index", fontsize=14)
        Saver.save_plots("industrial_index")

        logger.info(f"Starting Pre-processing of the industrial index")
        start_date = pd.to_datetime("2022-03-01")
        end_date = pd.to_datetime("2023-03-01")
        selected_rows = df_merged[
            (df_merged["DATE"] >= start_date) & (df_merged["DATE"] <= end_date)
        ]
        average_Industrial_value = selected_rows["INDUSTRIAL_INDEX"].mean()
        logger.debug(
            f"Average value between {start_date} and {end_date}: {average_Industrial_value}"
        )
        df_merged["INDUSTRIAL_INDEX"].fillna(average_Industrial_value, inplace=True)

        logger.info(
            "Fill the null values in CCFI_INDEX with the average of the available two consecutive weekly data"
        )
        df_merged["CCFI_INDEX_NEW"] = (
            df_merged["CCFI_INDEX"].bfill() + df_merged["CCFI_INDEX"].ffill()
        ) / 2
        df_merged.drop("CCFI_INDEX", axis=1, inplace=True)

        logger.info(
            "fill the null values in SCFI_INDEX with the average of the available two consecutive weekly data"
        )
        df_merged["SCFI_INDEX_NEW"] = (
            df_merged["SCFI_INDEX"].bfill() + df_merged["SCFI_INDEX"].ffill()
        ) / 2
        df_merged.drop("SCFI_INDEX", axis=1, inplace=True)

        logger.info("Plotting missing values indication plot again...")
        msno.matrix(df_merged)
        Saver.save_plots("missing_value_indication_after_index_ccfi_scfi_update")

        logger.info("Plotting Aluminium Corporation of China Stock prices...")
        plt.plot(df_merged["ACC_CLOSE"], label="ACC_CLOSE")
        plt.plot(df_merged["ACC_OPEN"], label="ACC_OPEN")
        plt.legend()
        Saver.save_plots("acc_stock_price")

        logger.info("Plotting Aluminium Corporation of China Stock prices...")
        df_merged = df_merged.sort_values("DATE")
        plt.plot(df_merged["DATE"], df_merged["ACC_VOLUME"], label="ACC_VOLUME")
        Saver.save_plots("acc_stock_vol")

        logger.debug(
            "Impute the missing values using Rolling Window Method(Linear Interpolation"
        )
        df_merged["ACC_OPEN"] = df_merged["ACC_OPEN"].interpolate(method="linear")
        df_merged["ACC_CLOSE"] = df_merged["ACC_CLOSE"].interpolate(method="linear")
        df_merged["ACC_VOLUME"] = df_merged["ACC_VOLUME"].interpolate(method="linear")

        logger.info("Plotting missing values indication plot again...")
        msno.matrix(df_merged)
        Saver.save_plots("missing_value_indication_after_acc_update")

        logger.debug("Backfilling all the other columns...")
        df_merged["OIL_PRICE"] = df_merged["OIL_PRICE"].bfill()
        df_merged["COAL"] = df_merged["COAL"].bfill()
        df_merged["US_DOLLAR"] = df_merged["US_DOLLAR"].bfill()
        df_merged["AUS_DOLLAR"] = df_merged["AUS_DOLLAR"].bfill()
        df_merged["LONDON_AL_PRICE"] = df_merged["LONDON_AL_PRICE"].bfill()
        df_merged["LONDON_AL_VOL"] = df_merged["LONDON_AL_VOL"].bfill()

        print(df_merged.head(5))
