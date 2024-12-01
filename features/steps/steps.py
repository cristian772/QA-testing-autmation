import time

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By

@given("I sign in as standard_user")
def standard_user_login(context):
    context.driver=webdriver.Chrome()
    context.driver.get('https://www.saucedemo.com/')
    username = context.driver.find_element(By.ID, 'user-name')
    username.send_keys('standard_user')
    password = context.driver.find_element(By.ID, 'password')
    password.send_keys("secret_sauce")
    context.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    assert context.driver.current_url == 'https://www.saucedemo.com/inventory.html'

@when('I add a backpack to cart')
def adding_backpack_to_cart(context):
    context.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack").click()

@then("the backpack shoud be on cart")
def assert_backpack_on_cart(context):
    context.driver.get('https://www.saucedemo.com/cart.html')
    assert context.driver.find_element(By.ID,"item_4_title_link")

@when('I add all the products to the cart')
def add_all_items(context):
    buttons = context.driver.find_elements(By.CSS_SELECTOR, ".btn.btn_primary")
    for index, button in enumerate(buttons):
        try:
            button.click()
        except:
            pass
@when("I click on cart and proceed check out")
def Iclickoncart(context):
    assert context.driver.current_url=="https://www.saucedemo.com/inventory.html"
    context.driver.find_element(By.CSS_SELECTOR,"a[class='shopping_cart_link']").click()
    context.driver.find_element(By.ID,"checkout").click()
@when("I put my delivery information")
def check_out(context):
    firstn=context.driver.find_element(By.ID,"first-name")
    firstn.send_keys("Antoine")
    context.driver.find_element(By.ID, "last-name").send_keys("Dupont")
    context.driver.find_element(By.ID,"postal-code").send_keys("75000")
    context.driver.save_screenshot("features/checkout.png")
    context.driver.find_element(By.ID, "continue").click()
    context.driver.find_element(By.ID, "finish").click()

@then("I should see Thank you for your order!")
def order_bye(context):
    assert context.driver.current_url=="https://www.saucedemo.com/checkout-complete.html"
    header_element = context.driver.find_element(By.CSS_SELECTOR, ".complete-header")
    assert  header_element.text == "Thank you for your order!"
    context.driver.save_screenshot("features/Thank you for your.png")
