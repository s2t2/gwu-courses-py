
import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


load_dotenv()

# default path for homebrew-installed chromedriver
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", default="/usr/local/bin/chromedriver")
CHROME_BINARY_PATH = os.getenv("CHROME_BINARY_PATH") # specify path where chrome binary is installed, as necessary (see "build.sh")
HEADLESS_MODE = bool(os.getenv("HEADLESS_MODE", default="false") == "true")


def create_driver(headless=HEADLESS_MODE, chromedriver_path=CHROMEDRIVER_PATH, binary_location=CHROME_BINARY_PATH):

    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument('--no-sandbox')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')

    # help Mac find where you installed Chrome
    # help production server find custom installation of chrome binary (see "build.sh"):
    if binary_location:
        # https://github.com/SeleniumHQ/selenium/blob/4071737de47f1cec2dfef934f3e18a2e36db20d5/py/selenium/webdriver/chromium/options.py#L34
        options.binary_location = binary_location

    #return webdriver.Chrome(chromedriver_path, options=options)

    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)


if __name__ == "__main__":

    driver = create_driver()
    print(driver)

    driver.get("https://gwcoders.github.io/studyGroup/")

    breakpoint()

    driver.quit()
