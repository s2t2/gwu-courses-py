
import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


load_dotenv()

# default path for homebrew-installed chromedriver
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", default="/usr/local/bin/chromedriver")
HEADLESS_MODE = bool(os.getenv("HEADLESS_MODE", default="false") == "true")


def create_driver(headless=HEADLESS_MODE):
    # TODO: suppress deprecation warning by passing a Service object instead of options
    # https://stackoverflow.com/questions/69918148/deprecationwarning-executable-path-has-been-deprecated-please-pass-in-a-servic
    if headless:

        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # https://stackoverflow.com/questions/67488276/selenium-within-a-docker-container-cant-find-chromedriver
        #option.add_argument("--disable-gpu")
        #option.add_argument("--disable-extensions")
        #option.add_argument("--disable-infobars")
        #option.add_argument("--start-maximized")
        #option.add_argument("--disable-notifications")

        return webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    else:
        # DeprecationWarning: executable_path has been deprecated, please pass in a Service object
        # maybe try:
        # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.service
        # service = webdriver.chrome.service.Service(executable_path=CHROMEDRIVER_PATH)
        # return webdriver.Chrome(service=service)
        return webdriver.Chrome(CHROMEDRIVER_PATH)


if __name__ == "__main__":

    driver = create_driver()
    print(driver)

    #driver.get("https://google.com")

    breakpoint()
