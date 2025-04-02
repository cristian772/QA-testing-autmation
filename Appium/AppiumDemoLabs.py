import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
# Configuration de la session
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
capabilities = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "automationName": "UiAutomator2"
}
appium_server_url = 'http://localhost:4723/wd/hub'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    def test_1open_demo(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="My Demo App"]')
        el.click()
        time.sleep(4)
        el = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(0)')
        el.click()
    def test_2add_to_card(self) -> None:
        el= self.driver.find_element(by=AppiumBy.ID,value="com.saucelabs.mydemoapp.android:id/cartBt")
        el.click()
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cartIV")
        el.click()

    def test_3clickcheckout(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cartBt")
        el.click()

    def test_4login(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/nameET")
        el.click()
        el.send_keys("bod@example.com")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/passwordET")
        el.click()
        el.send_keys("10203040")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/loginBtn").click()

    def test_5checkout(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/fullNameET")
        el.send_keys("Test Cristian")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/address1ET").send_keys("Rue des Tests")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cityET").send_keys("Paris")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/zipET").send_keys("75000")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/countryET").send_keys("France")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/paymentBtn").click()
    def test_6payement(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/nameET").send_keys("Cristian Test")
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cardNumberET").send_keys("3258125676587891")
        el = self.driver.find_element(by=AppiumBy.ID,value="com.saucelabs.mydemoapp.android:id/expirationDateET").send_keys("03/27")
        el = self.driver.find_element(by=AppiumBy.ID,value="com.saucelabs.mydemoapp.android:id/securityCodeET").send_keys("327")
        el = self.driver.find_element(by=AppiumBy.ID,value="com.saucelabs.mydemoapp.android:id/paymentBtn").click()
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/paymentBtn").click()
    def test_7place_order(self)-> None:
        el = self.driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/paymentBtn").click()
if __name__ == '__main__':
    unittest.main()
