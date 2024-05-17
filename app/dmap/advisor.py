

from app.dmap.user import StudentAdvisor


if __name__ == "__main__":

    import os
    from app import DATA_DIRPATH, EXPORTS_DIRPATH
    from pandas import read_csv

    DEPT = os.getenv("DEPT") or input("Input a department code (e.g. 'PSC'): ") or "PSC"
    csv_filepath = os.path.join(DATA_DIRPATH, "dmap", DEPT.upper(), "student_ids.csv")
    exports_filepath = os.path.join(EXPORTS_DIRPATH, "dmap", DEPT.upper(), "student_dashboards.csv")

    print("---------------")
    print("READING STUDENT IDENTIFIERS FROM CSV...")
    df = read_csv(csv_filepath)
    print(df.head())

    student_ids = df["gwid"].tolist()
    print("STUDENTS:", len(student_ids))

    print("---------------")
    print("BROWSING...")
    browser = StudentAdvisor() #dept=DEPT
    try:
        browser.login()
        df = browser.parse_dashboards(student_ids=student_ids)
        print(df.head())
        df.to_csv(exports_filepath)
    except Exception as err:
        print("ERROR:", err)
        breakpoint()

        #df = browser.parse_dashboards(student_ids=student_ids[0:50])
        #df.to_csv(os.path.join(EXPORTS_DIRPATH, "dmap", DEPT.upper(), "student_dashboards_0_50.csv"))

        df100 = browser.parse_dashboards(student_ids=student_ids[50:150])
        df100.to_csv(os.path.join(EXPORTS_DIRPATH, "dmap", DEPT.upper(), "student_dashboards_50_150.csv"))

        df250 = browser.parse_dashboards(student_ids=student_ids[150:])
        df250.to_csv(os.path.join(EXPORTS_DIRPATH, "dmap", DEPT.upper(), "student_dashboards_150_end.csv"))

    breakpoint()
    browser.driver.quit()
