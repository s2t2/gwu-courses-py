
import os

from selenium.webdriver.common.by import By
from pandas import DataFrame, read_csv

from app.driver import create_driver
from app.better_parser import BetterParser

CAMPUS_ID = os.getenv("CAMPUS_ID", default="1") # 1: main campus; ... others: vern, online, etc
TERM_ID = os.getenv("TERM_ID", default="202203") # YYYY ... 01: spring; 02: summer; 03: fall
SUBJECT_ID = os.getenv("SUBJECT_ID", default="EMSE") # choose your own subject of interest...

class BetterBrowser:
    """Browses and parses all pages for each given subject, and stores the results in memory"""

    def __init__(self, subject_id=SUBJECT_ID, term_id=TERM_ID, campus_id=CAMPUS_ID):
        self.campus_id = campus_id
        self.term_id = term_id
        self.subject_id = subject_id.upper()

        self.base_url = f"https://my.gwu.edu/mod/pws/courses.cfm?campId={self.campus_id}&termId={self.term_id}&subjId={self.subject_id}"

        self.driver = None
        self.page_counter = 0
        self.processed_pages_counter = 0
        self.courses = None


    def process_pages(self):
        self.courses = []
        self.driver = create_driver()
        try:
            self.driver.get(self.base_url)
            self.courses += self.process_page()

            next_page_link = self.next_page_link
            while next_page_link:
                next_page_link.click()
                self.courses += self.process_page()

                next_page_link = self.next_page_link
        except Exception as err:
            print("ERR", err)

        self.driver.quit()
        print("DONE! PROCESSED", self.processed_pages_counter, "PAGE(S)")
        return self.courses


    def process_page(self):
        self.page_counter+=1
        print("PROCESSING PAGE:", self.page_counter)
        html_contents = self.driver.page_source
        parser = BetterParser(html_contents)
        self.processed_pages_counter+=1
        return parser.courses


    @property
    def next_page_link(self):
        """
        This is the link we are looking for:
            <a href="javascript:nextPage()">Next Page &gt;&gt; </a>

        Returns a selenium.webdriver.remote.webelement.WebElement or None
        """
        try:
            return self.driver.find_element(By.PARTIAL_LINK_TEXT, "Next Page")
        except:
            return None



if __name__ == "__main__":

    browser = BetterBrowser()

    #breakpoint()

    courses = browser.process_pages()
    #print(courses_df[0:10])

    courses_df = DataFrame(courses)
    print(len(courses_df))
    print(courses_df.head())
