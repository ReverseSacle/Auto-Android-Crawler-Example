from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver,locator,value,timeout=30,poll_frequency=0.5):
    WebDriverWait(driver, timeout,poll_frequency).until(lambda d:d.find_element(locator, value))