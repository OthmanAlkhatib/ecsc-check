from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class Melden:
    def __init__(self):
        self.op = webdriver.ChromeOptions()
        self.op.binary_location = os.getenv("GOOGLE_CHROME_BIN")
        self.op.add_argument('--headless')
        self.op.add_argument("--disable--dev--shm--usage")
        self.op.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), options=self.op)

    def searchSubmitButton(self):
        global button
        try:
            button = self.driver.find_element(By.ID, "applicationForm:managedForm:proceed")
            return True
        except Exception as error:
            # print(error)
            return False

    def checkSite(self):
        self.driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen/wizardng/ad889662-ea23-4531-ace3-1f1564c62f71;jsessionid=RniDnAVxpXktXVxtF_mceXWtDg0zFg0wPAiqzEM6.frontend-2?dswid=2275&dsrid=668&st=2&v=1659631472533")
        while not self.searchSubmitButton():
            time.sleep(1)

        button.click()
        time.sleep(30)
        try:
            message = self.driver.find_element(By.CLASS_NAME, "errorMessage")
            print("====== No Places ======")
            return False
            # time.sleep(60)
        except Exception as error:
            # messagebox.showinfo("VISA", "Go Take Visa Now!")
            print(error)
            return True