
import os

from selenium.webdriver.common.by import By
from pandas import DataFrame, read_csv

from app import EXPORTS_DIRPATH
from app.driver import create_driver
from app.parser import PageParser

CAMPUS_ID = os.getenv("CAMPUS_ID", default="1") # 1: main campus; ... others: vern, online, etc
TERM_ID = os.getenv("TERM_ID", default="202203") # YYYY ... 01: spring; 02: summer; 03: fall
SUBJECT_ID = os.getenv("SUBJECT_ID", default="EMSE") # choose your own subject of interest...

class SubjectBrowser:
    """Browses and downloads all pages for a given subject"""

    def __init__(self, subject_id=SUBJECT_ID, term_id=TERM_ID, campus_id=CAMPUS_ID):
        self.campus_id = campus_id
        self.term_id = term_id
        self.subject_id = subject_id.upper()

        self.base_url = f"https://my.gwu.edu/mod/pws/courses.cfm?campId={self.campus_id}&termId={self.term_id}&subjId={self.subject_id}"

        self.exports_dirpath = os.path.join(EXPORTS_DIRPATH, self.subject_id)
        if not os.path.exists(self.exports_dirpath):
            os.mkdir(self.exports_dirpath)

        self.driver = None
        #self.page_parser = PageParser()
        self.page_counter = 0
        self.processed_pages_counter = 0


    @property
    def png_filepath(self):
        return os.path.join(self.exports_dirpath, f"page_{self.page_counter}.png")

    @property
    def html_filepath(self):
        return os.path.join(self.exports_dirpath, f"page_{self.page_counter}.html")

    def save_screenshot(self):
        self.driver.save_screenshot(self.png_filepath)

    def save_page_source(self):
        with open(self.html_filepath, "w") as html_file:
            html_file.write(self.driver.page_source)


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

    def process_page(self):
        self.page_counter+=1
        print("PROCESSING PAGE:", self.page_counter)
        self.save_screenshot()
        self.save_page_source()
        self.processed_pages_counter+=1

    def download_pages(self):
        self.driver = create_driver()
        try:
            self.driver.get(self.base_url)
            self.process_page()

            next_page_link = self.next_page_link
            while next_page_link:
                next_page_link.click()
                self.process_page()

                next_page_link = self.next_page_link
        except Exception as err:
            print("ERR", err)

        self.driver.quit()
        #print("DONE! PROCESSED", self.processed_pages_counter, "PAGE(S)")
        print("DONE! PROCESSED", len(self.html_filenames), "PAGE(S)")


    @property
    def html_filenames(self):
        return sorted([filename for filename in os.listdir(self.exports_dirpath) if filename.endswith(".html")])


    @property
    def csv_filepath(self):
        return os.path.join(self.exports_dirpath, "courses.csv")


    def parse_pages(self):
        records = []
        for html_filename in self.html_filenames:
            html_filepath = os.path.join(self.exports_dirpath, html_filename)

            parser = PageParser(html_filepath)
            page_records = parser.courses.to_dict("records")
            records += page_records

        df = DataFrame(records)
        df.to_csv(self.csv_filepath, index=False)
        return df


if __name__ == "__main__":

    browser = SubjectBrowser()

    if not any(browser.html_filenames):
        print("DOWNLOADING PAGES...")
        browser.download_pages()

    if os.path.isfile(browser.csv_filepath):
        courses_df = read_csv(browser.csv_filepath)
    else:
        print("PARSING PAGES...")
        courses_df = browser.parse_pages()
    print(len(courses_df))
    print(courses_df.head())
