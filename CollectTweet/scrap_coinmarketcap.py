import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup

### Advance
page = requests.get("https://coinmarketcap.com/")
soup = BeautifulSoup(page.content, 'html.parser')
coinTable = soup.find(id="currencies")
marketCap = coinTable.select(".market-cap")
marketCapList = [float(str.strip(i.get_text())) for i in marketCap]

# calculate market shares of top-n coin per whole market
globalMarketCap = 378465160823
top = 26
summ = np.sum(marketCapList[0:top])
percent = summ/globalMarketCap * 100
print(percent)
