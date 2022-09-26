from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import discord
from discord import SyncWebhook
from bs4 import BeautifulSoup
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

link = "https://www.metacareers.com/jobs/?page=1&results_per_page=100#search_result"

old = []
new = []
init = True
while True:
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get(link)

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    webhook = SyncWebhook.from_url(
        "https://discord.com/api/webhooks/828039746986442753/M-9VnM4P1huQrQXvaIlhj-_FHNjYKgzDtiWjkWQKRmRcUHFamhhsYG8CDY80o4SmIO-T")

    for element in soup.findAll(attrs={"class": "_af0h"}):
        sub = element.findChildren(recursive="false")
        for child in sub:
            if child.find(attrs={"class": "_8sel _97fe"}):
                title = child.find(attrs={"class": "_8sel _97fe"})
            if child.find(attrs={"class": "_8see _97fe"}):
                location = child.find(attrs={"class": "_8see _97fe"})
        if init == True:
            old.append(title.text)
            new.append(title.text)
        else:
            print("aaaa")
            print(location.text)
            new.append(title.text)
            if title.text in old:
                embed = discord.Embed(title="New job found")
                embed.add_field(name="Position:", value=title.text)
                embed.add_field(name="Location:", value=location.text)
                print(title.text)
                print(location.text)
    init = False
    if init == False:
        old = new
        new = []
    time.sleep(10)
