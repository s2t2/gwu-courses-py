
import os
from dotenv import load_dotenv

#from selenium import webdriver
#from selenium.webdriver import Chrome
#from selenium.webdriver.chrome.options import Options


from app.driver import create_driver

load_dotenv()

CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", default="/path/to/your/chrome/profile")
#CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", default="/Users/mjr/Library/Application Support/Google/Chrome/Profile 4")




from typing import List
from time import sleep

from bs4 import BeautifulSoup
from pandas import read_csv, DataFrame
#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#

from app import DATA_DIRPATH, EXPORTS_DIRPATH


def parse_student_dashboard_page(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    try:
        gwid_input = soup.find('input', {'id': 'studentSearch'})
        if not gwid_input:
            gwid_input = soup.find('input', id="student-id")
        student_id = gwid_input["value"]
    except:
        student_id = None

    try:
        student_name = soup.find('input', {'id': 'student-name'})["value"]
    except:
        student_name = None

    major_gpa = None
    #try:
    #    gpa_span = soup.find('span', string='Block GPA:')
    #    gpa_div = gpa_span.parent
    #    gpa_text = gpa_div.text.strip()
    #    major_gpa = gpa_text.replace('Block GPA:', '').strip()
    #except:
    #    major_gpa = None

    honors_status = None
    #try:
    #    honors_status = soup.find("span", id="RA004062_statusLabel").text.strip()
    #except:
    #    honors_status = None

    breakpoint()

    return {
        "gwid": student_id,
        "name": student_name,
        "major_gpa": major_gpa,
        "honors_status": honors_status
    }


#def navigate_to_student_dashboard_page(driver, student_id):
#    """requires the logged in user to have admin access to student search!"""
#    print(driver.title)
#    breakpoint()
#
#    #
#    # PART ONE (SEARCH)
#    #
#
#    #student_id_input = driver.find_element(By.NAME, "studentSearch-label")
#    #student_id_input = driver.find_element(By.ID, "studentSearch-label")
#    #student_id_input = driver.find_element(By.XPATH, '//input[@aria-label="hidden-search-input"]')
#
#    #input_element = driver.find_element(By.XPATH, '//input[@aria-label="hidden-search-input"]')
#
#    #driver.implicitly_wait(3)
#
#    input_field = driver.find_element(By.ID, 'studentSearch')
#    input_field.clear()  # Clears any pre-filled text in the input box
#    input_field.send_keys(student_id)
#    #search_button = driver.find_element(By.ID, 'studentSearch_Adornment')
#    #search_button.click()
#    # press enter to search!
#    input_field.send_keys(Keys.ENTER)
#
#
#    #search_button = driver.find_element(By.XPATH, '//button[text()="SEARCH"]')  # CHECK XPATH
#    #search_button.click()
#    print(driver.title)
#
#    #
#    # PART TWO (SELECT)
#    #
#
#    #wait_condition = EC.element_to_be_clickable((By.XPATH, '//button[text()="SELECT"]'))
#    #search_button = WebDriverWait(driver, 10).until(  wait_condition  )
#    #search_button.click()
#    #print(driver.title)
#
#    return driver.page_source




def student_search(driver, student_id):
    # WAIT AND LOCATE:
    sleep(2)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'studentSearch')))
    input_field = driver.find_element(By.ID, 'studentSearch')
    sleep(1)

    # CLEAR:
    input_field.clear()  # Clears any pre-filled text in the input box
    clear_button = driver.find_element(By.ID, 'studentSearch_Adornment')
    clear_button.click()
    sleep(1)

    # INPUT:
    input_field.send_keys(student_id)
    sleep(1)
    input_field.send_keys(Keys.ENTER)
    sleep(3)
    print(driver.title)

    # WAIT FOR SOME CONTENT WE WANT TO PARSE LATER:
    #"h2", "block-RA004062"
    wait = WebDriverWait(driver, 10)
    xpath = "//h2[span[contains(text(), 'Departmental/Special Honors')]]"
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    #return driver.page_source



def browse_all_students(driver, student_ids: List):
    records = []
    for i, student_id in enumerate(student_ids):
        print("STUDENT:", i)
        student_search(driver, student_id)
        record = parse_student_dashboard_page(driver.page_source)
        records.append(record)
    return records



if __name__ == "__main__":

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
    print("NAVIGATING DEGREE MAP...")
    driver = create_driver(headless=False)
    #driver = create_driver(profile_path=CHROME_PROFILE_PATH, headless=False)

    request_url = "https://degreemap.gwu.edu/worksheets/WEB31"
    driver.get(request_url)
    # since this is in non headless mode, we can manually sign in and provide the 2fa code
    # unfortunately this does not use the logged in user info from the browser profile?
    print(driver.title) #> 'DegreeMAP Dashboard'
    sleep(5)
    #breakpoint()
    #soup = BeautifulSoup(driver.page_source, "html.parser")
    #parse_student_dashboard_page(driver.page_source)

    try:

        records = browse_all_students(driver, student_ids)
        print("RECORDS:", len(records))

        print("---------------")
        print("SAVING RECORDS TO CSV...")
        exports_df = DataFrame(records)
        exports_df.to_csv(exports_filepath, index=False)

    except Exception as err:
        print("ERROR:", err)
        # we are seeing an initial fail, so we need to run the code manually, but that works
        breakpoint()

        records = browse_all_students(driver, student_ids)
        print("RECORDS:", len(records))

        print("---------------")
        print("SAVING RECORDS TO CSV...")
        exports_df = DataFrame(records)
        exports_df.to_csv(exports_filepath, index=False)

        #records = get_all_students(driver, student_ids[0:25])
        #exports_df = DataFrame(records)
        #exports_df.to_csv(os.path.join(EXPORTS_DIRPATH, "student_honors_0_25.csv"), index=False)
        ## DONE
        #records = get_all_students(driver, student_ids[25:75])
        #exports_df = DataFrame(records)
        #exports_df.to_csv(os.path.join(EXPORTS_DIRPATH, "student_honors_25_75.csv"), index=False)
        ## DONE
        #records = get_all_students(driver, student_ids[75:175])
        #exports_df = DataFrame(records)
        #exports_df.to_csv(os.path.join(EXPORTS_DIRPATH, "student_honors_75_175.csv"), index=False)
        ## DONE
        #records = get_all_students(driver, student_ids[175:])
        #exports_df = DataFrame(records)
        #exports_df.to_csv(os.path.join(EXPORTS_DIRPATH, "student_honors_175_end.csv"), index=False)
        ## DONE


    driver.quit()
