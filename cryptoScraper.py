from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import argparse

chrome_driver_path = r'C:\\Users\\nafis\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service)


def scraping(web_url, output_csv):
    driver.get(web_url)
    driver.implicitly_wait(10)
    time.sleep(10)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for i in range(12): 
        while True:
            driver.execute_script(f"window.scrollBy(0,500)")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            
            last_height = new_height
        while True:
            try:
                load_more_button = driver.find_element('xpath','//div[@class="cmc-table-listing__loadmore"]/button[@type="button"]')
                load_more_button.click()
                time.sleep(3)
            except:
                break

    rank = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__rank"]')
    name = driver.find_elements('xpath','//a[@class="cmc-table__column-name--name cmc-link"]')
    symbol = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--hide-sm cmc-table__cell--sort-by__symbol"]/div')
    marketCap = driver.find_elements('xpath','//span[@class="sc-11478e5d-1 jfwGHx"]')
    price = driver.find_elements('xpath','//div[@class="sc-b3fc6b7-0 dzgUIj"]')
    cirSupply = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply"]')
    vol24h = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h"]')
    per1h = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h"]/div')
    per24h = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h"]/div')
    per7d = driver.find_elements('xpath','//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d"]/div')
  
    all_data = []

    for index in range(len(rank)):
        all_data.append({
            "rank": rank[index].text,
            "name": name[index].text,
            "symbol": symbol[index].text,
            "market_cap": marketCap[index].text,
            "price": price[index].text,
            "ciculating_supply": cirSupply[index].text,
            "volume_24h": vol24h[index].text,
            "percent_1h": per1h[index].text,
            "percent_24h": per24h[index].text,
            "percent 7d": per7d[index].text
        })
        
    df = pd.DataFrame(data=all_data)
    df.to_csv(output_csv, index=False)

    return f"data has been saved in {output_csv}"


if __name__ == "__main__":


    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--url", help = "link web yang akan di scraping")
    parser.add_argument("-o", "--output", help = "file hasil scraping web")

    args = parser.parse_args()

    scraping(args.url, args.output)