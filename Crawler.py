import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import tqdm
import warnings

warnings.filterwarnings("ignore")

# Constants
MIN_PRICE = 8_000_000
MAX_PRICE = 15_000_000
QUERY = "Asus"
LIMIT = 100
TARGET_URL = "https://www.tokopedia.com/search?"
MIN_RATING_4 = True


class WebCrawler:
    def __init__(self, url, min_price, max_price, query, limit, min_rating_4):
        self.URL = url
        self.driver = None
        self.query = query
        self.max_price = max_price
        self.min_price = min_price
        self.limit = limit
        self.min_rating = min_rating_4

    def driver_setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)

    def query_parametize(self):
        self.query = self.query.replace(" ", "%20")
        self.URL += f"ob=3&origin_filter=sort_price&pmax={self.max_price}&pmin={self.min_price}&q={self.query}"
        if self.min_rating:
            self.URL += "&rt=4%2C5"

    def run(self):
        self.driver_setup()
        self.query_parametize()
        self.driver.get(self.URL)
        self.scroll_down()
        self.get_product_info()

    def scroll_down(self):
        SCROLL_PAUSE_TIME = 0.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_product_info(self):
        df = pd.DataFrame(
            columns=[
                "Product Name",
                "Product Price",
                "Product Rating",
                "Product Sales",
                "Product URL",
            ]
        )
        page = 1
        num_product = 0

        self.progres_bar = tqdm.tqdm(
            total=self.limit,
            position=0,
            leave=False,
            desc="Scraping Tokopedia",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

        while len(df) < self.limit:
            url_now = self.URL + f"&page={page}"
            self.driver.get(url_now)
            time.sleep(1)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(0.2)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            if soup.find(text="Oops, produk nggak ditemukan"):
                print("Limit reached at page", page)
                break

            for product, price, url in zip(
                soup.find_all("div", class_="prd_link-product-name"),
                soup.find_all("div", class_="prd_link-product-price"),
                soup.find_all("a", class_="pcv3__info-content"),
            ):
                if price.text:
                    df.loc[len(df)] = [
                        product.text if product.text else "N/A",
                        price.text,
                        "N/A",
                        "N/A",
                        url["href"],
                    ]

            for rating, sales in zip(
                soup.find_all("span", class_="prd_rating-average-text"),
                soup.find_all("span", class_="prd_label-integrity"),
            ):
                df.loc[len(df) - 1, "Product Rating"] = rating.text
                df.loc[len(df) - 1, "Product Sales"] = sales.text

            page += 1

            if len(df) == num_product:
                print("Limit reached at page", page)
                break

            num_product = len(df)
            self.progres_bar.update(len(df))

        self.driver.close()
        self.progres_bar.close()

        df = df[: self.limit]
        print(f"Succesfully scraped {len(df)} products")
        df.drop_duplicates(inplace=True)
        df.to_csv("tokopedia.csv", index=False)


if __name__ == "__main__":
    crawler = WebCrawler(TARGET_URL, MIN_PRICE, MAX_PRICE, QUERY, LIMIT, MIN_RATING_4)
    crawler.run()
