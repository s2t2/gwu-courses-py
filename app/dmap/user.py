
import os
from typing import List
from time import sleep

#from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame, concat

#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

from app import DATA_DIRPATH, EXPORTS_DIRPATH
from app.driver import create_driver
from app.dmap.dashboard_parser import DashboardParser


class User:

    def __init__(self, driver=None):
        self.driver = driver or create_driver(headless=False) # profile_path=CHROME_PROFILE_PATH

    def login(self, driver=None):
        """Manual Login. Requires user sitting at the computer."""
        #driver = driver or self.driver

        print("---------------")
        print("VISITING DEGREE MAP...")
        request_url = "https://degreemap.gwu.edu/worksheets/WEB31"
        self.driver.get(request_url)
        # since this is in non headless mode, we can manually sign in and provide the 2fa code
        # unfortunately this does not use the logged in user info from the browser profile?
        sleep(20)




    @property
    def logged_in(self):
        return bool(self.driver.title == 'DegreeMAP Dashboard')



class Student(User):
    def __init__(self, driver=None):
        super().__init__(driver=driver)
        self.parser = None

    #def login(self):
    #    super().login()
    #    # WAIT FOR SOME CONTENT WE WANT TO PARSE LATER:
    #    #wait = WebDriverWait(self.driver, 10)
    #    #xpath = "//h2[span[contains(text(), 'Fall Through General Electives')]]"
    #    #wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #
    #    #wait = WebDriverWait(self.driver, 15)
    #    #xpath = "//h2[span[contains(text(), 'In-progress')]]"
    #    #wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #
    #    #wait = WebDriverWait(self.driver, 10)
    #    #xpath = "//h2[span[contains(text(), 'Not Counted')]]"
    #    #wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #
    #    #sleep(5)
    #    #print("LOGGED IN:", self.logged_in)
    #    #sleep(5)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def parse_dashboard(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        self.parser = DashboardParser(self.driver.page_source)
        df = self.parser.df
        df.index.name = "row_num"
        df.index += 1
        return df


if __name__ == "__main__":

    exports_filepath = os.path.join(EXPORTS_DIRPATH, "dmap", "student.csv")

    browser = Student()
    try:
        browser.login()
        df = browser.parse_dashboard()
        print(df.head())
        df.to_csv(exports_filepath)
    except Exception as err:
        print("ERROR:", err)
        #breakpoint()

        try:
            browser.login()
            df = browser.parse_dashboard()
            print(df.head())
            df.to_csv(exports_filepath)
        except Exception as err:
            print("ERROR 2:", err)
            breakpoint()

    browser.driver.quit()
