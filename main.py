from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="parser"
)
mycursor = mydb.cursor()

ser = Service(r"C:\Users\kimva\Downloads\newParser-3.0\chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=ser, options=op)

print("webdriver opened")
driver.get('https://hh.kz/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=159')

print("page opened")

delay = 5  # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'bloko-button')))
    print("Page is ready!")
    myel = driver.find_elements(By.TAG_NAME, "a")
    num = 0
    a = len(myel)

    for i in myel:
        linkattr = i.get_attribute('href')

        if '//nur-sultan.hh.kz/vacancy/' in linkattr:
            print(i.get_attribute('href'))
            itt = i.get_attribute('href')
            i.click()
            time.sleep(5)
            window_name = driver.window_handles[1]
            driver.switch_to.window(window_name=window_name)
            myElem1 = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'g-user-content')))
            print(myElem1.get_attribute("textContent"))
            sql = "INSERT INTO vacancy (description, link) VALUES (%s, %s)"

            val = (myElem1.get_attribute("textContent"), itt)
            mycursor.execute(sql, val)
            mydb.commit()
            driver.execute_script("window.close();")
            window_name = driver.window_handles[0]
            driver.switch_to.window(window_name=window_name)
    driver.quit()
except TimeoutException:
    print("Loading took too much time!")