
from typing import List
from time import sleep

from pandas import DataFrame, concat

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.driver import create_driver
from app.dmap.dashboard_parser import DashboardParser


class User:

    def __init__(self, driver=None):
        self.driver = driver or create_driver(headless=False) # profile_path=CHROME_PROFILE_PATH

    def login(self, request_url="https://degreemap.gwu.edu/worksheets/WEB31", max_retries=3):
        """Manual Login. Requires user sitting at the computer."""
        print("---------------")
        print("VISITING DEGREE MAP...")
        print(request_url)
        self.driver.get(request_url)

        # since this is in non headless mode, we can manually sign in and provide the 2fa code
        # give us enough time to do all these things:
        retries = 0
        while not self.logged_in and retries <= max_retries:
            print("TIME FOR YOU TO LOGIN PLEASE...")
            sleep(15)
            retries +=1
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

    def __init__(self, driver=None):
        super().__init__(driver=driver)

        self.dashboards_df = DataFrame()


    def parse_dashboards(self, student_ids:List[str]):
        if not self.logged_in:
            self.login()

        for i, student_id in enumerate(student_ids):
            print("STUDENT:", i)
            self.search_student(student_id=student_id)

            parser = DashboardParser(self.driver.page_source)
            self.dashboards_df = concat([self.dashboards_df, parser.df], ignore_index=True)

        self.dashboards_df.index.name = "row_num"
        self.dashboards_df.index += 1
        return self.dashboards_df

    def search_student(self, student_id):

        # WAIT AND LOCATE:
        sleep(3)
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

        # WAIT FOR SOME CONTENT WE WANT TO PARSE LATER
        # ... (IF IT EXISTS, OTHERWISE CONTINUE):
        try:
            wait = WebDriverWait(self.driver, 10)
            xpath = "//h2[span[contains(text(), 'Departmental/Special Honors')]]"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException as err:
            print("ERR:", err)
            print("CONTINUING...")
