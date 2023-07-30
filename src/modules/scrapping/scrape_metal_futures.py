from src.modules.base import Module
import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger()


class Test(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self) -> None:
        """
        Webscrape metals future prices from shanghai futures exchange
        """

        headers_for_use = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "cookie": "test_accepte_cookie=1; idsess=a9db65f6; cartid=463849; _ga=GA1.2.1083246416.1665430026; _gid=GA1.2.662145473.1665430026; __cf_bm=QJPDcwXc57aJmaoNqto63qd9ue2cM1No3xxG6OGdnQg-1665430024-0-ATG20uOT6Ksq2P3L/mdwOLHXo6adec3KmNI92XBbv2wUEdErb8y87bKfGy0PpX6i1nAUWw2rBaCv1TXrWSBVaw5EqYWOmOzH5S5KtRZqYcIVkHkTiMtEVDPCY8JZoyAHFQ==; cookieconsent2021=1; collectestatus=ok; collectestatuscookie=ok; _gat_gtag_UA_17756636_1=1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        logger.debug(f"Setting headers to use, details: [{headers_for_use}]]...")

        logger.info("Starting a requests session")
        session = requests.Session()

        today = datetime.now()
        logger.debug(
            f"Today's date is {today}, Webscrapper will start looking for data from yesterday in a backward fashion"
        )

        daily_data = []
        back_tracked_days = 0
        number_of_backtrack_days = 20
        logger.debug(f"Number of backtracked days is [{number_of_backtrack_days}]")

        while back_tracked_days < number_of_backtrack_days:
            yesterday = today - timedelta(1)
            date_format_for_api = datetime.strftime(yesterday, "%Y%m%d")
            date_format_for_df = datetime.strftime(yesterday, "%Y-%m-%d")
            logger.debug(
                f"Starting the webscraping process from [{date_format_for_df}]"
            )

            url = f"https://www.shfe.com.cn/data/instrument/Settlement{date_format_for_api}.dat"
            logger.debug(f"Trying to access url: [{url}]")
            response = session.get(url, headers=headers_for_use)

            if response.status_code == 200:
                logger.debug(
                    f"Successful in obtaining metal future prices for {date_format_for_df}"
                )
                df_metal_prices = pd.DataFrame.from_dict(response.json()["Settlement"])
                df_metal_prices["date"] = date_format_for_df

                logger.info(f"Outputting future prices...")
                daily_data.append(df_metal_prices)
            else:
                logger.debug(
                    f"There are no futures prices data for {date_format_for_df} or connection was not successful"
                )

            today = yesterday
            back_tracked_days += 1


if __name__ == "__main__":
    test_class = Test()
    test_class._run()
