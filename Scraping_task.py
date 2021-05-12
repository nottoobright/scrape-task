import csv
import requests
import shutil
import urllib.request
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    URL = 'https://downtowndallas.com/experience/stay/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(URL)
    popup = driver.find_element_by_xpath('//*[@id="popup"]')
    popup.click()
    driver.back()
    button = driver.find_element_by_xpath("/html/body/main/div/section[2]/div[1]/div[3]/a")
    button.click()

    fields = ['Name', 'Image_Url', 'Address', 'Phone', 'Area']
    details = []

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    temp_name = soup.find('h1', class_='place-name')
    temp_img_url = soup.find('img', class_='attachment-hero size-hero').get('src')
    temp_details = soup.find_all('div', class_='place-info-address')
    details.append(temp_name.text.strip())
    details.append(temp_img_url)
    for el in temp_details:
        links = el.find('a')
        details.append(links.text.strip())
    for i in details:
        print(i)

    r = requests.get(details[1], headers={'User-Agent': 'Mozilla'}, stream=True)
    if r.status_code == 200:
        with open('D:\scraped_images\image.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    with open('D:\scraped_images\data.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerow(details)

if __name__ == "__main__":
  scrape()