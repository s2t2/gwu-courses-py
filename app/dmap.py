
import os
from dotenv import load_dotenv

#from selenium import webdriver
#from selenium.webdriver import Chrome
#from selenium.webdriver.chrome.options import Options


from app.driver import create_driver

load_dotenv()

CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", default="/path/to/your/chrome/profile")
#CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", default="/Users/mjr/Library/Application Support/Google/Chrome/Profile 4")


# for now we will use the saved HTML file instead of a live page we browsed to

#import email
#
#def read_html_file(html_filepath):
#    with open(html_filepath, 'r', encoding='utf-8') as f:
#        return f.read()
#
#def read_and_parse_saved_page(html_filepath):
#    page_source = read_html_file(html_filepath)
#
#    html_content = None
#    if page_source:
#        message = email.message_from_string(page_source)
#
#        for part in message.walk():
#            if part.get_content_type() == 'text/html':
#                html_content = part.get_payload(decode=True)  # Decoding from quoted-printable encoding
#                break
#
#    return html_content


from typing import List

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

    try:
        gpa_span = soup.find('span', string='Block GPA:')
        gpa_div = gpa_span.parent
        gpa_text = gpa_div.text.strip()
        major_gpa = gpa_text.replace('Block GPA:', '').strip()
    except:
        major_gpa = None

    try:
        honors_status = soup.find("span", id="RA004062_statusLabel").text.strip()
    except:
        honors_status = None

    return {
        "gwid": student_id,
        "name": student_name,
        "major_gpa": major_gpa,
        "honors_status": honors_status
    }


def navigate_to_student_dashboard_page(driver, student_id):
    """requires the logged in user to have admin access to student search!"""
    print(driver.title)
    breakpoint()

    #
    # PART ONE (SEARCH)
    #

    student_id_input = driver.find_element(By.NAME, "studentId") # CHECK ELEMENT NAME
    student_id_input.send_keys(student_id)

    search_button = driver.find_element(By.XPATH, '//button[text()="SEARCH"]')  # CHECK XPATH
    search_button.click()
    print(driver.title)

    #
    # PART TWO (SELECT)
    #

    wait_condition = EC.element_to_be_clickable((By.XPATH, '//button[text()="SELECT"]'))
    search_button = WebDriverWait(driver, 10).until(  wait_condition  )
    search_button.click()
    print(driver.title)

    return driver.page_source


def get_all_students(driver, student_ids: List):
    records = []
    for student_id in student_ids:
        page_source = navigate_to_student_dashboard_page(driver, student_id)
        record = parse_student_dashboard_page(page_source)
        records.append(record)
    return record


if __name__ == "__main__":

    #driver = create_driver(profile_path=CHROME_PROFILE_PATH, headless=False)
    driver = create_driver(headless=False)

    request_url = "https://degreemap.gwu.edu/worksheets/WEB31"
    driver.get(request_url)
    # since this is in non headless mode, we can manually sign in and provide the 2fa code
    # unfortunately this does not use the logged in user info from the browser profile?
    print(driver.title) #> 'DegreeMAP Dashboard'

    breakpoint()

    #soup = BeautifulSoup(driver.page_source, "html.parser")
    #parse_student_dashboard_page(driver.page_source)

    print("---------------")
    print("READING STUDENT IDENTIFIERS FROM CSV...")
    df = read_csv(os.path.join(DATA_DIRPATH, "student_ids.csv"))
    print(df.head())

    print("---------------")
    print("NAVIGATING DEGREE MAP...")
    student_ids = df["gwid"].tolist()
    records = get_all_students(driver, student_ids)
    print("RETRIEVED INFO FOR", len(records), "STUDENTS")

    print("---------------")
    print("SAVING RECORDS TO CSV...")
    exports_df = DataFrame(records)
    exports_df.to_csv(os.path.join(EXPORTS_DIRPATH, "student_honors.csv"), index=False)


    driver.quit()
