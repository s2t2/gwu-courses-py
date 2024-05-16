
#import os
from typing import List
from time import sleep

from pandas import DataFrame, concat

#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

#from app import DATA_DIRPATH, EXPORTS_DIRPATH
from app.driver import create_driver
from app.dmap.dashboard_parser import DashboardParser


class User:

    def __init__(self, driver=None):
        self.driver = driver or create_driver(headless=False) # profile_path=CHROME_PROFILE_PATH

    def login(self):
        """Manual Login. Requires user sitting at the computer."""
        #driver = driver or self.driver

        print("---------------")
        print("VISITING DEGREE MAP...")
        request_url = "https://degreemap.gwu.edu/worksheets/WEB31"
        print(request_url)
        self.driver.get(request_url)
        # since this is in non headless mode, we can manually sign in and provide the 2fa code
        # give us enough time to do all these things:
        if not self.logged_in:
            print("TIME FOR YOU TO LOGIN PLEASE...")
            sleep(30)
        print(self.driver.title)

    @property
    def logged_in(self):
        return bool(self.driver.title == 'DegreeMAP Dashboard')


class Student(User):
    def __init__(self, driver=None):
        super().__init__(driver=driver)
        self.parser = None

    def parse_dashboard(self):
        if not self.logged_in:
            self.login()

        sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        self.parser = DashboardParser(self.driver.page_source)
        df = self.parser.df

        df.index.name = "row_num"
        df.index += 1
        return df


class StudentAdvisor(User):

    def __init__(self, student_ids:List[str], driver=None):
        super().__init__(driver=driver)
        self.student_ids = student_ids

    def parse_dashboards(self):
        if not self.logged_in:
            self.login()

        df = DataFrame()
        for i, student_id in enumerate(self.student_ids):
            print("STUDENT:", i)
            self.search_student(student_id=student_id) #, driver=driver)

            sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

            parser = DashboardParser(self.driver.page_source)
            concat([df, parser.df])

        df.index.name = "row_num"
        df.index += 1
        return df

    def search_student(self, student_id):

        # WAIT AND LOCATE:
        sleep(2)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'studentSearch')))

        input_field = self.driver.find_element(By.ID, 'studentSearch')
        sleep(1)

        # CLEAR:
        input_field.clear()
        # ACTUALLY CLEAR:
        clear_button = self.driver.find_element(By.ID, 'studentSearch_Adornment')
        clear_button.click()
        sleep(1)

        # INPUT:
        input_field.send_keys(student_id)
        sleep(1)
        input_field.send_keys(Keys.ENTER)
        sleep(3)
        print(self.driver.title)

        # WAIT FOR SOME CONTENT WE WANT TO PARSE LATER:
        #"h2", "block-RA004062"
        wait = WebDriverWait(self.driver, 10)
        xpath = "//h2[span[contains(text(), 'Departmental/Special Honors')]]"
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
