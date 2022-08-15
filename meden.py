from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

login_url = "https://www.ecsc.gov.sy/login"
personal_id = "mat-input-0"
password_id = "mat-input-1"
next_button_class = "mat-primary"

class Melden:
    def __init__(self):
        self.op = webdriver.ChromeOptions()
        self.op.binary_location = os.getenv("GOOGLE_CHROME_BIN")
        self.op.add_argument('--headless')
        self.op.add_argument("--disable--dev--shm--usage")
        self.op.add_argument("--no-sandbox")
        # os.getenv("CHROMEDRIVER_PATH")
        self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), options=self.op)

    def searchElement(self, selector):
        global element
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except Exception as error:
            return False

    def check(self):
        for i in range(20) :
            if self.searchElement("div[role='alertdialog']"):
                return False
            time.sleep(0.5)
            print(i)
        return True

    def checkSite(self, url):
        try:
            self.driver.get(url)
        except Exception as error:
            return False
        return self.check()

    def const_select_options(self, select_index, option_index):
        self.driver.find_elements(By.TAG_NAME, "mat-select")[select_index].click()
        time.sleep(1)
        self.driver.find_elements(By.TAG_NAME, "mat-option")[option_index].click()
        time.sleep(1)

    def click_button(self, index):
        self.driver.find_elements(By.TAG_NAME, "button")[index].click()
        time.sleep(5)

    def login(self, personal_number, password):
        self.driver.get(login_url)
        personal_field = self.driver.find_element(By.ID, personal_id)
        password_field = self.driver.find_element(By.ID, password_id)
        next_button = self.driver.find_element(By.TAG_NAME, 'button')

        personal_field.send_keys(personal_number)
        password_field.send_keys(password)
        next_button.click()
        time.sleep(5)

    def checkDocument(self):

        # Step 2
        # self.driver.get("https://www.ecsc.gov.sy/requests")
        # self.driver.find_elements(By.TAG_NAME, "button")[3].click()
        self.driver.get("https://www.ecsc.gov.sy/requests/process/new/new")
        time.sleep(15)


        # Step 3
        # self.const_select_options(0, 5)
        self.const_select_options(1, 1)
        self.click_button(1)


        # Step 4
        self.const_select_options(2, 7)
        self.const_select_options(3, 1)
        self.const_select_options(4, 1)
        self.driver.find_elements(By.CSS_SELECTOR, "input[type= 'number']")[1].send_keys(0)
        self.const_select_options(5, 0)
        self.const_select_options(6, 2)
        self.click_button(3)

        return self.check()

    def makeDocument(self):
        # Step 5
        self.click_button(6)
        time.sleep(5)

        # Step 6
        self.click_button(1)
        self.click_button(4)
        time.sleep(10)

        self.driver.close()