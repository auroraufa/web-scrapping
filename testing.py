import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

merk = input('please enter cars merk : ')
total_pages_input = input('Total Page that you want to scrape : ')
total_pages = int(total_pages_input) 
link = "https://www.mobil123.com/mobil-dijual/{}/indonesia?page_number={}&page_size=25"    

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
}

datas = []
count_page = 0
path = 'C://Program Files//Mozilla Firefox//firefox.exe'
options = FirefoxOptions()
options.binary_location = path
driver = webdriver.Firefox(options=options)

for page_number in range(1, total_pages + 1):
    count_page+= 1
    print("count page : ", count_page)
    url = link.format(merk, page_number)
    
    req = requests.get(url, headers=headers)
    print(req)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('article','listing--card')
    
    for data in items:
        names = ''.join(data.find('h2', 'listing__title').text.strip().replace(',', '').split('\n'))
        price_element = data.find('div', class_='listing__price')
        price_span = price_element.find('span', class_='weight--semibold')
        if price_span:
            price = price_span.text.strip()
        else:
            price = price_element.text.strip()
        specs = data.find_all('div', 'item')
        km = ''.join(specs[0].text.strip().split('\n'))
        transmisi = ''.join(specs[1].text.strip().split('\n'))
        try:
            label = ''.join(data.find('div', 'listing__label').text.strip().split('\n'))
        except:
             label= ''
        
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'listing__ctr')))

        driver.execute_script("document.getElementsByClassName('listing__ctr')[0].click();")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]")))

        nama_kontak_element = driver.find_element(By.CLASS_NAME, "listing__seller-name")
        alamat_kontak_element = driver.find_element(By.CLASS_NAME, "listing__location")
        nomor_kontak_element = driver.find_element(By.CLASS_NAME, "number")

        nama_kontak = ''.join(nama_kontak_element.text.strip().split('\n'))
        alamat_kontak = ''.join(alamat_kontak_element.text.strip().split('\n'))
        nomor_kontak = nomor_kontak_element.text

        datas.append([names, price, km, transmisi, label, nama_kontak, alamat_kontak, nomor_kontak])

driver.close()

title = ['Name', 'Price', 'Car KM', 'Transmisi', 'Label', "Dealers's Names", 'Address', 'Phone Number']
with open('results/{}_scrapping.csv'.format(merk), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(title)
    for data in datas:
        writer.writerow(data)

        
            
                   