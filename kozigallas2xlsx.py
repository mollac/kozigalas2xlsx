import requests
from bs4 import BeautifulSoup
import pandas as pd

jobUrl = "https://kozszolgallas.ksz.gov.hu/JobAd/Info/"


def getPage(page):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition developer)',
        'X-Requested-With': 'XMLHttpRequest',
        'dnt': '1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera";v="106"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
    }

    params = {
        'page': f'{page}',
        'sort': 'Created DESC',
        'countyCode': 'county.gyormosonsopron',
    }

    response = requests.get(
        'https://kozszolgallas.ksz.gov.hu/JobAd/List', params=params, headers=headers)
    return BeautifulSoup(response.content, "html.parser")


nPage = 1
master_list = []
while True:
    print(f"Gathering page:", nPage)
    html = getPage(nPage)
    if len(html) <= 6:
        break
    divs = html.find_all("div", {"class", "jobad"})
    for div in divs:
        data = {}
        data["link"] = jobUrl+div['id']
        data["mit"] = div.h4.strong.text.split("\n")[1].strip().upper()
        data["kinél"] = div.h5.strong.text
        data["hol"] = div.select('li')[2].get_text(strip=True)
        data["meddig"] = div.select('h6')[1].get_text(strip=True)
        master_list.append(data)
    nPage += 1

df = pd.DataFrame(master_list)
df.to_excel('kozig.xlsx', index="")
