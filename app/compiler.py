
import os

from pandas import DataFrame, read_csv

from app import EXPORTS_DIRPATH
from app.browser import SubjectBrowser

if __name__ == "__main__":

    records = []
    subject_ids = [dirname for dirname in os.listdir(EXPORTS_DIRPATH) if "." not in dirname]

    for subject_id in subject_ids:
        browser = SubjectBrowser(subject_id=subject_id)
        subject_df = read_csv(browser.csv_filepath)
        print(subject_id, len(subject_df))
        records += subject_df.to_dict("records")

    # one CSV file to rule them all :-)
    # easy to import to google sheets, and filter there
    df = DataFrame(records)
    print("-------")
    print("TOTAL:", len(df))
    df.to_csv(os.path.join(EXPORTS_DIRPATH, "all_courses.csv"))
