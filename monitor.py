from attr import attr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import discord
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
import time
import urllib.request

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
count = 0
links = {
    "Newmarket": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=NMKT&mfr=&pr=",
    "North York": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=NO&mfr=&pr=",
    "Brampton": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=1304&mfr=&pr=",
    "Etobicoke": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=ETOB&mfr=&pr=",
    "Markham": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=MU&mfr=&pr=",
    "Mississauga": "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=MISS&mfr=&pr=",
}
stores = ["Newmarket", "North York", "Brampton", "Etobicoke", "Markham", "Mississauga"]
old = [[] for store in stores]
new = [[] for store in stores]
init = True
while True:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get(links[stores[count]])

    last_h = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_h = driver.execute_script("return document.body.scrollHeight")
        if new_h == last_h:
            break
        last_h = new_h

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    webhook = Webhook.from_url(
        "https://discord.com/api/webhooks/828039746986442753/M-9VnM4P1huQrQXvaIlhj-_FHNjYKgzDtiWjkWQKRmRcUHFamhhsYG8CDY80o4SmIO-T",
        adapter=RequestsWebhookAdapter(),
    )
    for element in soup.findAll(attrs={"class": "col-12 productImageDesc"}):
        sub = element.findChildren(recursive="false")
        for child in sub:
            if child.find(attrs={"class": "text-dark text-truncate_3"}):
                title = child.find(attrs={"class": "text-dark text-truncate_3"})
            if child.find(
                attrs={"class": "d-block mb-0 pq-hdr-product_price line-height"}
            ):
                price = child.find(
                    attrs={"class": "d-block mb-0 pq-hdr-product_price line-height"}
                )
            if child.find(attrs={"class": "pq-img-manu_logo align-self-center"}):
                image = child.find(
                    attrs={"class": "pq-img-manu_logo align-self-center"}
                )
        if init == True:
            old[count].append(title.text)
            new[count].append(title.text)
        else:
            new[count].append(title.text)
            if title.text not in old[count]:
                urllib.request.urlretrieve(image["src"], "gpu.jpg")
                img = discord.File("./gpu.jpg", filename="gpu.jpg")
                embed = discord.Embed(title="New card found", url=title["href"])
                embed.set_thumbnail(url="attachment://gpu.jpg")
                embed.add_field(name="Product:", value=title.text)
                embed.add_field(name="Price:", value=price.text)
                embed.add_field(name="Store", value=stores[count])
                webhook.send(file=img, embed=embed)
    if init == False:
        old[count] = new[count]
        new[count] = []

    if count < len(stores) - 1:
        print(old[count])
        count += 1
    else:
        count = 0
        init = False
