
from app.driver import create_driver

def test_driver():

    request_url = "https://github.com/s2t2"
    driver = create_driver(headless=True)
    #assert driver.caps.headless # NOT A THING?

    driver.get(request_url)
    assert driver.current_url == request_url

    driver.quit()
