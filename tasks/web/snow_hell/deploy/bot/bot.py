from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# from selenium.common.exceptions import UnexpectedAlertBehaviour
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import sleep


webdriver.DesiredCapabilities.FIREFOX["unexpectedAlertBehaviour"] = "accept"
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
# capabilities.setCapability(CapabilityType.UNEXPECTED_ALERT_BEHAVIOUR, UnexpectedAlertBehaviour.ACCEPT);
# driver = webdriver.Firefox()


def openURL(url):
    try:
        driver.get("{}".format(url))
        # print(driver.page_source)
        print("sucessfully opened url")
    except Exception as ex:
        print("smth went wrong", ex)


def form_filler(id, info):
    elem = driver.find_element_by_id("{}".format(id))
    driver.execute_script("arguments[0].value='{0}';".format(info), elem)
    print("form filled")


def form_submitter(id):
    elem = driver.find_element_by_id("{}".format(id))
    elem.submit()
    print("form submitted")


def refresher():
    driver.refresh()
    print(driver.page_source)
    print("page refreshed")


def clicker(link):
    driver.find_element_by_link_text("{}".format(link)).click()
    print("link clicked")


def closer():
    driver.close()
    print("session closed")


openURL("http://task/login")
form_filler("username", "admin")
form_filler("password", "ee6b4deb587078e5423813736fdbc6c2aeca47fde86bc95877cb780be91d5bc3")
form_submitter("password")
sleep(2)
openURL("http://task/my_congr")
sleep(2)
while True:
    # for i in range(0, 3):
    try:
        openURL("http://task/my_congr")
        # refresher()
        sleep(30)
    except InterruptedError:
        break
    # except UnexpectedAlertBehaviour:
    #    print("We have raised the UnexpectedAlertBehaviour")
    except UnexpectedAlertPresentException:
        print("UnexpectedAlertPresentException")
    except Exception as ex:
        print("exc", ex)
closer()
