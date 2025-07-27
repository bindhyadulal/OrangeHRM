from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Variables
url = "https://opensource-demo.orangehrmlive.com/"
username = "Admin"
password = "admin123"

# Setup WebDriver
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Login
wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Searching and clicking 'Time' menu
search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
search_input.send_keys("Time")
time.sleep(1)
driver.find_element(By.XPATH, "//span[text()='Time']").click()

# Wait for Time page to load and locate Employee Name input
emp_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='Employee Name']/following::input[1]")))

# Enter employee name with special characters
emp_input.send_keys("A234@#$%P3r3z")
time.sleep(1)
emp_input.send_keys(Keys.ENTER)

# Click the 'View' button
view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' View ']")))
view_button.click()
print("View button clicked.")

# Assert and extracting the 'Invalid' error message
invalid_message = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message') and text()='Invalid']")
))
assert invalid_message.text == "Invalid", "'Invalid' message not found"
print("Invalid message displayed:", invalid_message.text)

# === Navigate to PIM ===
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()
# === Input Supervisor Name instead of Employee Name ===
supervisor_input = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//label[text()='Supervisor Name']/following::input[1]")
))
supervisor_input.clear()
supervisor_input.send_keys("abcde")

# === Click Search button ===
search_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button') and normalize-space()= 'Search']")
))
search_button.click()

# Wait for and assert the 'Invalid' message below Supervisor Name input
invalid_msg = wait.until(EC.visibility_of_element_located(
    (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message') and text()='Invalid']")
))
assert invalid_msg.text == "Invalid", "'Invalid' message not displayed as expected"
print("Invalid message displayed:", invalid_msg.text)


# === Cleanup ===
time.sleep(3)
driver.quit()
