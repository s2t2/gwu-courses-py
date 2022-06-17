
import os

from app import EXPORTS_DIRPATH
from app.driver import create_driver

CAMPUS_ID = os.getenv("CAMPUS_ID", default="1") # 1: main campus; ... others: vern, online, etc
TERM_ID = os.getenv("TERM_ID", default="202203") # YYYY ... 01: spring; 02: summer; 03: fall
SUBJECT_ID = os.getenv("CAMPUS_ID", default="EMSE") # choose your own subject of interest...

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
        #breakpoint()
        return None

    def perform(self):
        self.driver = create_driver()
        try:
            self.driver.get(self.base_url)

            self.page_counter+=1
            self.save_screenshot()
            self.save_page_source()
            self.processed_pages_counter+=1

            # todo: click the next page link!
            #next_page_link = None
            #while next_page_link:
            #    print("...", "next page")
            #    next_page_url = "TODO"
            #    self.driver.get(next_page_url)
            #    self.page_counter+=1
            #    self.save_screenshot()
            #    self.save_page_source()
            #    self.processed_pages_counter+=1
            #    next_page_link = self.next_page_link


        except Exception as err:
            print("ERR", err)

        self.driver.quit()
        print("DONE! PROCESSED", self.processed_pages_counter, "PAGE(S)")



if __name__ == "__main__":

    browser = SubjectBrowser()

    browser.perform()
