import requests as rs
from bs4 import BeautifulSoup
import json as js
import csv
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
csv_file = open('web_scrape.csv', "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product Link', 'Product Name', 'Product Brand', 'Size Available', 'Price', 'MRP', 'Gender', 'Description', 'Primary Image Link', 'Secondary Image Link'])
for i in range(1, 201): # 50 products on each page, mult 200 page = 10k
    url = "https://www.myntra.com/men-tshirts?p={p}&plaEnabled=false".format(p = i)
    page = rs.get(url, headers = headers).text
    soup = BeautifulSoup(page, 'html5lib')
    script = soup.find_all('script')[11].text.strip()[15:]
    jsonFile = js.loads(script)
    dt = jsonFile['searchData']['results']['products']
    for data in dt:
        link = 'https://www.myntra.com/' + data['landingPageUrl']
        name = data['productName']
        brand = data['brand']
        sizes = data['sizes']
        price = data['price']
        mrp = data['mrp']
        gender = data['gender']
        priimg = data['searchImage']
        secimg = data['images'][-1]['src']
        nhtml = rs.get(link, headers = headers).text
        nsoup = BeautifulSoup(nhtml, 'html5lib')
        nscripts = nsoup.find_all('script')[11].text.strip()[15:]
        ndt = js.loads(nscripts)
        ndt = ndt['pdpData']['productDetails']
        description = ndt[0]['description']
        csv_writer.writerow([link, name, brand, sizes, price, mrp, gender, description, priimg, secimg])
    print(str(i) + " completed") #just for knowing that, which pages are scraped
csv_file.close()
