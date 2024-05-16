

from app.dmap.user import StudentAdvisor


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
