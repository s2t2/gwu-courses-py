
from typing import List
from time import sleep


from pandas import DataFrame, concat

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from app.dmap.dashboard_parser import DashboardParser
from app.dmap.user import User



class StudentAdvisor(User):

    def __init__(self, student_ids:List[str], driver=None):
        super().__init__(driver=driver)
        self.student_ids = student_ids

    def parse_dashboards(self): # driver=None
        #driver = driver or self.driver
        #records = []
        df = DataFrame()
        for i, student_id in enumerate(self.student_ids):
            print("STUDENT:", i)
            self.visit_student_dashboard(student_id=student_id) #, driver=driver)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            parser = DashboardParser(self.driver.page_source)

            #records.extend(parser.heading_records)
            concat([df, parser.df])
        #return records
        breakpoint()

        df.index.name = "row_num"
        df.index += 1
        return df

    def visit_student_dashboard(self, student_id): # driver=None
        # STUDENT SEARCH
        #driver = self.driver

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




if __name__ == "__main__":

    import os
    from app import DATA_DIRPATH, EXPORTS_DIRPATH
    from pandas import read_csv

    DEPT = os.getenv("DEPT") or input("Input a department code (e.g. 'PSC'): ") or "PSC"
    csv_filepath = os.path.join(DATA_DIRPATH, "dmap", DEPT.upper(), "student_ids.csv")
    exports_filepath = os.path.join(EXPORTS_DIRPATH, DEPT.upper(), "student_honors.csv")

    print("---------------")
    print("READING STUDENT IDENTIFIERS FROM CSV...")
    df = read_csv(csv_filepath)
    print(df.head())

    student_ids = df["gwid"].tolist()
    print("STUDENTS:", len(student_ids))

    print("---------------")
    print("BROWSING...")
    browser = StudentAdvisor(student_ids=student_ids) #dept=DEPT
    try:
        browser.login()
        df = browser.parse_dashboards()
        print(df.head())
        df.to_csv(exports_filepath)
    except Exception as err:
        print("ERROR:", err)
        breakpoint
