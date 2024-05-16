
import os

from app import EXPORTS_DIRPATH
from app.dmap.user import Student


if __name__ == "__main__":

    exports_filepath = os.path.join(EXPORTS_DIRPATH, "dmap", "student_dashboard.csv")

    browser = Student()
    try:
        browser.login()
        df = browser.parse_dashboard()
        print(df.head())
        df.to_csv(exports_filepath)

    except Exception as err:
        print("ERROR:", err)
        breakpoint()

        #try:
        #    browser.login()
        #    df = browser.parse_dashboard()
        #    print(df.head())
        #    df.to_csv(exports_filepath)
        #except Exception as err:
        #    print("ERROR 2:", err)
        #    breakpoint()

    browser.driver.quit()
