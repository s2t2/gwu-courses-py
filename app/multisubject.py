import os
from dotenv import load_dotenv
from pandas import read_csv
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.browser import TERM_ID, CAMPUS_ID #, SubjectBrowser
from app.better_browser import BetterBrowser

load_dotenv()

SUBJECT_IDS = os.getenv("SUBJECT_IDS", default="CSCI, EMSE")
MAX_WORKERS = 10 # worker per subject, we can set a max limit of ten

def csv_to_list(subjects_csv:str) -> list:
    """Param subjects_csv (str) a list of zero or more subject identifiers, delimited by commas (e.g. "CSCI, EMSE")"""
    if subjects_csv == "":
        return []

    return [token.strip() for token in subjects_csv.upper().split(",")]



class MultiSubjectBrowser:

    def __init__(self, term_id=TERM_ID, subject_ids=["CSCI, EMSE"], campus_ids=[CAMPUS_ID], verbose=True):
        """
            Params
                subject_ids (list or CSV string)

        """
        self.term_id = term_id
        if isinstance(subject_ids, str):
            subject_ids = csv_to_list(subject_ids)
        self.subject_ids = subject_ids
        self.campus_ids = campus_ids

        self.verbose = bool(verbose)
        if verbose:
            print("--------------")
            print("MULTI-SUBJECT BROWSER...")
            print("TERM:", self.term_id)
            print("SUBJECTS:", self.subject_ids)
            print("CAMPUSES:", self.campus_ids)
            print("--------------")

        self.courses = None


    def browse_subject(self, subject_id, campus_id):
        browser = BetterBrowser(term_id=self.term_id, subject_id=subject_id, campus_id=campus_id)
        browser.process_pages()
        return browser.courses

    def fetch_all_courses(self):
        self.courses = []
        for subject_id in self.subject_ids:
            for campus_id in self.campus_ids:

                #browser = BetterBrowser(term_id=self.term_id, subject_id=subject_id, campus_id=campus_id)
                ##browser.fetch_all_courses()
                #browser.process_pages()
                #print(subject_id, len(browser.courses))
                #self.courses += browser.courses

                self.courses += self.browse_subject(subject_id, campus_id)

        return self.courses

    def fetch_all_courses_threaded(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            print("EXECUTOR:", type(executor))

            #futures = [executor.submit(self.process_batch, i) for i in range(len(df_test))]
            futures = []
            for subject_id in self.subject_ids:
                for campus_id in self.campus_ids:
                    future = executor.submit(self.browse_subject, subject_id, campus_id)
                    futures.append(future)
            print("FUTURES:", len(futures))

            self.courses = []
            for index, future in enumerate(as_completed(futures)):
                print("SUBJECT", index+1, "COMPLETED")
                result = future.result()
                self.courses += result

        return self.courses





if __name__ == "__main__":

    from app import EXPORTS_DIRPATH
    from pandas import DataFrame

    subject_ids = csv_to_list(SUBJECT_IDS)
    browser = MultiSubjectBrowser(subject_ids=subject_ids)

    threaded = input("THREADED?") or "y"
    if threaded.upper() == "Y":
        courses = browser.fetch_all_courses_threaded()
    else:
        courses = browser.fetch_all_courses()

    print("FETCHED:", len(courses))

    courses_df = DataFrame(courses)
    print(courses_df)
    courses_df.to_csv(os.path.join(EXPORTS_DIRPATH, "all_courses_better.csv"))
