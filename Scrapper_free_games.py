from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

base_url = os.getenv("BASE_URL")

link  = "https://store.epicgames.com/en-US"


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome()
driver.get(link)


WebDriverWait(driver,20).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

WebDriverWait(driver,20).until(
    EC.presence_of_element_located((By.CLASS_NAME,"css-1myhtyb"))
)


time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html,"html.parser")


data = []
sp = soup.find("div",class_="css-1myhtyb")
for game in sp:
    game_obj={}
    game_obj["Game_name"] = game.find("div",class_="css-1p5cyzj-ROOT").find("h6").text
    game_obj["Game_link"]=f"https://store.epicgames.com{game.find("a",class_="css-g3jcms").get("href")}"
    game_obj["Game_status"]=game.find("div",class_=re.compile(r"css-(82y1uz|gyjcm9)")).text
    timeperiod = game.find_all("time")
    temp=[]
    for t in timeperiod:
        temp.append(t.text)
    game_obj["Game_free_timeperiod"] = f"{temp[0]}-{temp[1]}"
    # print(game_obj)
    data.append(game_obj)
json_data = json.dumps(data,indent=4)
print(json_data)

auto_delete_table_data = requests.delete(f"{base_url}/delete-all")

time.sleep(1)

if auto_delete_table_data.status_code==200:
    print("Old data deleted")
    response = requests.post(f"{base_url}/add-free-games",json=data)

    if response.status_code==200:
        print("New free games added")
    else:
        print(f"Error while deleting data : {response.status_code}",response.text)

else:
    print(f"Error while deleting data : {auto_delete_table_data.status_code}",auto_delete_table_data.text)









# q =  requests.get("http://127.0.0.1:8000/get-free-games")
# print(q.json())
