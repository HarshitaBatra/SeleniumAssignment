from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import unittest

class SauceDemoTestSuite(unittest.TestCase):

    def setUp(self):
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

        # Login
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()

    def test_checkout_flow(self):
        driver = self.driver

        # Select 3 random items
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        selected_items = random.sample(inventory_items, 3)
        for item in selected_items:
            item.find_element(By.CLASS_NAME, "btn_inventory").click()

        # Go to cart
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Assert 3 items in the cart
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 3, "There should be 3 items in the cart.")

        # Proceed to checkout
        driver.find_element(By.ID, "checkout").click()

        # Enter user information
        driver.find_element(By.ID, "first-name").send_keys("Harshita")
        driver.find_element(By.ID, "last-name").send_keys("Batra")
        driver.find_element(By.ID, "postal-code").send_keys("324002")
        driver.find_element(By.ID, "continue").click()

        # Finish checkout
        driver.find_element(By.ID, "finish").click()

        # Assert checkout completion
        completion_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        self.assertEqual(completion_message.text, "THANK YOU FOR YOUR ORDER")

    def tearDown(self):
        self.driver.quit()
