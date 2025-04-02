import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
# Configuration de la session
capabilities = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "automationName": "UiAutomator2"
}
appium_server_url = 'http://localhost:4723/wd/hub'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    def test_open_tiktok(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="TikTok"]')
        el.click()
        time.sleep(4)
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@resource-id="com.zhiliaoapp.musically:id/juj"]')
        el.click()
        time.sleep(4)
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="com.zhiliaoapp.musically:id/c_i" and @text="Continue with Google"]')
        el.click()
        time.sleep(1)
        el=self.driver.find_element(by=AppiumBy.XPATH,value='(//android.widget.LinearLayout[@resource-id="com.google.android.gms:id/container"])[1]/android.widget.LinearLayout')
        el.click()

if __name__ == '__main__':
    unittest.main()
