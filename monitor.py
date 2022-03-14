from attr import attr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import discord
from discord import Webhook, RequestsWebhookAdapter
from bs4 import BeautifulSoup
import time
from PIL import Image
import urllib.request

client = discord.Client()
chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)
driver.get(
    "https://www.canadacomputers.com/index.php?cPath=43_557&sf=:3_3,3_4,3_5,3_6,3_7,3_8,3_9,3_12,3_29,3_30,3_31,3_32,3_33&loc=NMKT&mfr=&pr="
)


last_h = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    new_h = driver.execute_script("return document.body.scrollHeight")
    if new_h == last_h:
        break
    last_h = new_h

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")


channel = client.get_channel(828037920564183100)
webhook = Webhook.from_url(
    "https://discord.com/api/webhooks/828039746986442753/M-9VnM4P1huQrQXvaIlhj-_FHNjYKgzDtiWjkWQKRmRcUHFamhhsYG8CDY80o4SmIO-T",
    adapter=RequestsWebhookAdapter(),
)
for element in soup.findAll(attrs={"class": "col-12 productImageDesc"}):
    sub = element.findChildren(recursive="false")
    for child in sub:
        if child.find(attrs={"class": "text-dark text-truncate_3"}):
            title = child.find(attrs={"class": "text-dark text-truncate_3"})
        if child.find(attrs={"class": "d-block mb-0 pq-hdr-product_price line-height"}):
            price = child.find(
                attrs={"class": "d-block mb-0 pq-hdr-product_price line-height"}
            )
        if child.find(attrs={"class": "pq-img-manu_logo align-self-center"}):
            image = child.find(attrs={"class": "pq-img-manu_logo align-self-center"})
    urllib.request.urlretrieve(image["src"], "gpu.jpg")
    img = discord.File("./gpu.jpg", filename="gpu.jpg")
    embed = discord.Embed(title="New card found", url=title["href"])
    embed.set_thumbnail(url="attachment://gpu.jpg")
    embed.add_field(name="Product:", value=title.text)
    embed.add_field(name="Price:", value=price.text)
    webhook.send(file=img, embed=embed)
