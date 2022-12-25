import os
from dotenv import load_dotenv
from pandas import read_csv

from app.browser import TERM_ID, CAMPUS_ID #, SubjectBrowser
from app.better_browser import BetterBrowser

load_dotenv()

SUBJECT_IDS = os.getenv("SUBJECT_IDS", default="CSCI, EMSE")


def csv_to_list(subjects_csv:str) -> list:
    """Param subjects_csv (str) a list of zero or more subject identifiers, delimited by commas (e.g. "CSCI, EMSE")"""
    if subjects_csv == "":
        return []

    return [token.strip() for token in subjects_csv.upper().split(",")]



class MultiSubjectBrowser:

    def __init__(self, term_id=TERM_ID, subject_ids=["CSCI, EMSE"], campus_ids=[CAMPUS_ID], verbose=True):
        self.term_id = term_id
        self.subject_ids = subject_ids
        self.campus_ids = campus_ids

        self.verbose = bool(verbose)
        if verbose:
            print("--------------")
            print("MULTI-SUBJECT BROWSER...")
            print("TERM:", self.term_id)
            print("SUBJECTS:", self.subject_ids)
            print("CAMPUSES:", self.campus_ids)


    def fetch_all_courses(self):
        records = []
        for subject_id in self.subject_ids:
            for campus_id in self.campus_ids:

                # TODO: in memory processing instead of writing to file
                #browser = SubjectBrowser(term_id=self.term_id, subject_id=subject_id, campus_id=campus_id)
                #subject_df = read_csv(browser.csv_filepath)
                #print(subject_id, len(subject_df))
                #records += subject_df.to_dict("records")

                browser = BetterBrowser(term_id=self.term_id, subject_id=subject_id, campus_id=campus_id)
                #browser.fetch_all_courses()
                browser.process_pages()
                print(subject_id, len(browser.courses))
                records += browser.courses

        return records


if __name__ == "__main__":


    subject_ids = csv_to_list(SUBJECT_IDS)
    browser = MultiSubjectBrowser(subject_ids=subject_ids)
    courses = browser.fetch_all_courses()

    print("FETCHED:", len(courses))
